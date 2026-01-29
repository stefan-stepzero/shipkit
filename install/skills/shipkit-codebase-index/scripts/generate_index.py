#!/usr/bin/env python3
"""
Generate base codebase index for Claude Code.
Outputs to .shipkit/codebase-index.json

This script ONLY does what it can do 100% reliably:
- Git history (recently modified files)
- Package.json scripts
- List existing directories
- List existing config files

Claude handles all the ambiguous stuff:
- Framework detection
- Concept mappings
- Core files identification
- Directory purposes
"""

import json
import os
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

OUTPUT_PATH = '.shipkit/codebase-index.json'
SOURCE_EXTENSIONS = {'.ts', '.tsx', '.js', '.jsx', '.py', '.go', '.rs', '.vue', '.svelte'}
EXCLUDE_DIRS = {'node_modules', 'dist', '.next', '__pycache__', '.git', 'venv', '.venv', 'build', 'out'}


def run_git(args):
    """Run git command and return output."""
    try:
        result = subprocess.run(
            ['git'] + args,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8',
            errors='replace'
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return ''
    except FileNotFoundError:
        return ''


def get_recently_active(root, days=14, limit=15):
    """Get recently modified files from git. This is 100% reliable."""
    since = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    output = run_git(['log', f'--since={since}', '--name-only', '--pretty=format:'])

    if not output:
        return []

    counts = defaultdict(int)
    for line in output.strip().split('\n'):
        line = line.strip()
        if not line or line.startswith(' '):
            continue

        file_path = Path(root) / line
        if file_path.exists() and Path(line).suffix in SOURCE_EXTENSIONS:
            if not any(excl in Path(line).parts for excl in EXCLUDE_DIRS):
                counts[line] += 1

    sorted_files = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return [f for f, _ in sorted_files[:limit]]


def parse_scripts(root):
    """Parse scripts from package.json. This is 100% reliable."""
    pkg_path = Path(root) / 'package.json'
    if not pkg_path.exists():
        return {}

    try:
        data = json.loads(pkg_path.read_text(encoding='utf-8'))
        return data.get('scripts', {})
    except (json.JSONDecodeError, IOError):
        return {}


def list_directories(root):
    """List existing directories (not their purpose - Claude does that)."""
    root_path = Path(root)
    dirs = []

    # Check common directory patterns
    candidates = [
        'src', 'src/app', 'src/pages', 'src/components', 'src/lib', 'src/utils',
        'src/services', 'src/hooks', 'src/types', 'src/api', 'src/styles',
        'app', 'pages', 'components', 'lib', 'utils',
        'prisma', 'supabase', 'drizzle',
        'public', 'static', 'assets',
        'tests', '__tests__', 'test', 'spec',
        'scripts', 'tools', 'bin',
        'docs', 'documentation',
        'config', 'configs',
    ]

    for candidate in candidates:
        if (root_path / candidate).is_dir():
            dirs.append(candidate)

    return dirs


def list_config_files(root):
    """List existing config files (Claude uses these to detect framework)."""
    root_path = Path(root)
    configs = []

    candidates = [
        # JS/TS frameworks
        'next.config.js', 'next.config.mjs', 'next.config.ts',
        'vite.config.ts', 'vite.config.js',
        'remix.config.js',
        'astro.config.mjs', 'astro.config.ts',
        'svelte.config.js',
        'nuxt.config.ts', 'nuxt.config.js',
        'gatsby-config.js', 'gatsby-config.ts',
        # Build tools
        'webpack.config.js', 'rollup.config.js', 'esbuild.config.js',
        'turbo.json',
        # Package managers
        'package.json', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'bun.lockb',
        # TypeScript
        'tsconfig.json', 'jsconfig.json',
        # Linting/Formatting
        'eslint.config.js', '.eslintrc.js', '.eslintrc.json',
        'prettier.config.js', '.prettierrc',
        'biome.json',
        # Testing
        'vitest.config.ts', 'jest.config.js', 'playwright.config.ts',
        # Database
        'prisma/schema.prisma',
        'drizzle.config.ts',
        # Python
        'pyproject.toml', 'setup.py', 'requirements.txt',
        # Go
        'go.mod', 'go.sum',
        # Rust
        'Cargo.toml',
        # Docker
        'Dockerfile', 'docker-compose.yml', 'docker-compose.yaml',
        # CI/CD
        '.github/workflows', '.gitlab-ci.yml',
        # Misc
        'tailwind.config.js', 'tailwind.config.ts',
        'postcss.config.js',
        '.env.example', '.env.local.example',
    ]

    for candidate in candidates:
        path = root_path / candidate
        if path.exists():
            configs.append(candidate)

    return configs


def generate_index():
    """Generate the base codebase index."""
    root = run_git(['rev-parse', '--show-toplevel']).strip()
    if not root:
        print("Error: Not a git repository")
        return 1

    root = root.replace('/', os.sep)
    os.chdir(root)

    print("Generating codebase index (base data)...")

    index = {
        'generated': datetime.now().strftime('%Y-%m-%d'),

        # === SCRIPT FILLS THESE (100% reliable) ===
        'scripts': parse_scripts(root),
        'recentlyActive': get_recently_active(root),
        'directories': list_directories(root),
        'configFiles': list_config_files(root),

        # === CLAUDE FILLS THESE (requires judgment) ===
        'framework': '',        # Claude detects from configFiles
        'entryPoints': {},      # Claude identifies
        'concepts': {},         # Claude maps
        'coreFiles': [],        # Claude identifies
        'skip': [],             # User/Claude decides
    }

    output_dir = Path(OUTPUT_PATH).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2)

    print(f"✅ Base index created at {OUTPUT_PATH}")
    print(f"   Scripts: {len(index['scripts'])}")
    print(f"   Recently active: {len(index['recentlyActive'])} files")
    print(f"   Directories: {len(index['directories'])}")
    print(f"   Config files: {len(index['configFiles'])}")
    print()
    print("📋 Claude will now analyze this and add:")
    print("   - Framework detection")
    print("   - Entry points")
    print("   - Concept mappings (auth, database, etc.)")
    print("   - Core files")

    return 0


if __name__ == '__main__':
    sys.exit(generate_index())
