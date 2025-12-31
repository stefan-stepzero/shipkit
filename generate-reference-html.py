#!/usr/bin/env python3
"""
Generate detailed reference HTML from skill profiles
"""

import json
from pathlib import Path

def generate_skill_profile_html(skill_name: str, profile: dict) -> str:
    """Generate HTML for a single skill profile"""

    auto_queue_badge = ''
    if profile.get('auto_queue'):
        auto_queue_badge = '<span class="auto-badge">🤖 Auto-Queue</span>'

    # Trigger keywords
    keywords_html = ''
    if profile['triggers']['keywords']:
        keywords = profile['triggers']['keywords'][:10]  # Limit to 10
        keywords_html = ', '.join(f'<code>{k}</code>' for k in keywords)

    # Process steps
    steps_html = ''
    if profile['process_steps']:
        steps_items = '\n'.join(f'<li>{step}</li>' for step in profile['process_steps'])
        steps_html = f'<ol class="process-steps">{steps_items}</ol>'

    # Auto-queue info
    auto_queue_html = ''
    if profile.get('auto_queue'):
        aq = profile['auto_queue']
        auto_queue_html = f'''
        <div class="profile-section">
            <h4>🤖 Auto-Detection</h4>
            <p><strong>Queue File:</strong> <code>.shipkit-lite/.queues/{aq['queue_file']}</code></p>
            <p><strong>Mode:</strong> Automatically processes pending items when queue exists, falls back to manual mode if no queue.</p>
        </div>
        '''

    html = f'''
    <div class="skill-profile" id="{skill_name}">
        <h3>/{skill_name} {auto_queue_badge}</h3>
        <p class="skill-desc">{profile['description']}</p>

        <div class="profile-section">
            <h4>🎯 Trigger Keywords</h4>
            <p>{keywords_html if keywords_html else '<em>See SKILL.md for manual invocation</em>'}</p>
        </div>

        {auto_queue_html}

        <div class="profile-section">
            <h4>⚙️ Key Process Steps</h4>
            {steps_html if steps_html else '<p><em>See SKILL.md for detailed process</em></p>'}
        </div>
    </div>
    '''

    return html

def generate_trigger_flows_html() -> str:
    """Generate trigger flow diagrams"""
    html = '''
    <div class="section">
        <h2>🔄 Automatic Trigger Flows</h2>
        <p class="section-intro">These diagrams show how detection skills automatically create queues when milestones are reached.</p>

        <h3>Flow 1: Spec → Integration Docs</h3>
        <div class="mermaid">
graph LR
    A[👤 User creates spec<br/>mentioning Stripe] --> B[⚡ Stop Hook fires]
    B --> C[🎯 lite-milestone-detector<br/>detects new spec]
    C --> D[🔍 lite-post-spec-check<br/>scans for services]
    D --> E[📝 Creates queue:<br/>fetch-integration-docs.md]
    E --> F[🧠 lite-whats-next<br/>suggests skill]
    F --> G[👤 User runs<br/>/lite-integration-docs]
    G --> H[📚 Fetches Stripe docs<br/>to references/]
    H --> I[✅ Queue updated:<br/>Pending → Completed]
        </div>

        <h3>Flow 2: Plan → Data Contracts</h3>
        <div class="mermaid">
graph LR
    A[👤 User creates plan<br/>with User type] --> B[⚡ Stop Hook fires]
    B --> C[🎯 lite-milestone-detector<br/>detects new plan]
    C --> D[🔍 lite-post-plan-check<br/>scans for types]
    D --> E[📝 Creates queue:<br/>define-data-contracts.md]
    E --> F[🧠 lite-whats-next<br/>suggests skill]
    F --> G[👤 User runs<br/>/lite-data-contracts]
    G --> H[✔️ Validates contracts<br/>across layers]
    H --> I[✅ Queue updated:<br/>Pending → Completed]
        </div>

        <h3>Flow 3: Implementation → Component Docs</h3>
        <div class="mermaid">
graph LR
    A[👤 User implements<br/>LoginForm component] --> B[⚡ Stop Hook fires]
    B --> C[🎯 lite-milestone-detector<br/>detects file changes]
    C --> D[🔍 lite-post-implement-check<br/>finds new component]
    D --> E[📝 Creates queue:<br/>components-to-document.md]
    E --> F[🧠 lite-whats-next<br/>suggests skill]
    F --> G[👤 User runs<br/>/lite-component-knowledge]
    G --> H[📋 Documents props,<br/>state, events]
    H --> I[✅ Queue updated:<br/>Pending → Completed]
        </div>
    </div>
    '''

    return html

def generate_system_skills_html() -> str:
    """Generate system skills documentation"""
    html = '''
    <div class="section">
        <h2>🔧 Hidden System Skills</h2>
        <p class="section-intro">These skills run automatically in the background. You never invoke them directly.</p>

        <div class="system-skill-card">
            <h3>lite-milestone-detector</h3>
            <p><strong>Purpose:</strong> Coordinator that detects which workflow milestone just completed</p>
            <p><strong>Triggered:</strong> Stop hook after ANY skill completes</p>
            <p><strong>Detection Logic:</strong> Checks file modification times in last 2 minutes in .shipkit-lite/</p>
            <p><strong>Routes To:</strong></p>
            <ul>
                <li>New spec in <code>specs/active/</code> → lite-post-spec-check</li>
                <li>New plan in <code>plans/</code> → lite-post-plan-check</li>
                <li>Modified files in <code>src/</code> or <code>app/</code> → lite-post-implement-check</li>
            </ul>
        </div>

        <div class="system-skill-card">
            <h3>lite-post-spec-check</h3>
            <p><strong>Purpose:</strong> Scans spec for external service mentions</p>
            <p><strong>Detects:</strong> Stripe, Supabase, OpenAI, S3, SendGrid, Twilio, Clerk, Vercel, Firebase, Cloudflare</p>
            <p><strong>Creates:</strong> <code>.queues/fetch-integration-docs.md</code></p>
            <p><strong>Detection Pattern:</strong> 5-6 keywords per service (case-insensitive)</p>
        </div>

        <div class="system-skill-card">
            <h3>lite-post-plan-check</h3>
            <p><strong>Purpose:</strong> Scans plan for data structure definitions</p>
            <p><strong>Detects:</strong> TypeScript types, database tables, API contracts</p>
            <p><strong>Creates:</strong> <code>.queues/define-data-contracts.md</code></p>
            <p><strong>Detection Pattern:</strong> Regex for type/interface, CREATE TABLE, common entity names</p>
        </div>

        <div class="system-skill-card">
            <h3>lite-post-implement-check</h3>
            <p><strong>Purpose:</strong> Scans for new/modified components and routes</p>
            <p><strong>Detects:</strong> Files modified in last 60 minutes in src/ or app/</p>
            <p><strong>Creates:</strong> <code>.queues/components-to-document.md</code>, <code>.queues/routes-to-document.md</code></p>
            <p><strong>Detection Pattern:</strong> File patterns (**/*.tsx, **/route.ts) + modification time</p>
        </div>

        <div class="system-skill-card">
            <h3>lite-pre-ship-check</h3>
            <p><strong>Purpose:</strong> Determines if UX audit needed before shipping</p>
            <p><strong>Detects:</strong> Interactive component patterns (forms, async buttons, data widgets, file uploads, modals)</p>
            <p><strong>Creates:</strong> <code>.queues/ux-audit-needed.md</code> when 3+ interactive components found</p>
            <p><strong>Threshold:</strong> 3 interactive components triggers UX audit</p>
        </div>
    </div>
    '''

    return html

# Main execution
if __name__ == '__main__':
    # Load profiles
    with open('skill-profiles.json') as f:
        profiles = json.load(f)

    # Generate trigger flows
    trigger_flows = generate_trigger_flows_html()

    # Generate system skills
    system_skills = generate_system_skills_html()

    # Generate skill profiles
    profiles_html = []
    for skill_name in sorted(profiles.keys()):
        profile = profiles[skill_name]
        profiles_html.append(generate_skill_profile_html(skill_name, profile))

    # Combine all
    reference_content = f'''
    <div id="reference-tab" class="tab-content">
        <h1>Technical Reference Guide</h1>
        <p class="intro">Comprehensive developer reference for all Shipkit Lite skills, trigger flows, and automation infrastructure.</p>

        {trigger_flows}

        {system_skills}

        <div class="section">
            <h2>📚 Complete Skill Profiles</h2>
            <p class="section-intro">Detailed information for all 23 user-facing skills.</p>
            <div class="skills-reference">
                {''.join(profiles_html)}
            </div>
        </div>
    </div>
    '''

    # Save
    output = Path('reference-tab-content.html')
    output.write_text(reference_content, encoding='utf-8')

    print(f'[OK] Generated reference tab content')
    print(f'[OK] Saved to: {output}')
    print(f'[OK] Profiles: {len(profiles)}')
    print(f'[OK] Trigger flows: 3')
    print(f'[OK] System skills: 5')
