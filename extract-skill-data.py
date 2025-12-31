#!/usr/bin/env python3
"""
Extract comprehensive data from all lite SKILL.md files
Generates JSON with trigger patterns, inputs, outputs, process steps
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional

def extract_frontmatter(content: str) -> Dict[str, str]:
    """Extract YAML frontmatter"""
    match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}

    frontmatter = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()

    return frontmatter

def extract_section(content: str, section_name: str) -> Optional[str]:
    """Extract content of a specific section"""
    # Try ## heading first
    pattern = rf'^## {re.escape(section_name)}$(.*?)(?=^## |\Z)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)

    if not match:
        # Try ### heading
        pattern = rf'^### {re.escape(section_name)}$(.*?)(?=^### |\Z)'
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL)

    if match:
        return match.group(1).strip()
    return None

def extract_trigger_keywords(when_invoke: str) -> List[str]:
    """Extract trigger keywords from When to Invoke section"""
    keywords = []

    # Look for quoted phrases
    quoted = re.findall(r'"([^"]+)"', when_invoke)
    keywords.extend(quoted)

    # Look for user says patterns
    user_says = re.findall(r'User(?:\s+(?:says|asks))?:\s*"([^"]+)"', when_invoke, re.IGNORECASE)
    keywords.extend(user_says)

    return keywords

def extract_file_paths(section: str, pattern: str = r'`([^`]+\.(md|json|yaml|yml|py|ts|tsx))`') -> List[str]:
    """Extract file paths from a section"""
    if not section:
        return []

    paths = re.findall(pattern, section)
    return [p[0] for p in paths]

def extract_process_steps(process_section: str) -> List[str]:
    """Extract key process steps"""
    if not process_section:
        return []

    steps = []
    # Look for ### Step headings
    step_pattern = r'### (Step \d+:? [^\n]+)'
    step_matches = re.findall(step_pattern, process_section)
    steps.extend(step_matches)

    return steps[:6]  # Limit to first 6 steps

def check_auto_queue(skill_name: str, content: str) -> Optional[Dict[str, str]]:
    """Check if skill has auto-queue capability"""
    if 'Step 0: Check for Queue' in content:
        # Extract queue file name
        queue_match = re.search(r'\.queues/([a-z-]+\.md)', content)
        if queue_match:
            return {
                'has_queue': True,
                'queue_file': queue_match.group(1),
                'mode': 'auto-detect mode when queue exists'
            }
    return None

def process_skill(skill_name: str) -> Dict:
    """Process a single skill and extract all metadata"""
    skill_path = Path(f'install/skills/{skill_name}/SKILL.md')

    if not skill_path.exists():
        return {'error': 'SKILL.md not found'}

    content = skill_path.read_text(encoding='utf-8')

    # Extract sections
    frontmatter = extract_frontmatter(content)
    when_invoke = extract_section(content, 'When to Invoke')
    prerequisites = extract_section(content, 'Prerequisites')
    reads = extract_section(content, 'Context Files This Skill Reads')
    writes = extract_section(content, 'Context Files This Skill Writes')
    process = extract_section(content, 'Process')

    # Build profile
    profile = {
        'name': frontmatter.get('name', skill_name),
        'description': frontmatter.get('description', ''),
        'triggers': {
            'keywords': extract_trigger_keywords(when_invoke or ''),
            'section': when_invoke[:300] if when_invoke else ''
        },
        'inputs': extract_file_paths(reads or ''),
        'outputs': extract_file_paths(writes or ''),
        'process_steps': extract_process_steps(process or ''),
        'auto_queue': check_auto_queue(skill_name, content)
    }

    return profile

# Main execution
if __name__ == '__main__':
    # Load manifest
    with open('install/profiles/lite.manifest.json') as f:
        manifest = json.load(f)

    skills = manifest['skills']['definitions']

    # Process all skills
    profiles = {}
    for skill in skills:
        print(f'Processing {skill}...')
        profiles[skill] = process_skill(skill)

    # Save to JSON
    output_path = Path('skill-profiles.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(profiles, f, indent=2, ensure_ascii=False)

    print(f'\n[OK] Extracted data for {len(profiles)} skills')
    print(f'[OK] Saved to: {output_path}')

    # Print summary
    auto_queue_count = sum(1 for p in profiles.values() if p.get('auto_queue'))
    print(f'\nSummary:')
    print(f'  - Skills with auto-queue: {auto_queue_count}')
    print(f'  - Total skills: {len(profiles)}')
