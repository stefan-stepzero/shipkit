#!/usr/bin/env python3
"""
lite-post-implement-check: Detect Implementation Changes

Scans for recently modified components, routes, and service integrations
after implementation completes. Creates documentation queues.

Usage:
    python detect-changes.py [--since-minutes 60]

Returns:
    0: Success
    1: Error
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import os
import argparse

# File patterns to scan
COMPONENT_PATTERNS = [
    'src/components/**/*.tsx',
    'src/components/**/*.jsx',
    'app/components/**/*.tsx',
    'components/**/*.tsx',
]

ROUTE_PATTERNS = [
    'src/app/**/route.ts',
    'src/app/**/route.js',
    'app/api/**/route.ts',
    'src/api/**/*.ts',
]

SERVICE_PATTERNS = {
    'stripe': ['from "stripe"', "from 'stripe'"],
    'supabase': ['from "@supabase/supabase-js"', "from '@supabase/supabase-js'"],
    'openai': ['from "openai"', "from 'openai'"],
    's3': ['from "@aws-sdk/client-s3"'],
    'sendgrid': ['from "@sendgrid/mail"'],
}


def find_modified_files(patterns, since_minutes):
    """Find files matching patterns modified in last N minutes"""
    cutoff = datetime.now() - timedelta(minutes=since_minutes)
    modified = []

    for pattern in patterns:
        for file_path in Path('.').glob(pattern):
            if file_path.is_file():
                mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                if mtime > cutoff:
                    modified.append((file_path, mtime))

    return modified


def detect_service_usage(file_path):
    """Detect which services are imported in a file"""
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception:
        return []

    detected = []
    for service, patterns in SERVICE_PATTERNS.items():
        if any(pattern in content for pattern in patterns):
            detected.append(service)

    return detected


def create_components_queue(components):
    """Create queue for component documentation"""
    if not components:
        return False

    queue_dir = Path('.shipkit-lite/.queues')
    queue_dir.mkdir(parents=True, exist_ok=True)
    queue_path = queue_dir / 'components-to-document.md'

    content = f"""# Components To Document

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Reason:** New/modified components detected after implementation

## Pending

"""

    for file_path, mtime in sorted(components, key=lambda x: x[1], reverse=True):
        component_name = file_path.stem
        content += f"- [ ] {file_path}\n"
        content += f"  - Modified: {mtime.strftime('%Y-%m-%d %H:%M')}\n"
        content += f"  - Type: Component\n"
        content += f"  - Needs: Props contract, usage examples\n\n"

    content += """## Completed

<!-- Items move here after /lite-component-knowledge documents components -->
"""

    queue_path.write_text(content, encoding='utf-8')
    print(f"✓ Created components queue with {len(components)} items")
    return True


def create_routes_queue(routes):
    """Create queue for route documentation"""
    if not routes:
        return False

    queue_dir = Path('.shipkit-lite/.queues')
    queue_dir.mkdir(parents=True, exist_ok=True)
    queue_path = queue_dir / 'routes-to-document.md'

    content = f"""# Routes To Document

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Reason:** New/modified routes detected after implementation

## Pending

"""

    for file_path, mtime in sorted(routes, key=lambda x: x[1], reverse=True):
        # Try to determine HTTP methods from file
        try:
            route_content = file_path.read_text(encoding='utf-8')
            methods = []
            if 'export async function GET' in route_content or 'export function GET' in route_content:
                methods.append('GET')
            if 'export async function POST' in route_content or 'export function POST' in route_content:
                methods.append('POST')
            if 'export async function PUT' in route_content or 'export function PUT' in route_content:
                methods.append('PUT')
            if 'export async function DELETE' in route_content or 'export function DELETE' in route_content:
                methods.append('DELETE')
            methods_str = ', '.join(methods) if methods else 'Unknown'
        except Exception:
            methods_str = 'Unknown'

        content += f"- [ ] {file_path}\n"
        content += f"  - Modified: {mtime.strftime('%Y-%m-%d %H:%M')}\n"
        content += f"  - Methods: {methods_str}\n"
        content += f"  - Needs: Request/response schemas, auth requirements\n\n"

    content += """## Completed

<!-- Items move here after /lite-route-knowledge documents routes -->
"""

    queue_path.write_text(content, encoding='utf-8')
    print(f"✓ Created routes queue with {len(routes)} items")
    return True


def create_integrations_queue(integrations):
    """Create queue for service integration verification"""
    if not integrations:
        return False

    queue_dir = Path('.shipkit-lite/.queues')
    queue_dir.mkdir(parents=True, exist_ok=True)
    queue_path = queue_dir / 'integrations-used.md'

    content = f"""# Service Integrations Detected

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Reason:** Service imports found in recent code changes

## Pending Review

"""

    for file_path, services in integrations:
        for service in services:
            content += f"- [ ] {service.capitalize()}\n"
            content += f"  - Detected in: {file_path}\n"
            content += f"  - Check needed: Verify patterns match current best practices\n\n"

    content += """## Verified Correct

<!-- Items move here after /lite-integration-docs verifies patterns -->
"""

    queue_path.write_text(content, encoding='utf-8')
    total_services = sum(len(services) for _, services in integrations)
    print(f"✓ Created integrations queue with {total_services} service usages")
    return True


def main():
    parser = argparse.ArgumentParser(description='Detect implementation changes')
    parser.add_argument('--since-minutes', type=int, default=60,
                        help='Check files modified in last N minutes (default: 60)')
    args = parser.parse_args()

    print(f"Scanning for changes in last {args.since_minutes} minutes...")

    # Find modified components
    components = find_modified_files(COMPONENT_PATTERNS, args.since_minutes)
    if components:
        print(f"\nFound {len(components)} modified components")
        create_components_queue(components)

    # Find modified routes
    routes = find_modified_files(ROUTE_PATTERNS, args.since_minutes)
    if routes:
        print(f"\nFound {len(routes)} modified routes")
        create_routes_queue(routes)

    # Detect service integrations
    all_files = components + routes
    integrations = []
    for file_path, _ in all_files:
        services = detect_service_usage(file_path)
        if services:
            integrations.append((file_path, services))

    if integrations:
        print(f"\nFound {len(integrations)} files with service integrations")
        create_integrations_queue(integrations)

    # Summary
    total = len(components) + len(routes)
    if total > 0:
        print(f"\n💡 Next steps:")
        if components:
            print(f"  - Run /lite-component-knowledge to document {len(components)} components")
        if routes:
            print(f"  - Run /lite-route-knowledge to document {len(routes)} routes")
        if integrations:
            print(f"  - Run /lite-integration-docs to verify integration patterns")
    else:
        print("\n✓ No recent changes detected")

    return 0


if __name__ == '__main__':
    sys.exit(main())
