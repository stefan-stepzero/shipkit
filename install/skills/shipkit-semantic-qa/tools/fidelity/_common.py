#!/usr/bin/env python3
"""
_common.py - Shared helpers for the fidelity checker CLIs.

Provides a gitignore-ish source-file walker used by mock-seam-detector,
unbacked-surface-checker, and ssot-checker. Not a CLI itself.
"""

import os
from pathlib import Path

# Directories we never descend into (build output, deps, VCS, caches).
SKIP_DIRS = {
    "node_modules", ".git", "dist", "build", ".next", "out", "coverage",
    "__pycache__", ".venv", "venv", "env", ".turbo", ".cache", ".parcel-cache",
    ".vercel", ".svelte-kit", "vendor", ".pytest_cache", ".mypy_cache",
    "storybook-static", "public", ".idea", ".vscode",
    ".claude", ".shipkit",
}

# Source extensions we scan. Deliberately code-only (no .md/.json/.lock).
CODE_EXTS = {
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs",
    ".vue", ".svelte", ".py", ".sql", ".astro",
}

# Skip obvious non-hand-written / generated / minified files.
SKIP_FILE_SUFFIXES = (".min.js", ".min.css", ".d.ts", ".bundle.js")


def _is_skip_dir(name):
    """True if a directory should never be descended into.

    Covers the explicit SKIP_DIRS set plus build-output variants that use a
    suffixed name (e.g. Next.js `.next-e2e`, `.next-test`) which would otherwise
    leak minified chunks / generated route types into the scan.
    """
    if name in SKIP_DIRS:
        return True
    if name.startswith(".next"):  # .next, .next-e2e, .next-test, ...
        return True
    return False


def iter_source_files(root):
    """Yield Path objects for hand-written source files under root.

    Respects SKIP_DIRS (gitignore-ish) and CODE_EXTS. Symlinks not followed.
    """
    root = Path(root)
    for dirpath, dirnames, filenames in os.walk(root):
        # Prune skip dirs in-place so os.walk does not descend into them.
        dirnames[:] = [d for d in dirnames if not _is_skip_dir(d)]
        for fn in filenames:
            if any(fn.endswith(sfx) for sfx in SKIP_FILE_SUFFIXES):
                continue
            ext = os.path.splitext(fn)[1].lower()
            if ext in CODE_EXTS:
                yield Path(dirpath) / fn


def read_lines(path):
    """Read a file as a list of lines; returns [] on any read error."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read().splitlines()
    except Exception:
        return []


def rel(path, root):
    """Best-effort POSIX-style path relative to root for stable output."""
    try:
        return Path(path).relative_to(root).as_posix()
    except Exception:
        return Path(path).as_posix()
