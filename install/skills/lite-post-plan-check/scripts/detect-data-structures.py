#!/usr/bin/env python3
"""
lite-post-plan-check: Detect Data Structures in Plan

Scans the most recent plan for data structure definitions and creates
a queue file for lite-data-contracts to validate contracts across layers.

Usage:
    python detect-data-structures.py

Returns:
    0: Success (queue created or no data structures detected)
    1: Error (plan not found, permissions issue)
"""

import sys
from pathlib import Path
from datetime import datetime
import os
import re

# Common data types that often need contracts
COMMON_TYPES = ['User', 'Post', 'Comment', 'Product', 'Order', 'Session', 'Profile', 'Message', 'Notification']


def find_latest_plan():
    """Find the most recently modified plan in plans/"""
    plans_dir = Path('.shipkit-lite/plans')

    if not plans_dir.exists():
        return None

    plans = list(plans_dir.glob('*.md'))
    if not plans:
        return None

    # Return most recently modified plan
    latest = max(plans, key=lambda p: os.path.getmtime(p))
    return latest


def detect_data_structures(plan_path):
    """Scan plan content for data structure definitions"""
    try:
        content = plan_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"❌ Error reading plan: {e}", file=sys.stderr)
        return set(), ""

    detected_types = set()

    # Pattern 1: TypeScript type/interface definitions
    type_matches = re.findall(r'(?:type|interface)\s+(\w+)', content)
    detected_types.update(type_matches)

    # Pattern 2: Database tables (CREATE TABLE, schema references)
    table_matches = re.findall(r'CREATE TABLE\s+(\w+)', content, re.IGNORECASE)
    # Convert snake_case table names to PascalCase (users → User)
    for table in table_matches:
        pascal_case = ''.join(word.capitalize() for word in table.split('_'))
        detected_types.add(pascal_case)

    # Pattern 3: API route patterns (/api/users, /api/posts)
    api_matches = re.findall(r'/api/(\w+)', content, re.IGNORECASE)
    for api_entity in api_matches:
        # Singularize and capitalize (users → User, posts → Post)
        singular = api_entity.rstrip('s').capitalize()
        detected_types.add(singular)

    # Pattern 4: Common entity names mentioned in plan
    for common_type in COMMON_TYPES:
        # Check for exact word match (not substring)
        if re.search(r'\b' + common_type + r'\b', content):
            detected_types.add(common_type)

    return detected_types, content


def identify_layers(plan_content, type_name):
    """Determine which layers mention this type"""
    layers = []
    content_lower = plan_content.lower()
    type_lower = type_name.lower()

    # Check for database mentions
    db_keywords = ['table', 'schema', 'sql', 'database', 'migration', 'create table']
    if any(keyword in content_lower for keyword in db_keywords):
        # Check if this type is mentioned near database keywords
        if type_lower in content_lower:
            layers.append('Database')

    # Check for API/backend mentions
    api_keywords = ['api', 'endpoint', 'route', '/api/', 'get /', 'post /']
    if any(keyword in content_lower for keyword in api_keywords):
        layers.append('Backend API')

    # Check for frontend mentions
    frontend_keywords = ['component', 'props', 'interface', 'frontend', 'ui', 'react', 'vue']
    if any(keyword in content_lower for keyword in frontend_keywords):
        layers.append('Frontend')

    return layers


def create_queue(detected_types, plan_path, plan_content):
    """Create or update queue file for data contracts"""
    if not detected_types:
        print("✓ No data structures detected in plan")
        return True

    # Create queue directory
    queue_dir = Path('.shipkit-lite/.queues')
    try:
        queue_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"❌ Error creating queue directory: {e}", file=sys.stderr)
        return False

    queue_path = queue_dir / 'define-data-contracts.md'

    # Check if queue exists and has pending items
    existing_types = set()
    if queue_path.exists():
        try:
            existing_content = queue_path.read_text(encoding='utf-8')
            # Extract existing type names from "- [ ]" lines
            for line in existing_content.split('\n'):
                if line.strip().startswith('- [ ]'):
                    # Parse type name from "- [ ] User"
                    type_name = line.split('- [ ]')[1].strip().split('\n')[0]
                    existing_types.add(type_name)
        except Exception as e:
            print(f"⚠️  Warning: Could not read existing queue: {e}", file=sys.stderr)

    # Filter out already queued types
    new_types = detected_types - existing_types

    if not new_types:
        print(f"✓ All {len(detected_types)} detected types already in queue")
        return True

    # Build queue content
    content = f"""# Data Contracts To Define

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Reason:** Plan defines data structures

## Pending

"""

    # If queue exists, append to existing pending items
    if queue_path.exists():
        try:
            existing_content = queue_path.read_text(encoding='utf-8')
            # Extract pending section
            if '## Pending' in existing_content:
                pending_section = existing_content.split('## Pending')[1].split('## Completed')[0]
                # Add existing pending items
                content += pending_section.strip() + '\n\n'
        except Exception:
            pass  # If parsing fails, just create fresh queue

    # Add new types
    for type_name in sorted(new_types):
        layers = identify_layers(plan_content, type_name)
        layers_str = ' → '.join(layers) if layers else 'Unknown layers (needs investigation)'

        content += f"- [ ] {type_name}\n"
        content += f"  - Mentioned in: {plan_path.relative_to('.')}\n"
        content += f"  - Layers: {layers_str}\n"
        content += f"  - Contract needed: Define consistent shape across all layers\n\n"

    content += """## Completed

<!-- Items move here after /lite-data-contracts validates contracts -->
"""

    # Write queue file
    try:
        queue_path.write_text(content, encoding='utf-8')
    except Exception as e:
        print(f"❌ Error writing queue file: {e}", file=sys.stderr)
        return False

    print(f"✓ Created data contracts queue with {len(new_types)} new types")
    print(f"  Total pending: {len(detected_types)} types")
    print(f"\n💡 Next: Run /lite-data-contracts to validate contracts across layers")

    return True


def main():
    """Main detection logic"""
    # Find latest plan
    plan_path = find_latest_plan()
    if not plan_path:
        # No plan found - exit silently (nothing to detect)
        print("✓ No plans to scan")
        return 0

    print(f"Scanning: {plan_path.relative_to('.')}")

    # Detect data structures
    detected, plan_content = detect_data_structures(plan_path)

    if not detected:
        print("✓ No data structures detected")
        return 0

    print(f"\nDetected {len(detected)} data types:")
    for type_name in sorted(detected):
        layers = identify_layers(plan_content, type_name)
        print(f"  - {type_name} ({', '.join(layers) if layers else 'layers TBD'})")

    # Create queue
    success = create_queue(detected, plan_path, plan_content)

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
