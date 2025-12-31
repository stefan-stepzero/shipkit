#!/usr/bin/env python3
"""
lite-milestone-detector: Route to Detection Check

Detects which workflow milestone was just completed and routes to
the appropriate detection skill to create bug-prevention queues.

Triggered by: Stop hook (receives JSON via stdin)

Hook Input (JSON via stdin):
    {
      "session_id": "...",
      "transcript_path": "...",
      "stop_hook_active": true/false,
      ...
    }

Usage:
    python route-to-check.py

Returns:
    0: Success (detection skill invoked or no milestone detected)
    1: Error
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
import subprocess
import os

# Time window for detecting recent file changes
RECENT_MINUTES = 2


def detect_milestone():
    """Detect which workflow milestone just occurred"""
    now = datetime.now()
    recent_threshold = timedelta(minutes=RECENT_MINUTES)

    # Check for new/modified spec (highest priority if multiple detected)
    specs_dir = Path('.shipkit-lite/specs/active')
    if specs_dir.exists():
        specs = list(specs_dir.glob('*.md'))
        for spec in specs:
            try:
                mtime = datetime.fromtimestamp(os.path.getmtime(spec))
                if now - mtime < recent_threshold:
                    return 'post-spec', spec
            except Exception:
                pass

    # Check for new/modified plan
    plans_dir = Path('.shipkit-lite/plans')
    if plans_dir.exists():
        plans = list(plans_dir.glob('*.md'))
        for plan in plans:
            try:
                mtime = datetime.fromtimestamp(os.path.getmtime(plan))
                if now - mtime < recent_threshold:
                    return 'post-plan', plan
            except Exception:
                pass

    # Check for implementation (modified source files)
    src_patterns = [
        'src/**/*.ts',
        'src/**/*.tsx',
        'src/**/*.jsx',
        'src/**/*.js',
        'app/**/*.ts',
        'app/**/*.tsx',
    ]

    implementation_detected = False
    for pattern in src_patterns:
        for file_path in Path('.').glob(pattern):
            try:
                mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                if now - mtime < recent_threshold:
                    implementation_detected = True
                    break
            except Exception:
                pass
        if implementation_detected:
            break

    if implementation_detected:
        return 'post-implement', None

    # No milestone detected
    return None, None


def invoke_detection_skill(milestone, context_file):
    """Invoke the appropriate detection skill"""
    skill_map = {
        'post-spec': ('lite-post-spec-check', 'scripts/detect-services.py'),
        'post-plan': ('lite-post-plan-check', 'scripts/detect-data-structures.py'),
        'post-implement': ('lite-post-implement-check', 'scripts/detect-changes.py'),
    }

    if milestone not in skill_map:
        return False

    skill_name, script_path = skill_map[milestone]
    full_script_path = Path('.claude/skills') / skill_name / script_path

    # Check if script exists
    if not full_script_path.exists():
        print(f"⚠️  Detection script not found: {full_script_path}", file=sys.stderr)
        return False

    # Run detection script
    try:
        result = subprocess.run(
            ['python', str(full_script_path)],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Print script output
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print(result.stderr, file=sys.stderr)

        return result.returncode == 0

    except subprocess.TimeoutExpired:
        print(f"❌ Detection script timed out: {skill_name}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ Error running detection script: {e}", file=sys.stderr)
        return False


def main():
    """Main coordination logic"""
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        # If no JSON input (testing), continue anyway
        hook_input = {}
    except Exception:
        hook_input = {}

    # Prevent infinite loops: Exit if stop hook already active
    if hook_input.get('stop_hook_active'):
        return 0

    # Detect milestone
    milestone, context_file = detect_milestone()

    if milestone is None:
        # No milestone detected - exit silently (this is normal)
        return 0

    # Invoke appropriate detection skill
    success = invoke_detection_skill(milestone, context_file)

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
