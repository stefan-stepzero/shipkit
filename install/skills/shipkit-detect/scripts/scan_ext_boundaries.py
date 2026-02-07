#!/usr/bin/env python3
"""
Scan source code for external service integrations missing operational boundaries.
Creates queue for review via preflight or manual fix.

Checks for external SDK imports/usage and whether timeout, resource limits,
and error handling are configured in the same file or nearby config.
"""

import re
from pathlib import Path
from datetime import datetime

# External service patterns: SDK imports and API call signatures
EXTERNAL_SERVICES = {
    'openai': {
        'detect': [r'from\s+[\'"]openai', r'OpenAI\(', r'openai\.', r'createChatCompletion'],
        'boundary_signals': [r'timeout', r'maxTokens', r'max_tokens', r'maxOutputTokens', r'AbortController', r'signal:'],
    },
    'anthropic': {
        'detect': [r'from\s+[\'"]@anthropic', r'Anthropic\(', r'anthropic\.', r'messages\.create'],
        'boundary_signals': [r'timeout', r'max_tokens', r'AbortController', r'signal:'],
    },
    'google-ai': {
        'detect': [r'from\s+[\'"]@google', r'GoogleGenerativeAI\(', r'gemini', r'generateContent'],
        'boundary_signals': [r'timeout', r'maxOutputTokens', r'AbortController', r'signal:'],
    },
    'replicate': {
        'detect': [r'from\s+[\'"]replicate', r'Replicate\(', r'replicate\.run'],
        'boundary_signals': [r'timeout', r'AbortController'],
    },
    'stripe': {
        'detect': [r'from\s+[\'"]stripe', r'Stripe\(', r'stripe\.'],
        'boundary_signals': [r'timeout', r'maxNetworkRetries', r'idempotencyKey'],
    },
    'resend': {
        'detect': [r'from\s+[\'"]resend', r'Resend\(', r'resend\.emails'],
        'boundary_signals': [r'timeout', r'AbortController'],
    },
    'supabase': {
        'detect': [r'from\s+[\'"]@supabase', r'createClient.*supabase', r'supabase\.from\('],
        'boundary_signals': [r'timeout', r'AbortController', r'signal:'],
    },
    'fetch-external': {
        'detect': [r'fetch\([\'"]https?://(?!localhost)'],
        'boundary_signals': [r'timeout', r'AbortController', r'signal:', r'AbortSignal\.timeout'],
    },
}

# Source file patterns to scan
SOURCE_GLOBS = [
    'src/**/*.ts',
    'src/**/*.tsx',
    'src/**/*.js',
    'src/**/*.jsx',
    'app/**/*.ts',
    'app/**/*.tsx',
    'lib/**/*.ts',
    'pages/api/**/*.ts',
]


def scan_file(file_path):
    """Scan a single file for external services and their boundary config."""
    try:
        content = file_path.read_text()
    except Exception:
        return []

    findings = []

    for service_name, config in EXTERNAL_SERVICES.items():
        # Check if this file uses the external service
        service_detected = False
        matched_patterns = []
        for pattern in config['detect']:
            if re.search(pattern, content):
                service_detected = True
                matched_patterns.append(pattern)

        if not service_detected:
            continue

        # Check if boundary signals exist in the same file
        boundaries_found = []
        boundaries_missing = []
        for signal in config['boundary_signals']:
            if re.search(signal, content):
                boundaries_found.append(signal)
            else:
                boundaries_missing.append(signal)

        # Flag if service detected but no boundary signals at all
        if not boundaries_found:
            findings.append({
                'service': service_name,
                'file': str(file_path),
                'status': 'no_boundaries',
                'missing': boundaries_missing,
            })
        # Flag if only partial boundaries (e.g., timeout but no token limit)
        elif boundaries_missing and len(boundaries_found) < len(config['boundary_signals']) // 2:
            findings.append({
                'service': service_name,
                'file': str(file_path),
                'status': 'partial_boundaries',
                'found': boundaries_found,
                'missing': boundaries_missing,
            })

    return findings


def scan():
    """Scan project for external services missing operational boundaries."""
    cwd = Path('.')
    all_findings = []

    for pattern in SOURCE_GLOBS:
        for file_path in cwd.glob(pattern):
            if not file_path.is_file():
                continue
            if 'node_modules' in str(file_path):
                continue

            findings = scan_file(file_path)
            all_findings.extend(findings)

    return all_findings


def create_queue(findings):
    """Create external boundary review queue."""
    queue_dir = Path('.shipkit/.queues')
    queue_dir.mkdir(parents=True, exist_ok=True)

    queue_path = queue_dir / 'ext-boundary-review.md'

    # Group by service
    by_service = {}
    for f in findings:
        service = f['service']
        if service not in by_service:
            by_service[service] = []
        by_service[service].append(f)

    content = f"""# External Service Boundary Review

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Detected by:** shipkit-detect --mode=ext-boundaries

## Why This Matters

External service calls without explicit operational boundaries (timeouts, resource
limits, error handling) work in dev but fail unpredictably in production — especially
on serverless platforms with execution time limits.

## Pending

"""

    for service, items in by_service.items():
        content += f"### {service}\n\n"
        for item in items:
            status_label = "No boundaries" if item['status'] == 'no_boundaries' else "Partial boundaries"
            content += f"- [ ] `{item['file']}` — {status_label}\n"
            if item.get('missing'):
                missing_str = ', '.join(item['missing'])
                content += f"  - Missing: {missing_str}\n"
            if item.get('found'):
                found_str = ', '.join(item['found'])
                content += f"  - Has: {found_str}\n"
        content += "\n"

    content += """## Completed

<!-- Items move here after boundaries are configured -->
"""

    queue_path.write_text(content)
    return queue_path
