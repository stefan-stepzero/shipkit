#!/usr/bin/env python3
"""
Scan for recently modified files after implementation.
Creates queues for lite-component-knowledge and lite-route-knowledge.
"""

import os
import time
from pathlib import Path
from datetime import datetime

# Time window: 60 minutes
TIME_WINDOW_SECONDS = 60 * 60

# File patterns to detect
COMPONENT_PATTERNS = [
    'src/components/**/*.tsx',
    'src/components/**/*.jsx',
    'components/**/*.tsx',
    'components/**/*.jsx',
    'app/components/**/*.tsx',
]

ROUTE_PATTERNS = [
    'src/app/**/route.ts',
    'src/app/**/route.tsx',
    'src/api/**/*.ts',
    'app/api/**/*.ts',
    'pages/api/**/*.ts',
]

HOOK_PATTERNS = [
    'src/hooks/**/*.ts',
    'src/hooks/**/*.tsx',
    'hooks/**/*.ts',
    'lib/hooks/**/*.ts',
]


def find_recent_files(patterns, cutoff_time):
    """Find files matching patterns modified after cutoff_time."""
    recent = []
    cwd = Path('.')

    for pattern in patterns:
        for file_path in cwd.glob(pattern):
            if file_path.is_file():
                mtime = os.path.getmtime(file_path)
                if mtime > cutoff_time:
                    recent.append({
                        'path': str(file_path),
                        'modified': datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M'),
                    })

    return recent


def scan():
    """Scan for recently modified files."""
    cutoff_time = time.time() - TIME_WINDOW_SECONDS

    detected = {
        'components': find_recent_files(COMPONENT_PATTERNS, cutoff_time),
        'routes': find_recent_files(ROUTE_PATTERNS, cutoff_time),
        'hooks': find_recent_files(HOOK_PATTERNS, cutoff_time),
    }

    # Only return if we found something
    if any(detected.values()):
        return detected
    return {}


def create_queue(detected):
    """Create component and route documentation queues."""
    queue_dir = Path('.shipkit-lite/.queues')
    queue_dir.mkdir(parents=True, exist_ok=True)

    created_queues = []

    # Components queue
    components = detected.get('components', []) + detected.get('hooks', [])
    if components:
        queue_path = queue_dir / 'components-to-document.md'
        content = f"""# Components To Document

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Detected by:** lite-detect --mode=changes

## Pending

"""
        for item in components:
            content += f"- [ ] `{item['path']}`\n"
            content += f"  - Modified: {item['modified']}\n"
            content += f"  - Need: Props interface, usage examples, state management docs\n\n"

        content += """## Completed

<!-- Items move here after /lite-component-knowledge documents them -->
"""
        queue_path.write_text(content)
        created_queues.append(queue_path)

    # Routes queue
    routes = detected.get('routes', [])
    if routes:
        queue_path = queue_dir / 'routes-to-document.md'
        content = f"""# Routes To Document

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Detected by:** lite-detect --mode=changes

## Pending

"""
        for item in routes:
            content += f"- [ ] `{item['path']}`\n"
            content += f"  - Modified: {item['modified']}\n"
            content += f"  - Need: Request/response schemas, auth requirements, error handling\n\n"

        content += """## Completed

<!-- Items move here after /lite-route-knowledge documents them -->
"""
        queue_path.write_text(content)
        created_queues.append(queue_path)

    # Return first queue path for consistency with other scanners
    return created_queues[0] if created_queues else None
