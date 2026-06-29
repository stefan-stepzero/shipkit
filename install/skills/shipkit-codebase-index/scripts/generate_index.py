#!/usr/bin/env python3
"""
Generate / refresh the codebase index for Claude Code.
Outputs to .shipkit/codebase-index.json

Two modes:

  (default / full)        python generate_index.py
      Rebuilds the base index: the script fills the 100%-reliable MECHANICAL
      fields and leaves the judgment fields empty for Claude to complete.
      Sets both timestamps and seeds the hash-cache.

  --refresh-mechanical    python generate_index.py --refresh-mechanical
      DETERMINISTIC, NO LLM. Refreshes ONLY the mechanical fields and preserves
      the Claude-judgment fields (framework/entryPoints/concepts/coreFiles/skip)
      byte-for-byte. Skips writing entirely when nothing source-relevant changed
      (content-hash cache). Never creates a partial index — if no index exists,
      it exits 0 and does nothing. This is what the commit hook + SessionStart run.

The script ONLY computes what it can do 100% reliably:
- Git history (recently modified files)
- package.json scripts
- Which common directories exist
- Which config files exist

Claude handles the ambiguous fields (framework, concepts, coreFiles, ...) — those
are refreshed only by a full run inside the /shipkit-codebase-index skill.
"""

import hashlib
import json
import os
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

OUTPUT_PATH = '.shipkit/codebase-index.json'
CACHE_PATH = '.shipkit/cache/codebase-index.cache.json'
CACHE_DIR = '.shipkit/cache'

SOURCE_EXTENSIONS = {'.ts', '.tsx', '.js', '.jsx', '.py', '.go', '.rs', '.vue', '.svelte'}
EXCLUDE_DIRS = {'node_modules', 'dist', '.next', '__pycache__', '.git', 'venv', '.venv', 'build', 'out'}

# Fields the script owns and may overwrite on a mechanical refresh.
MECHANICAL_FIELDS = ('scripts', 'recentlyActive', 'directories', 'configFiles')
# Fields that require Claude — a mechanical refresh must NEVER touch these.
JUDGMENT_FIELDS = ('framework', 'entryPoints', 'concepts', 'coreFiles', 'skip')


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


def build_mechanical(root):
    """Compute the four mechanical fields (100% reliable, no judgment)."""
    return {
        'scripts': parse_scripts(root),
        'recentlyActive': get_recently_active(root),
        'directories': list_directories(root),
        'configFiles': list_config_files(root),
    }


# ─── Incremental change detection (content-hash cache) ──────────────────────

def _iter_source_files(root):
    """Yield POSIX-relative paths of tracked-shape source files, excluding heavy dirs."""
    root_path = Path(root)
    for dirpath, dirnames, filenames in os.walk(root_path):
        # prune excluded dirs in place (also skips dotdirs like .git/.venv listed above)
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for name in filenames:
            if Path(name).suffix in SOURCE_EXTENSIONS:
                rel = Path(dirpath, name).relative_to(root_path).as_posix()
                yield rel


def compute_source_digest(root):
    """Deterministic digest of everything the mechanical fields derive from.

    Captures: source-file contents (add/remove/edit), the structural shape
    (which dirs/config files exist), and package.json scripts. Deliberately
    EXCLUDES recentlyActive (time-windowed — it drifts without a real change,
    and is cheap to recompute when something else moves).
    """
    h = hashlib.sha256()
    for rel in sorted(_iter_source_files(root)):
        h.update(rel.encode('utf-8'))
        h.update(b'\0')
        try:
            with open(Path(root) / rel, 'rb') as f:
                h.update(hashlib.sha256(f.read()).digest())
        except OSError:
            h.update(b'<unreadable>')
        h.update(b'\n')
    # Structural shape: a new dir or config file must bust the cache even if no
    # source file changed (e.g. adding tsconfig.json or a prisma/ folder).
    h.update(json.dumps(list_directories(root), sort_keys=True).encode('utf-8'))
    h.update(json.dumps(list_config_files(root), sort_keys=True).encode('utf-8'))
    h.update(json.dumps(parse_scripts(root), sort_keys=True).encode('utf-8'))
    return h.hexdigest()


def read_cache(root):
    cache_file = Path(root) / CACHE_PATH
    if not cache_file.exists():
        return None
    try:
        return json.loads(cache_file.read_text(encoding='utf-8')).get('sourceDigest')
    except Exception:
        return None


def write_cache(root, digest):
    cache_dir = Path(root) / CACHE_DIR
    cache_dir.mkdir(parents=True, exist_ok=True)
    payload = {'sourceDigest': digest, 'computedAt': datetime.now().isoformat()}
    _atomic_write_json(Path(root) / CACHE_PATH, payload)


def ensure_cache_gitignore(root):
    """Self-ignore the cache regardless of install age.

    The installed .gitignore is only created at install time (copy-if-not-exists),
    so editing the template won't reach existing projects. Writing this keeps the
    machine-specific cache out of git everywhere. .shipkit/ content is otherwise
    intentionally committed (it's the user's context).
    """
    cache_dir = Path(root) / CACHE_DIR
    cache_dir.mkdir(parents=True, exist_ok=True)
    gi = cache_dir / '.gitignore'
    if not gi.exists():
        try:
            gi.write_text('*\n', encoding='utf-8')
        except OSError:
            pass


# ─── Atomic write (fork-safe: PostToolUse hooks fire at every fork depth) ────

def _atomic_write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + f'.tmp.{os.getpid()}')
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, path)  # atomic on POSIX and Windows


# ─── Modes ──────────────────────────────────────────────────────────────────

def generate_full(root):
    """Rebuild the base index; leave judgment fields empty for Claude."""
    print("Generating codebase index (base data)...")
    now = datetime.now().strftime('%Y-%m-%d')

    index = {
        'generated': now,
        'fullRefreshedAt': now,
        'mechanicalRefreshedAt': now,
    }
    index.update(build_mechanical(root))
    # Judgment fields — Claude fills these in the skill flow.
    index.update({
        'framework': '',
        'entryPoints': {},
        'concepts': {},
        'coreFiles': [],
        'skip': [],
    })

    _atomic_write_json(Path(root) / OUTPUT_PATH, index)
    ensure_cache_gitignore(root)
    write_cache(root, compute_source_digest(root))

    print(f"OK Base index created at {OUTPUT_PATH}")
    print(f"   Scripts: {len(index['scripts'])}")
    print(f"   Recently active: {len(index['recentlyActive'])} files")
    print(f"   Directories: {len(index['directories'])}")
    print(f"   Config files: {len(index['configFiles'])}")
    print()
    print("Claude will now analyze this and add:")
    print("   - Framework detection")
    print("   - Entry points")
    print("   - Concept mappings (auth, database, etc.)")
    print("   - Core files")
    return 0


def refresh_mechanical(root):
    """Deterministic refresh of mechanical fields only. No LLM. No partial creation."""
    index_path = Path(root) / OUTPUT_PATH
    if not index_path.exists():
        # Never create a partial index from the hook — a full skill run owns creation.
        print("No codebase-index.json yet — nothing to refresh (run /shipkit-codebase-index).")
        return 0

    digest = compute_source_digest(root)
    if read_cache(root) == digest:
        print("Codebase index up to date (no source change) — skipped.")
        return 0

    try:
        existing = json.loads(index_path.read_text(encoding='utf-8'))
        if not isinstance(existing, dict):
            raise ValueError("index is not an object")
    except Exception as e:
        print(f"Existing index unreadable ({e}) — leaving it untouched.")
        return 0

    # Refresh mechanical fields; preserve judgment fields byte-for-byte.
    existing.update(build_mechanical(root))
    existing['mechanicalRefreshedAt'] = datetime.now().strftime('%Y-%m-%d')
    # Back-compat: pre-existing indexes won't have fullRefreshedAt. Seed it from
    # `generated` so the SessionStart staleness check has something to key off.
    if 'fullRefreshedAt' not in existing:
        existing['fullRefreshedAt'] = existing.get('generated', existing['mechanicalRefreshedAt'])

    _atomic_write_json(index_path, existing)
    ensure_cache_gitignore(root)
    write_cache(root, digest)
    print(f"OK Codebase index mechanical fields refreshed ({existing['mechanicalRefreshedAt']}).")
    return 0


def main(argv):
    root = run_git(['rev-parse', '--show-toplevel']).strip()
    if not root:
        print("Error: Not a git repository")
        return 1
    root = root.replace('/', os.sep)
    os.chdir(root)

    if '--refresh-mechanical' in argv:
        return refresh_mechanical(root)
    return generate_full(root)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
