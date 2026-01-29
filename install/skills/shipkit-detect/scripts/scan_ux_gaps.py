#!/usr/bin/env python3
"""
Scan for interactive components needing UX review.
Creates queue for shipkit-ux-audit.
"""

import re
from pathlib import Path
from datetime import datetime

# Minimum interactive components to trigger audit
THRESHOLD = 3

# Patterns indicating interactive components
INTERACTIVE_PATTERNS = {
    'form_submit': r'onSubmit\s*[=:]|handleSubmit|formAction',
    'async_button': r'onClick\s*=\s*\{?\s*async|isLoading|isPending',
    'data_fetching': r'useQuery|useSWR|useFetch|isLoading.*\?|loading\s*\?',
    'file_upload': r'<input.*type=["\']file|useDropzone|FileUpload',
    'modal_dialog': r'<Dialog|<Modal|isOpen.*setIsOpen|showModal',
    'toast_notification': r'toast\(|useToast|notify\(',
    'optimistic_update': r'optimistic|useOptimistic',
    'infinite_scroll': r'useInfiniteQuery|loadMore|hasNextPage',
}

# Component file patterns
COMPONENT_GLOBS = [
    'src/components/**/*.tsx',
    'src/components/**/*.jsx',
    'components/**/*.tsx',
    'app/components/**/*.tsx',
]


def scan_file_for_patterns(file_path):
    """Scan a single file for interactive patterns."""
    try:
        content = file_path.read_text()
    except Exception:
        return []

    found_patterns = []
    for pattern_name, regex in INTERACTIVE_PATTERNS.items():
        if re.search(regex, content):
            found_patterns.append(pattern_name)

    return found_patterns


def scan():
    """Scan components for interactive patterns."""
    cwd = Path('.')

    detected = {}

    for pattern in COMPONENT_GLOBS:
        for file_path in cwd.glob(pattern):
            if not file_path.is_file():
                continue

            patterns_found = scan_file_for_patterns(file_path)
            if patterns_found:
                detected[str(file_path)] = {
                    'patterns': patterns_found,
                    'count': len(patterns_found),
                }

    # Only return if we hit the threshold
    if len(detected) >= THRESHOLD:
        return detected
    return {}


def create_queue(detected):
    """Create UX audit queue."""
    queue_dir = Path('.shipkit/.queues')
    queue_dir.mkdir(parents=True, exist_ok=True)

    queue_path = queue_dir / 'ux-audit-needed.md'

    # Sort by pattern count (most interactive first)
    sorted_items = sorted(detected.items(), key=lambda x: x[1]['count'], reverse=True)

    content = f"""# UX Audit Needed

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Detected by:** shipkit-detect --mode=ux-gaps
**Components found:** {len(detected)} interactive components

## Why This Matters

Interactive components need UX review for:
- Loading states and feedback
- Error handling and recovery
- Accessibility (keyboard nav, screen readers)
- Mobile responsiveness
- Edge cases (empty states, long content)

## Pending

"""

    for file_path, info in sorted_items:
        patterns_str = ', '.join(info['patterns'])
        content += f"- [ ] `{file_path}`\n"
        content += f"  - Patterns: {patterns_str}\n"
        content += f"  - Priority: {'High' if info['count'] >= 3 else 'Medium'}\n\n"

    content += """## Completed

<!-- Items move here after /shipkit-ux-audit reviews them -->
"""

    queue_path.write_text(content)
    return queue_path
