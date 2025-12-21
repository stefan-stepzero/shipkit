#!/usr/bin/env python3
"""
Generate shipkit Skills Overview HTML
Creates comprehensive reference with:
- Repository structure overview
- All ProdKit prompts embedded and browsable
- Visual pseudocode for scripts
- File references for devkit and devkit

Run from shipkit root directory:
    python generate-reference.py

Output: prodkit-references/skills-overview.html
"""

import json
from pathlib import Path
from datetime import datetime

def read_prompts(base_path):
    """Read all ProdKit skill prompt files"""
    prompts = {}
    prodkit_path = base_path / 'skills' / 'prodkit'

    # Sequential skills
    for file in sorted((prodkit_path / 'sequential').glob('*.md')):
        if file.name not in ['README.md', '_template.md']:
            prompts[file.stem] = file.read_text(encoding='utf-8')

    # Async skills
    for file in sorted((prodkit_path / 'async').glob('*.md')):
        if file.name not in ['README.md', '_template.md']:
            prompts[file.stem] = file.read_text(encoding='utf-8')

    return prompts

def generate_html(prompts, output_path):
    """Generate the comprehensive HTML reference"""

    # Start building HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>shipkit - Complete Skills Reference</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #1e293b;
            background: #f8fafc;
        }}

        .header {{
            background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
            color: white;
            padding: 60px 40px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .header h1 {{ font-size: 48px; font-weight: 700; margin-bottom: 12px; }}
        .header .subtitle {{ font-size: 20px; opacity: 0.9; }}
        .header .meta {{ margin-top: 20px; font-size: 14px; opacity: 0.8; }}

        .tabs {{
            background: white;
            border-bottom: 2px solid #e2e8f0;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}

        .tab-buttons {{
            max-width: 1600px;
            margin: 0 auto;
            display: flex;
            gap: 0;
            overflow-x: auto;
        }}

        .tab-button {{
            padding: 20px 30px;
            border: none;
            background: transparent;
            color: #64748b;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            border-bottom: 3px solid transparent;
            transition: all 0.2s;
            white-space: nowrap;
        }}

        .tab-button:hover {{ background: #f8fafc; color: #2563eb; }}
        .tab-button.active {{ color: #2563eb; border-bottom-color: #2563eb; }}

        .tab-content {{
            display: none;
            max-width: 1600px;
            margin: 40px auto;
            padding: 0 40px 80px 40px;
        }}

        .tab-content.active {{ display: block; }}

        .section {{
            background: white;
            border-radius: 12px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}

        .section-title {{
            font-size: 32px;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 20px;
        }}

        .skill-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}

        .skill-card {{
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            padding: 24px;
            cursor: pointer;
            transition: all 0.2s;
            position: relative;
        }}

        .skill-card:hover {{
            border-color: #2563eb;
            box-shadow: 0 4px 6px rgba(37, 99, 235, 0.1);
            transform: translateY(-2px);
        }}

        .skill-number {{
            position: absolute;
            top: 20px;
            right: 20px;
            width: 32px;
            height: 32px;
            background: #2563eb;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 14px;
        }}

        .skill-card-title {{
            font-size: 20px;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 12px;
            padding-right: 45px;
        }}

        .skill-card-description {{
            font-size: 14px;
            color: #64748b;
            line-height: 1.6;
        }}

        .badge {{
            display: inline-block;
            padding: 4px 10px;
            background: #dbeafe;
            color: #1e40af;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            margin-top: 12px;
        }}

        .badge.sequential {{ background: #d1fae5; color: #065f46; }}
        .badge.async {{ background: #fef3c7; color: #92400e; }}

        .modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.6);
            z-index: 2000;
            overflow-y: auto;
        }}

        .modal.active {{
            display: flex;
            align-items: flex-start;
            justify-content: center;
            padding: 40px 20px;
        }}

        .modal-content {{
            background: white;
            border-radius: 12px;
            max-width: 1000px;
            width: 100%;
            box-shadow: 0 20px 25px -5px rgba(0,0,0,0.3);
        }}

        .modal-header {{
            padding: 30px;
            border-bottom: 2px solid #e2e8f0;
            position: sticky;
            top: 0;
            background: white;
            z-index: 10;
            border-radius: 12px 12px 0 0;
        }}

        .modal-title {{
            font-size: 28px;
            font-weight: 700;
            color: #0f172a;
            padding-right: 40px;
        }}

        .modal-close {{
            position: absolute;
            right: 30px;
            top: 30px;
            font-size: 32px;
            font-weight: bold;
            cursor: pointer;
            color: #64748b;
            line-height: 1;
        }}

        .modal-close:hover {{ color: #0f172a; }}

        .modal-body {{
            padding: 30px;
            max-height: calc(90vh - 200px);
            overflow-y: auto;
        }}

        .prompt-content {{
            background: #0f172a;
            color: #e2e8f0;
            padding: 30px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.8;
            white-space: pre-wrap;
            word-wrap: break-word;
            overflow-x: auto;
        }}

        .button-row {{
            display: flex;
            gap: 12px;
            margin-top: 20px;
        }}

        .btn {{
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.2s;
        }}

        .btn-primary {{
            background: #2563eb;
            color: white;
        }}

        .btn-primary:hover {{ background: #1e40af; }}

        .btn-secondary {{
            background: #f1f5f9;
            color: #475569;
        }}

        .btn-secondary:hover {{ background: #e2e8f0; }}

        .tree-item {{
            font-family: 'Courier New', monospace;
            padding: 4px 0;
            color: #475569;
            font-size: 14px;
        }}

        .tree-item.folder {{ color: #2563eb; font-weight: 600; }}
        .indent-1 {{ padding-left: 24px; }}
        .indent-2 {{ padding-left: 48px; }}
        .indent-3 {{ padding-left: 72px; }}

        .script-flow {{
            background: #f8fafc;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
        }}

        .script-title {{
            font-size: 24px;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 24px;
            font-family: 'Courier New', monospace;
        }}

        .flow-step {{
            position: relative;
            padding: 20px 20px 20px 50px;
            background: white;
            border-left: 4px solid #2563eb;
            margin-bottom: 20px;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}

        .flow-step-number {{
            position: absolute;
            left: -18px;
            top: 20px;
            width: 36px;
            height: 36px;
            background: #2563eb;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 16px;
            box-shadow: 0 2px 4px rgba(37, 99, 235, 0.3);
        }}

        .flow-step-title {{
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 8px;
            font-size: 16px;
        }}

        .flow-step-content {{
            color: #475569;
            line-height: 1.6;
        }}

        .flow-params {{
            background: #fffbeb;
            border: 1px solid #fef3c7;
            padding: 15px;
            border-radius: 6px;
            margin-top: 15px;
        }}

        .flow-params-title {{
            font-weight: 700;
            color: #92400e;
            font-size: 12px;
            text-transform: uppercase;
            margin-bottom: 10px;
        }}

        .flow-param {{
            font-family: 'Courier New', monospace;
            font-size: 13px;
            color: #78350f;
            margin: 6px 4px;
            padding: 4px 8px;
            background: #fef9c3;
            border-radius: 3px;
            display: inline-block;
        }}

        .flow-output {{
            background: #ecfdf5;
            border: 1px solid #d1fae5;
            padding: 15px;
            border-radius: 6px;
            margin-top: 15px;
        }}

        .flow-output-title {{
            font-weight: 700;
            color: #065f46;
            font-size: 12px;
            text-transform: uppercase;
            margin-bottom: 10px;
        }}

        .flow-output-file {{
            font-family: 'Courier New', monospace;
            font-size: 14px;
            color: #064e3b;
            padding: 4px 8px;
            background: #d1fae5;
            border-radius: 3px;
            display: inline-block;
            margin: 4px 4px 4px 0;
        }}

        @media (max-width: 768px) {{
            .skill-grid {{ grid-template-columns: 1fr; }}
            .tab-buttons {{ overflow-x: scroll; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>shipkit</h1>
        <div class="subtitle">Complete Product Development Framework</div>
        <div class="meta">Generated {datetime.now().strftime("%Y-%m-%d %H:%M")}</div>
    </div>

    <div class="tabs">
        <div class="tab-buttons">
            <button class="tab-button active" onclick="switchTab('overview')">Overview</button>
            <button class="tab-button" onclick="switchTab('prodkit')">ProdKit Prompts (11)</button>
            <button class="tab-button" onclick="switchTab('scripts')">Scripts (Visual)</button>
            <button class="tab-button" onclick="switchTab('other')">devkit & devkit</button>
        </div>
    </div>

    <!-- OVERVIEW TAB -->
    <div class="tab-content active" id="overview">
        <div class="section">
            <h2 class="section-title">Repository Structure</h2>
            <div class="tree-item folder">shipkit/</div>
            <div class="tree-item file indent-1">├── install.sh</div>
            <div class="tree-item file indent-1">├── README.md</div>
            <div class="tree-item folder indent-1">├── agents/ - 5 agent personas</div>
            <div class="tree-item folder indent-1">├── skills/ - Claude Code skills</div>
            <div class="tree-item folder indent-2">│   ├── devkit/ - 10 skills (includes constitution-builder)</div>
            <div class="tree-item folder indent-2">│   ├── devkit/</div>
            <div class="tree-item folder indent-3">│   │   ├── essential/ - 8 skills (brainstorming is async)</div>
            <div class="tree-item folder indent-3">│   │   └── advanced/ - 5 skills</div>
            <div class="tree-item folder indent-2">│   └── prodkit/</div>
            <div class="tree-item folder indent-3">│       ├── sequential/ - 9 workflow skills</div>
            <div class="tree-item folder indent-3">│       └── async/ - 2 anytime skills</div>
            <div class="tree-item folder indent-1">├── devkit-files/scripts/bash/</div>
            <div class="tree-item folder indent-1">├── prodkit-files/scripts/bash/</div>
            <div class="tree-item folder indent-1">└── help/</div>
            <div class="tree-item file indent-2">    └── skills-overview.html</div>
        </div>

        <div class="section">
            <h2 class="section-title">What is shipkit?</h2>
            <p style="font-size: 16px; color: #475569; margin-bottom: 20px; line-height: 1.8;">
                <strong>Claude Code skills + Agent Personas</strong> for end-to-end product development
            </p>
            <ul style="padding-left: 24px; color: #475569; font-size: 16px; line-height: 2;">
                <li><strong>devkit (10)</strong> - Technical specification pipeline (/implement integrates TDD, reviews)</li>
                <li><strong>devkit (13)</strong> - Quality & workflow enhancements (key skills integrated into /implement)</li>
                <li><strong>ProdKit (11)</strong> - Product discovery & strategy (/brainstorming is async)</li>
                <li><strong>Agent Personas (5)</strong> - Discovery, Architect, Implementer, Reviewer, Researcher</li>
            </ul>
        </div>

        <div class="section">
            <h2 class="section-title">How to Use This Reference</h2>
            <p style="font-size: 16px; color: #475569; line-height: 1.8;">
                <strong>ProdKit Prompts:</strong> Browse all 11 skills. Click to view full prompt content for discussing changes.<br><br>
                <strong>Scripts:</strong> Visual pseudocode showing what each script does.<br><br>
                <strong>Other:</strong> File paths for devkit and devkit.
            </p>
        </div>
    </div>

    <!-- PRODKIT PROMPTS TAB -->
    <div class="tab-content" id="prodkit">
        <div class="section">
            <h2 class="section-title">Sequential Workflow (Steps 1-9)</h2>
            <div class="skill-grid">
'''

    # Add sequential skill cards
    seq_skills = [
        ("1-strategic-thinking", "Strategic Thinking", "Business strategy using Playing to Win + Lean Canvas"),
        ("2-personas", "Personas", "Target user demographics, goals, pain points"),
        ("3-jobs-to-be-done", "Jobs-to-be-Done", "Current state AS-IS analysis"),
        ("4-market-analysis", "Market Analysis", "Porter's Five Forces"),
        ("5-brand-guidelines", "Brand Guidelines", "Visual direction, personality, patterns"),
        ("6-interaction-design", "Interaction Design", "Future state TO-BE journeys"),
        ("7-user-stories", "User Stories", "Requirements with MoSCoW prioritization"),
        ("8-assumptions-and-risks", "Assumptions and Risks", "Strategic risk identification"),
        ("9-success-metrics", "Success Metrics", "KPIs, AARRR framework, instrumentation"),
    ]

    for skill_id, title, desc in seq_skills:
        step_num = skill_id.split('-')[0]
        html += f'''                <div class="skill-card" onclick="showPrompt('{skill_id}')">
                    <div class="skill-number">{step_num}</div>
                    <div class="skill-card-title">{title}</div>
                    <div class="skill-card-description">{desc}</div>
                    <span class="badge sequential">Sequential</span>
                </div>
'''

    html += '''            </div>
        </div>

        <div class="section">
            <h2 class="section-title">Async Skills</h2>
            <div class="skill-grid">
'''

    # Add async skill cards
    async_skills = [
        ("trade-off-analysis", "Trade-Off Analysis", "Feature prioritization, ROI, build/defer/cut"),
        ("communicator", "Communicator", "Generate stakeholder HTML communications"),
    ]

    for skill_id, title, desc in async_skills:
        html += f'''                <div class="skill-card" onclick="showPrompt('{skill_id}')">
                    <div class="skill-card-title">{title}</div>
                    <div class="skill-card-description">{desc}</div>
                    <span class="badge async">Async</span>
                </div>
'''

    html += '''            </div>
        </div>
    </div>

    <!-- SCRIPTS TAB -->
    <div class="tab-content" id="scripts">
        <div class="section">
            <h2 class="section-title">ProdKit Scripts - Visual Pseudocode</h2>
            <p style="margin-bottom: 30px; color: #64748b;">Scripts enforce consistency using templates and validation</p>

            <div class="script-flow">
                <div class="script-title">create-strategy.sh</div>
                <div class="flow-step">
                    <div class="flow-step-number">1</div>
                    <div class="flow-step-title">Accept Parameters</div>
                    <div class="flow-step-content">Parse 14 command-line parameters</div>
                    <div class="flow-params">
                        <div class="flow-params-title">Parameters</div>
                        <span class="flow-param">--winning-aspiration</span>
                        <span class="flow-param">--where-to-play</span>
                        <span class="flow-param">--how-to-win</span>
                        <span class="flow-param">--capabilities</span>
                        <span class="flow-param">--systems</span>
                        <span class="flow-param">--problem</span>
                        <span class="flow-param">--segments</span>
                        <span class="flow-param">--value-prop</span>
                        <span class="flow-param">--solution</span>
                        <span class="flow-param">--channels</span>
                        <span class="flow-param">--revenue</span>
                        <span class="flow-param">--costs</span>
                        <span class="flow-param">--metrics</span>
                        <span class="flow-param">--unfair-advantage</span>
                    </div>
                </div>
                <div class="flow-step">
                    <div class="flow-step-number">2</div>
                    <div class="flow-step-title">Validate</div>
                    <div class="flow-step-content">Ensure required fields exist</div>
                </div>
                <div class="flow-step">
                    <div class="flow-step-number">3</div>
                    <div class="flow-step-title">Create Directory</div>
                    <div class="flow-step-content">mkdir -p .prodkit/strategy</div>
                </div>
                <div class="flow-step">
                    <div class="flow-step-number">4</div>
                    <div class="flow-step-title">Use Template or Generate</div>
                    <div class="flow-step-content">Apply template if exists, otherwise create structured markdown</div>
                    <div class="flow-output">
                        <div class="flow-output-title">Outputs</div>
                        <span class="flow-output-file">.prodkit/strategy/business-canvas.md</span>
                        <span class="flow-output-file">.prodkit/strategy/value-proposition.md</span>
                    </div>
                </div>
            </div>

            <div class="script-flow">
                <div class="script-title">All Other Scripts Follow Similar Patterns</div>
                <div class="flow-step">
                    <div class="flow-step-number">▶</div>
                    <div class="flow-step-title">Common Flow</div>
                    <div class="flow-step-content">
                        1. Accept parameters<br>
                        2. Validate required fields<br>
                        3. Create directory<br>
                        4. Use template or generate markdown<br>
                        5. Write to .prodkit/ structure
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- OTHER TAB -->
    <div class="tab-content" id="other">
        <div class="section">
            <h2 class="section-title">devkit (9) & devkit (13)</h2>
            <p style="margin-bottom: 20px; color: #64748b;">File locations:</p>
            <div style="font-family: 'Courier New', monospace; color: #475569; line-height: 2; font-size: 14px;">
                skills/devkit/*.md (9 files)<br>
                skills/devkit/essential/*.md (8 files)<br>
                skills/devkit/advanced/*.md (5 files)
            </div>
        </div>
    </div>

    <!-- MODAL -->
    <div id="promptModal" class="modal" onclick="closeModal(event)">
        <div class="modal-content" onclick="event.stopPropagation()">
            <div class="modal-header">
                <span class="modal-close" onclick="closeModal()">&times;</span>
                <div class="modal-title" id="modalTitle"></div>
            </div>
            <div class="modal-body">
                <pre class="prompt-content" id="promptContent"></pre>
                <div class="button-row">
                    <button class="btn btn-primary" onclick="copyPrompt()">Copy Prompt</button>
                    <button class="btn btn-secondary" onclick="copyFilePath()">Copy File Path</button>
                    <button class="btn btn-secondary" onclick="closeModal()">Close</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Embedded prompts
        const PROMPTS = ''' + json.dumps(prompts, indent=8) + ''';

        function switchTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));

            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }

        let currentSkillId = '';

        function showPrompt(skillId) {
            const modal = document.getElementById('promptModal');
            const title = document.getElementById('modalTitle');
            const content = document.getElementById('promptContent');

            currentSkillId = skillId;
            title.textContent = skillId.replace(/-/g, ' ').replace(/\\b\\w/g, l => l.toUpperCase());
            content.textContent = PROMPTS[skillId] || 'Prompt not found';

            modal.classList.add('active');
        }

        function closeModal(event) {
            if (!event || event.target.classList.contains('modal') || event.target.classList.contains('modal-close')) {
                document.getElementById('promptModal').classList.remove('active');
            }
        }

        function copyPrompt() {
            const content = document.getElementById('promptContent').textContent;
            navigator.clipboard.writeText(content).then(() => {
                const btn = event.target;
                btn.textContent = 'Copied!';
                btn.style.background = '#10b981';
                setTimeout(() => {
                    btn.textContent = 'Copy Prompt';
                    btn.style.background = '#2563eb';
                }, 2000);
            });
        }

        function copyFilePath() {
            let path = '';
            if (currentSkillId && currentSkillId.includes('-')) {
                const num = currentSkillId.split('-')[0];
                path = !isNaN(num) ?
                    `skills/prodkit/sequential/${{currentSkillId}}.md` :
                    `skills/prodkit/async/${{currentSkillId}}.md`;
            }

            navigator.clipboard.writeText(path).then(() => {
                const btn = event.target;
                btn.textContent = 'Copied Path!';
                btn.style.background = '#10b981';
                setTimeout(() => {
                    btn.textContent = 'Copy File Path';
                    btn.style.background = '#f1f5f9';
                }, 2000);
            });
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') closeModal();
        });
    </script>
</body>
</html>
'''

    # Write the file
    output_path.write_text(html, encoding='utf-8')
    print(f"[OK] Generated {output_path}")
    print(f"     Size: {len(html):,} characters")
    print(f"     Prompts embedded: {len(prompts)}")

def main():
    """Main execution"""
    # Go up one level from help/ to the repo root
    base_path = Path(__file__).parent.parent

    print("ShipKit Skills Overview Generator")
    print("=" * 50)

    # Read prompts
    print("\nReading ProdKit prompts...")
    prompts = read_prompts(base_path)
    print(f"  Found {len(prompts)} skills")

    # Generate HTML
    output_path = base_path / 'prodkit-references' / 'skills-overview.html'
    output_path.parent.mkdir(exist_ok=True)

    print(f"\nGenerating HTML...")
    generate_html(prompts, output_path)

    print(f"\n[OK] Complete!")
    print(f"\nOpen: {output_path}")

if __name__ == '__main__':
    main()
