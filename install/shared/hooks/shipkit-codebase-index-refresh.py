#!/usr/bin/env python3
"""
Shipkit - Codebase Index Refresh Hook

Deterministic (no-LLM) freshness for .shipkit/codebase-index.json.

Wired as a PostToolUse hook scoped to `git commit` (if:"Bash(git commit *)") and
also invoked from session-start. It is a THIN wrapper: it locates the index
generator and runs it in --refresh-mechanical mode, which refreshes only the
script-owned mechanical fields and preserves the Claude-judgment fields.

Design contract:
- Never raises, always exits 0 (a refresh failure must never break a commit/turn).
- Early-exits silently when there is no git repo, no existing index, or no generator.
- Idempotent and fork-safe (the generator writes atomically); PostToolUse hooks
  fire at every fork depth, so this may run concurrently — that is tolerated.
"""

import os
import subprocess
import sys
from pathlib import Path

HOOK_NAME = "codebase-index-refresh"


def _resolve_root(project_dir: str) -> str | None:
    """Repo root via git, anchored at the session's project dir."""
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=project_dir or None,
            capture_output=True, text=True, timeout=10,
        )
        root = out.stdout.strip()
        return root or None
    except Exception:
        return None


def _find_generator(root: str) -> Path | None:
    """generate_index.py at project scope first, then user scope (~/.claude)."""
    candidates = [
        Path(root) / ".claude" / "skills" / "shipkit-codebase-index" / "scripts" / "generate_index.py",
        Path.home() / ".claude" / "skills" / "shipkit-codebase-index" / "scripts" / "generate_index.py",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def main() -> int:
    # Drain stdin (the hook payload) so we never block the caller; we don't need it
    # — the if:"Bash(git commit *)" matcher already scopes when we fire.
    try:
        sys.stdin.read()
    except Exception:
        pass

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "") or os.getcwd()

    root = _resolve_root(project_dir)
    if not root:
        return 0

    # No index yet → nothing to keep fresh (the full skill run owns creation).
    if not (Path(root) / ".shipkit" / "codebase-index.json").exists():
        return 0

    gen = _find_generator(root)
    if gen is None:
        return 0

    try:
        subprocess.run(
            [sys.executable, "-X", "utf8", str(gen), "--refresh-mechanical"],
            cwd=root, capture_output=True, text=True, timeout=30,
        )
    except Exception:
        pass  # best-effort; never break the commit/turn
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"[shipkit:{HOOK_NAME}] ERROR: {e}", file=sys.stderr)
        sys.exit(0)
