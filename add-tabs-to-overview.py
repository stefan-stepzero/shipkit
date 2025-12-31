#!/usr/bin/env python3
"""
Add tabbed interface to shipkit-lite-overview.html
"""
from pathlib import Path

# Read files
overview_path = Path('help/shipkit-lite-overview.html')
reference_path = Path('reference-tab-content.html')

overview_html = overview_path.read_text(encoding='utf-8')
reference_html = reference_path.read_text(encoding='utf-8')

# Tab CSS to add to the style section
tab_css = """
        /* Tab Navigation */
        .tab-nav {
            background: #f8fafc;
            border-bottom: 2px solid #e2e8f0;
            padding: 0 40px;
            display: flex;
            gap: 0;
            position: sticky;
            top: 0;
            z-index: 1000;
        }

        .tab-button {
            background: transparent;
            border: none;
            padding: 20px 30px;
            font-size: 1.1em;
            font-weight: 600;
            color: #64748b;
            cursor: pointer;
            border-bottom: 3px solid transparent;
            transition: all 0.3s ease;
        }

        .tab-button:hover {
            background: #f1f5f9;
            color: #475569;
        }

        .tab-button.active {
            color: #667eea;
            border-bottom-color: #667eea;
            background: white;
        }

        .tab-content {
            display: none;
            animation: fadeIn 0.3s ease;
        }

        .tab-content.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        /* Reference Tab Styles */
        .skills-reference {
            display: grid;
            gap: 30px;
        }

        .skill-profile {
            background: #f8fafc;
            border-radius: 12px;
            padding: 30px;
            border-left: 4px solid #667eea;
        }

        .skill-profile h3 {
            color: #667eea;
            font-size: 1.8em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .auto-badge {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 0.5em;
            font-weight: 600;
        }

        .skill-desc {
            font-size: 1.1em;
            color: #475569;
            margin-bottom: 25px;
        }

        .profile-section {
            margin: 20px 0;
        }

        .profile-section h4 {
            color: #475569;
            font-size: 1.3em;
            margin-bottom: 10px;
        }

        .process-steps {
            margin-left: 20px;
        }

        .process-steps li {
            margin: 8px 0;
            color: #64748b;
        }

        .system-skill-card {
            background: #fef3c7;
            border-radius: 12px;
            padding: 25px;
            margin: 20px 0;
            border-left: 4px solid #f59e0b;
        }

        .system-skill-card h3 {
            color: #d97706;
            margin-bottom: 15px;
        }

        .system-skill-card ul {
            margin-left: 20px;
        }

        .section-intro {
            font-size: 1.2em;
            color: #64748b;
            text-align: center;
            margin-bottom: 30px;
        }

        .intro {
            font-size: 1.3em;
            color: #64748b;
            text-align: center;
            margin-bottom: 40px;
        }
"""

# Tab navigation HTML
tab_nav = """
        <!-- Tab Navigation -->
        <div class="tab-nav">
            <button class="tab-button active" onclick="switchTab('overview')">Quick Overview</button>
            <button class="tab-button" onclick="switchTab('reference')">Technical Reference</button>
        </div>
"""

# Tab switching JavaScript
tab_js = """
    <script>
        function switchTab(tabName) {
            // Hide all tab contents
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });

            // Deactivate all tab buttons
            document.querySelectorAll('.tab-button').forEach(button => {
                button.classList.remove('active');
            });

            // Show selected tab
            document.getElementById(tabName + '-tab').classList.add('active');

            // Activate selected button
            event.target.classList.add('active');
        }
    </script>
"""

# Insert tab CSS before the closing </style> tag
overview_html = overview_html.replace('</style>', tab_css + '\n    </style>')

# Insert tab navigation after the </header> tag
overview_html = overview_html.replace('</header>', '</header>\n' + tab_nav)

# Wrap existing content in Tab 1
# Find the <div class="content"> opening tag
content_start = overview_html.find('<div class="content">')
content_start_end = overview_html.find('>', content_start) + 1

# Find the closing </div> for content (before footer)
footer_start = overview_html.find('<footer>')
content_end = overview_html.rfind('</div>', 0, footer_start)

# Extract the existing content between
existing_content = overview_html[content_start_end:content_end].strip()

# Build new content structure with tabs
new_content = f'''
        <div class="content">
            <!-- Tab 1: Overview -->
            <div id="overview-tab" class="tab-content active">
{existing_content}
            </div>

            <!-- Tab 2: Reference -->
            {reference_html}
        </div>
'''

# Replace old content section with new tabbed structure
overview_html = overview_html[:content_start] + new_content + overview_html[content_end + 6:]

# Add tab switching JavaScript before closing </body>
overview_html = overview_html.replace('</body>', tab_js + '\n</body>')

# Write updated HTML
overview_path.write_text(overview_html, encoding='utf-8')

print('[OK] Added tabbed interface to overview HTML')
print('[OK] Tab 1: Quick Overview (existing content)')
print('[OK] Tab 2: Technical Reference (23 skills, trigger flows, system skills)')
print(f'[OK] Saved to: {overview_path}')
