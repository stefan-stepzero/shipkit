#!/usr/bin/env python3
"""
Installer smoke test for Shipkit.

Runs `node cli/bin/shipkit.js init -y --target <tempdir>` into an isolated
temp directory and asserts invariants on the generated settings.json:

  1. File exists and is valid JSON.
  2. Every hook event declared in install/settings/shipkit.settings.json
     also exists in the generated file (no silently dropped events).
  3. Every command-type hook in the generated file uses $CLAUDE_PROJECT_DIR/
     (catches the v2.4.4 regression where hand-maintained JS duplicated paths).
  4. Skill() allow-list count matches the manifest skill count.

Exits 0 on pass, 1 on fail. Prints a structured report suitable for the
framework-integrity aggregator.

Invoked from shipkit-framework-integrity Step 0.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def find_package_root() -> Path:
    """Walk upward from this script to find the repo root (contains cli/bin/shipkit.js)."""
    here = Path(__file__).resolve()
    for parent in [here, *here.parents]:
        if (parent / "cli" / "bin" / "shipkit.js").is_file():
            return parent
    sys.exit("ERROR: could not locate Shipkit repo root from script path")


def iter_command_hooks(hooks_obj: dict):
    """Yield (event_name, command_string) for every command-type hook."""
    for event, entries in (hooks_obj or {}).items():
        if not isinstance(entries, list):
            continue
        for entry in entries:
            for hook in entry.get("hooks", []) or []:
                if hook.get("type") == "command" and isinstance(hook.get("command"), str):
                    yield event, hook["command"]


def count_manifest_skills(manifest: dict) -> int:
    skills = manifest.get("skills") or {}
    mandatory = skills.get("mandatory") or []
    optional = skills.get("optional") or {}
    total = len(mandatory)
    for category in optional.values():
        total += len(category or [])
    return total


def run_installer(package_root: Path, target: Path) -> tuple[int, str]:
    cli = package_root / "cli" / "bin" / "shipkit.js"
    proc = subprocess.run(
        ["node", str(cli), "init", "-y", "--target", str(target)],
        cwd=str(package_root),
        capture_output=True,
        text=True,
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def main() -> int:
    package_root = find_package_root()
    canonical_path = package_root / "install" / "settings" / "shipkit.settings.json"
    manifest_path = package_root / "install" / "profiles" / "shipkit.manifest.json"

    if not canonical_path.is_file():
        print(f"FAIL: canonical settings missing at {canonical_path}")
        return 1
    if not manifest_path.is_file():
        print(f"FAIL: manifest missing at {manifest_path}")
        return 1

    canonical = json.loads(canonical_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected_skill_count = count_manifest_skills(manifest)

    canonical_events = set((canonical.get("hooks") or {}).keys())
    canonical_command_events = {
        event for event, _cmd in iter_command_hooks(canonical.get("hooks") or {})
    }

    tempdir = Path(tempfile.mkdtemp(prefix="shipkit-smoke-"))
    errors: list[str] = []
    try:
        rc, output = run_installer(package_root, tempdir)
        if rc != 0:
            errors.append(f"installer exited with code {rc}")
            tail = "\n".join(output.splitlines()[-15:])
            errors.append(f"installer tail output:\n{tail}")
            return _report(errors, {})

        settings_path = tempdir / ".claude" / "settings.json"
        if not settings_path.is_file():
            errors.append(f"settings.json not generated at {settings_path}")
            return _report(errors, {})

        try:
            generated = json.loads(settings_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"generated settings.json is not valid JSON: {exc}")
            return _report(errors, {})

        generated_hooks = generated.get("hooks") or {}
        generated_events = set(generated_hooks.keys())

        missing_events = sorted(canonical_events - generated_events)
        if missing_events:
            errors.append(
                "events dropped during install: " + ", ".join(missing_events)
            )

        bad_paths: list[str] = []
        for event, cmd in iter_command_hooks(generated_hooks):
            if "$CLAUDE_PROJECT_DIR/" not in cmd:
                bad_paths.append(f"{event}: {cmd}")
        if bad_paths:
            errors.append(
                "command hooks missing $CLAUDE_PROJECT_DIR/ prefix:\n  - "
                + "\n  - ".join(bad_paths)
            )

        missing_command_events = sorted(
            canonical_command_events - {
                event for event, _ in iter_command_hooks(generated_hooks)
            }
        )
        if missing_command_events:
            errors.append(
                "command hooks dropped for events: "
                + ", ".join(missing_command_events)
            )

        allow = (generated.get("permissions") or {}).get("allow") or []
        skill_entries = [p for p in allow if isinstance(p, str) and p.startswith("Skill(")]
        if len(skill_entries) != expected_skill_count:
            errors.append(
                f"Skill() allow-list count {len(skill_entries)} != manifest skill count {expected_skill_count}"
            )

        stats = {
            "command_hooks": sum(1 for _ in iter_command_hooks(generated_hooks)),
            "hook_events": len(generated_events),
            "skill_entries": len(skill_entries),
            "expected_skills": expected_skill_count,
        }
        return _report(errors, stats)

    finally:
        shutil.rmtree(tempdir, ignore_errors=True)


def _report(errors: list[str], stats: dict) -> int:
    print("INSTALLER_SMOKE_TEST:")
    if stats:
        print(f"  command_hooks:  {stats.get('command_hooks', 0)}")
        print(f"  hook_events:    {stats.get('hook_events', 0)}")
        print(f"  skill_entries:  {stats.get('skill_entries', 0)} (expected {stats.get('expected_skills', 0)})")
    if errors:
        print("  status: FAIL")
        for err in errors:
            print(f"  - {err}")
        return 1
    print("  status: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
