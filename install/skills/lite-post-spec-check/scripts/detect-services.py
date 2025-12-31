#!/usr/bin/env python3
"""
lite-post-spec-check: Detect Services in Spec

Scans the most recent spec for external service mentions and creates
a queue file for lite-integration-docs to fetch current patterns.

Usage:
    python detect-services.py

Returns:
    0: Success (queue created or no services detected)
    1: Error (spec not found, permissions issue)
"""

import sys
from pathlib import Path
from datetime import datetime
import os

# Service detection patterns
SERVICES = {
    'stripe': ['stripe', 'payment', 'webhook', 'subscription', 'checkout', 'billing'],
    'supabase': ['supabase', 'postgres', 'rls', 'auth', 'realtime', 'storage'],
    'openai': ['openai', 'gpt', 'embedding', 'completion', 'chat', 'llm'],
    's3': ['s3', 'bucket', 'upload', 'storage', 'cloudfront', 'aws'],
    'sendgrid': ['sendgrid', 'email', 'smtp', 'transactional', 'mail'],
    'twilio': ['twilio', 'sms', 'phone', 'messaging', 'voice'],
    'clerk': ['clerk', 'authentication', 'user management', 'auth'],
    'vercel': ['vercel', 'deployment', 'edge', 'serverless'],
    'firebase': ['firebase', 'firestore', 'realtime database', 'hosting'],
    'cloudflare': ['cloudflare', 'cdn', 'workers', 'pages'],
}


def find_latest_spec():
    """Find the most recently modified spec in specs/active/"""
    specs_dir = Path('.shipkit-lite/specs/active')

    if not specs_dir.exists():
        return None

    specs = list(specs_dir.glob('*.md'))
    if not specs:
        return None

    # Return most recently modified spec
    latest = max(specs, key=lambda p: os.path.getmtime(p))
    return latest


def detect_services(spec_path):
    """Scan spec content for service keyword mentions"""
    try:
        content = spec_path.read_text(encoding='utf-8').lower()
    except Exception as e:
        print(f"❌ Error reading spec: {e}", file=sys.stderr)
        return {}

    detected = {}
    for service, keywords in SERVICES.items():
        found_keywords = [kw for kw in keywords if kw in content]
        if found_keywords:
            detected[service] = found_keywords

    return detected


def create_queue(detected_services, spec_path):
    """Create or update queue file for integration docs"""
    if not detected_services:
        print("✓ No external services detected in spec")
        return True

    # Create queue directory
    queue_dir = Path('.shipkit-lite/.queues')
    try:
        queue_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"❌ Error creating queue directory: {e}", file=sys.stderr)
        return False

    queue_path = queue_dir / 'fetch-integration-docs.md'

    # Check if queue exists and has pending items
    existing_services = set()
    if queue_path.exists():
        try:
            existing_content = queue_path.read_text(encoding='utf-8')
            # Extract existing service names from "- [ ]" lines
            for line in existing_content.split('\n'):
                if line.strip().startswith('- [ ]'):
                    # Parse service name from "- [ ] Stripe integration"
                    service_name = line.split('- [ ]')[1].strip().split()[0].lower()
                    existing_services.add(service_name)
        except Exception as e:
            print(f"⚠️  Warning: Could not read existing queue: {e}", file=sys.stderr)

    # Filter out already queued services
    new_services = {svc: kws for svc, kws in detected_services.items() if svc not in existing_services}

    if not new_services:
        print(f"✓ All {len(detected_services)} detected services already in queue")
        return True

    # Build queue content
    content = f"""# Integration Docs Needed

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Reason:** Spec mentions external services

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

    # Add new services
    for service, keywords in new_services.items():
        content += f"- [ ] {service.capitalize()} integration\n"
        content += f"  - Mentioned in: {spec_path.relative_to('.')}\n"
        content += f"  - Keywords found: {', '.join(keywords[:5])}\n"  # Max 5 keywords
        content += f"  - Need: Current best practices and patterns\n\n"

    content += """## Completed

<!-- Items move here after /lite-integration-docs fetches docs -->
"""

    # Write queue file
    try:
        queue_path.write_text(content, encoding='utf-8')
    except Exception as e:
        print(f"❌ Error writing queue file: {e}", file=sys.stderr)
        return False

    print(f"✓ Created integration docs queue with {len(new_services)} new services")
    print(f"  Total pending: {len(detected_services)} services")
    print(f"\n💡 Next: Run /lite-integration-docs to fetch current patterns")

    return True


def main():
    """Main detection logic"""
    # Find latest spec
    spec_path = find_latest_spec()
    if not spec_path:
        # No spec found - exit silently (nothing to detect)
        print("✓ No specs to scan")
        return 0

    print(f"Scanning: {spec_path.relative_to('.')}")

    # Detect services
    detected = detect_services(spec_path)

    if not detected:
        print("✓ No external services detected")
        return 0

    print(f"\nDetected {len(detected)} services:")
    for service in detected.keys():
        print(f"  - {service.capitalize()}")

    # Create queue
    success = create_queue(detected, spec_path)

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
