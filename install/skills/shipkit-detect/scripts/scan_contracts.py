#!/usr/bin/env python3
"""
Scan plans for data structure definitions.
Creates queue for shipkit-data-contracts.
"""

import os
import re
from pathlib import Path
from datetime import datetime

# Common entity names
COMMON_TYPES = ['User', 'Post', 'Comment', 'Product', 'Order', 'Session', 'Profile',
                'Account', 'Transaction', 'Invoice', 'Subscription', 'Team', 'Member']


def find_latest_plan():
    """Find most recently modified plan from todo or active folders."""
    base_dir = Path('.shipkit/plans')
    plans = []

    # Check todo and active folders (the actionable ones)
    for folder in ['todo', 'active']:
        folder_path = base_dir / folder
        if folder_path.exists():
            plans.extend(folder_path.glob('*.json'))

    # Fallback to legacy flat structure
    if not plans and base_dir.exists():
        plans = list(base_dir.glob('*.json'))

    if not plans:
        return None

    return max(plans, key=lambda p: os.path.getmtime(p))


def identify_layers(content, type_name):
    """Determine which layers mention this type."""
    content_lower = content.lower()
    type_lower = type_name.lower()
    layers = []

    # Database layer
    db_keywords = ['table', 'schema', 'sql', 'database', 'migration', 'prisma']
    if any(kw in content_lower for kw in db_keywords) and type_lower in content_lower:
        layers.append('Database')

    # API layer
    api_keywords = ['api', 'endpoint', 'route', '/api/', 'handler']
    if any(kw in content_lower for kw in api_keywords):
        layers.append('API')

    # Frontend layer
    fe_keywords = ['component', 'props', 'interface', 'frontend', 'client', 'hook']
    if any(kw in content_lower for kw in fe_keywords):
        layers.append('Frontend')

    return layers if layers else ['Unknown']


def scan():
    """Scan plan for data structure mentions."""
    plan_path = find_latest_plan()
    if not plan_path:
        return {}

    content = plan_path.read_text()

    detected = {}

    # Pattern 1: Type/Interface definitions
    type_matches = re.findall(r'(?:type|interface)\s+(\w+)', content)
    for match in type_matches:
        if match not in detected:
            detected[match] = {
                'source': str(plan_path),
                'layers': identify_layers(content, match),
            }

    # Pattern 2: Common entity names
    for entity in COMMON_TYPES:
        if entity in content and entity not in detected:
            detected[entity] = {
                'source': str(plan_path),
                'layers': identify_layers(content, entity),
            }

    return detected


def create_queue(detected):
    """Create data contracts queue."""
    queue_dir = Path('.shipkit/.queues')
    queue_dir.mkdir(parents=True, exist_ok=True)

    queue_path = queue_dir / 'define-data-contracts.md'

    content = f"""# Data Contracts To Define

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Detected by:** shipkit-detect --mode=contracts

## Pending

"""

    for type_name, info in sorted(detected.items()):
        layers_str = ' → '.join(info['layers'])
        content += f"- [ ] {type_name}\n"
        content += f"  - Mentioned in: {info['source']}\n"
        content += f"  - Layers: {layers_str}\n"
        content += f"  - Need: Consistent shape across all layers\n\n"

    content += """## Completed

<!-- Items move here after /shipkit-data-contracts validates contracts -->
"""

    queue_path.write_text(content)
    return queue_path
