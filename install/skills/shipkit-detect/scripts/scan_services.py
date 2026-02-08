#!/usr/bin/env python3
"""
Scan specs for external service mentions.
Creates queue for shipkit-integration-docs.
"""

import os
from pathlib import Path
from datetime import datetime

# Service keywords to detect
SERVICES = {
    'lemonsqueezy': ['lemon squeezy', 'lemonsqueezy', 'payment', 'webhook', 'subscription', 'checkout', 'billing'],
    'stripe': ['stripe', 'payment intent', 'checkout session'],
    'supabase': ['supabase', 'postgres', 'rls', 'realtime', 'supabase auth'],
    'prisma': ['prisma', 'orm', 'migration', 'schema.prisma'],
    'openai': ['openai', 'gpt-4', 'gpt-3', 'embedding', 'completion', 'chat completion'],
    'anthropic': ['anthropic', 'claude', 'claude-3'],
    's3': ['s3', 'bucket', 'aws s3', 'cloudfront'],
    'r2': ['cloudflare r2', 'r2 bucket'],
    'resend': ['resend', 'transactional email', 'react email'],
    'sendgrid': ['sendgrid', 'email api'],
    'clerk': ['clerk', '@clerk/nextjs', 'clerk auth'],
    'nextauth': ['next-auth', 'nextauth', 'authjs'],
    'vercel': ['vercel', 'edge function', 'vercel ai'],
    'upstash': ['upstash', 'redis', 'qstash', 'ratelimit'],
}


def find_latest_spec():
    """Find most recently modified spec from todo or active folders."""
    base_dir = Path('.shipkit/specs')
    specs = []

    # Check todo and active folders (the actionable ones)
    for folder in ['todo', 'active']:
        folder_path = base_dir / folder
        if folder_path.exists():
            specs.extend(folder_path.glob('*.json'))

    # Fallback to legacy flat structure
    if not specs and base_dir.exists():
        specs = list(base_dir.glob('*.json'))

    if not specs:
        return None

    return max(specs, key=lambda p: os.path.getmtime(p))


def scan():
    """Scan spec for service mentions."""
    spec_path = find_latest_spec()
    if not spec_path:
        return {}

    content = spec_path.read_text().lower()

    detected = {}
    for service, keywords in SERVICES.items():
        found_keywords = [kw for kw in keywords if kw in content]
        if found_keywords:
            detected[service] = {
                'keywords': found_keywords,
                'source': str(spec_path),
            }

    return detected


def create_queue(detected):
    """Create integration docs queue."""
    queue_dir = Path('.shipkit/.queues')
    queue_dir.mkdir(parents=True, exist_ok=True)

    queue_path = queue_dir / 'fetch-integration-docs.md'

    content = f"""# Integration Docs Needed

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Detected by:** shipkit-detect --mode=services

## Pending

"""

    for service, info in detected.items():
        content += f"- [ ] {service.capitalize()}\n"
        content += f"  - Mentioned in: {info['source']}\n"
        content += f"  - Keywords: {', '.join(info['keywords'])}\n"
        content += f"  - Need: Current API patterns and best practices\n\n"

    content += """## Completed

<!-- Items move here after /shipkit-integration-docs fetches docs -->
"""

    queue_path.write_text(content)
    return queue_path
