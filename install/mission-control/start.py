#!/usr/bin/env python3
"""
Shipkit Mission Control — Startup Script

Cross-platform script to start/stop/check the Mission Control server.
Run this in a separate terminal — the server runs in the foreground.

Usage:
    python mission-control.py            # Start server (default)
    python mission-control.py status     # Check if running
    python mission-control.py stop       # Stop server on port 7777
"""

import json
import os
import platform
import re
import shutil
import signal
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

PORT = 7777
HUB_DIR = Path.home() / ".shipkit-mission-control"
CONFIG_PATH = HUB_DIR / ".shipkit" / "mission-control" / "config.json"
SERVER_JS = HUB_DIR / "server" / "index.js"


def parse_server_version(index_js_path):
    """Extract SERVER_VERSION from mission control index.js"""
    try:
        with open(index_js_path, "r", encoding="utf-8") as f:
            for line in f:
                if "SERVER_VERSION" in line and "=" in line:
                    parts = line.split("'")
                    if len(parts) >= 2:
                        return parts[1]
                    parts = line.split('"')
                    if len(parts) >= 2:
                        return parts[1]
    except Exception:
        pass
    return None


def check_health():
    """Check if the MC server is running. Returns health JSON or None."""
    try:
        req = urllib.request.Request(f"http://localhost:{PORT}/health", method="GET")
        with urllib.request.urlopen(req, timeout=3) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return None


def find_mc_source():
    """Find the mission-control source files for copying to the hub.

    Looks for install/mission-control/ relative to this script's location
    (works when run from the Shipkit repo).
    """
    script_dir = Path(__file__).resolve().parent
    # If this script IS in install/mission-control/, source is right here
    if (script_dir / "server" / "index.js").exists():
        return script_dir
    # If copied to .shipkit/scripts/, try finding the repo
    repo_root = script_dir.parent.parent  # .shipkit/scripts -> .shipkit -> project
    mc_src = repo_root / "install" / "mission-control"
    if (mc_src / "server" / "index.js").exists():
        return mc_src
    return None


def ensure_hub(mc_source=None):
    """Ensure the hub directory exists and files are current."""
    # Create directory structure
    (HUB_DIR / "server").mkdir(parents=True, exist_ok=True)
    (HUB_DIR / "dashboard" / "dist").mkdir(parents=True, exist_ok=True)
    (HUB_DIR / ".shipkit" / "mission-control" / "codebases").mkdir(parents=True, exist_ok=True)
    (HUB_DIR / ".shipkit" / "mission-control" / "inbox").mkdir(parents=True, exist_ok=True)

    # Copy/update files from source if available
    if mc_source:
        src_version = parse_server_version(mc_source / "server" / "index.js")
        hub_version = parse_server_version(SERVER_JS)

        if src_version and hub_version and hub_version >= src_version:
            print(f"  Hub already at v{hub_version}, skipping file copy")
        else:
            # Copy server files
            server_src = mc_source / "server"
            server_dest = HUB_DIR / "server"
            for filename in ["index.js", "package.json"]:
                src_file = server_src / filename
                if src_file.exists():
                    shutil.copy2(src_file, server_dest / filename)

            # Copy dashboard dist
            dashboard_src = mc_source / "dashboard" / "dist"
            if dashboard_src.exists():
                dashboard_dest = HUB_DIR / "dashboard" / "dist"
                if dashboard_dest.exists():
                    shutil.rmtree(dashboard_dest)
                shutil.copytree(dashboard_src, dashboard_dest)

            old_msg = f" (was v{hub_version})" if hub_version else ""
            new_msg = f"v{src_version}" if src_version else "latest"
            print(f"  Hub updated to {new_msg}{old_msg}")

    # Create config if missing
    if not CONFIG_PATH.exists():
        config = {
            "port": PORT,
            "host": "0.0.0.0",
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "version": "1.0.0",
        }
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        print("  Config created")


def get_local_ip():
    """Get the local network IP address."""
    if platform.system() == "Windows":
        try:
            result = subprocess.run(
                ["ipconfig"], capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.splitlines():
                if "IPv4" in line and ":" in line:
                    ip = line.split(":")[-1].strip()
                    if ip.startswith("192.") or ip.startswith("10.") or ip.startswith("172."):
                        return ip
        except Exception:
            pass
    else:
        try:
            result = subprocess.run(
                ["hostname", "-I"], capture_output=True, text=True, timeout=5
            )
            parts = result.stdout.strip().split()
            if parts:
                return parts[0]
        except Exception:
            pass
    return "localhost"


def cmd_start():
    """Start the MC server in the foreground."""
    # Check if already running
    health = check_health()
    if health:
        version = health.get("version", "unknown")
        print(f"\n  Mission Control is already running (v{version})")
        print(f"\n  Dashboard: http://localhost:{PORT}")
        print(f"  Network:   http://{get_local_ip()}:{PORT}")
        print(f"\n  Use 'status' for details or 'stop' to shut down.")
        return

    # Ensure hub is set up
    if not SERVER_JS.exists():
        mc_source = find_mc_source()
        if not mc_source:
            print("\n  ERROR: Server files not found.")
            print(f"  Expected: {SERVER_JS}")
            print("  Run the Shipkit installer first, or run this from the Shipkit repo.")
            sys.exit(1)
        ensure_hub(mc_source)
    else:
        # Still check for updates if source is available
        mc_source = find_mc_source()
        if mc_source:
            ensure_hub(mc_source)

    if not SERVER_JS.exists():
        print(f"\n  ERROR: {SERVER_JS} not found after setup.")
        sys.exit(1)

    # Check node is available
    try:
        subprocess.run(
            ["node", "--version"], capture_output=True, text=True, timeout=5
        )
    except FileNotFoundError:
        print("\n  ERROR: Node.js not found. Install it from https://nodejs.org")
        sys.exit(1)

    local_ip = get_local_ip()
    version = parse_server_version(SERVER_JS) or "unknown"

    print(f"""
  Shipkit Mission Control v{version}
  ─────────────────────────────

  Dashboard: http://localhost:{PORT}
  Network:   http://{local_ip}:{PORT}
  Hub:       {HUB_DIR}

  Press Ctrl+C to stop.
""")

    # Start node server as foreground subprocess
    try:
        proc = subprocess.Popen(
            ["node", str(SERVER_JS)],
            cwd=str(HUB_DIR),
        )
        proc.wait()
    except KeyboardInterrupt:
        print("\n\n  Shutting down Mission Control...")
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        print("  Stopped.")


def cmd_status():
    """Check if the MC server is running."""
    health = check_health()
    if health:
        version = health.get("version", "unknown")
        uptime = health.get("uptime", 0)
        instances = health.get("instances", 0)
        local_ip = get_local_ip()
        print(f"""
  Mission Control is RUNNING

  Version:    v{version}
  Uptime:     {int(uptime)}s
  Instances:  {instances}
  Dashboard:  http://localhost:{PORT}
  Network:    http://{local_ip}:{PORT}
""")
    else:
        print(f"""
  Mission Control is NOT RUNNING

  Start it with:
    python {sys.argv[0]}
""")


def cmd_stop():
    """Stop the MC server by killing the process on the port."""
    health = check_health()
    if not health:
        print("\n  Mission Control is not running.")
        return

    system = platform.system()
    try:
        if system == "Windows":
            # Find PID on port 7777 and kill it
            result = subprocess.run(
                ["netstat", "-aon"],
                capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.splitlines():
                if f":{PORT}" in line and "LISTENING" in line:
                    parts = line.split()
                    pid = parts[-1]
                    subprocess.run(["taskkill", "/F", "/PID", pid], timeout=5)
                    print(f"\n  Mission Control stopped (PID {pid}).")
                    return
        else:
            result = subprocess.run(
                ["lsof", f"-ti:{PORT}"],
                capture_output=True, text=True, timeout=5
            )
            pids = result.stdout.strip().split()
            if pids:
                for pid in pids:
                    os.kill(int(pid), signal.SIGTERM)
                print(f"\n  Mission Control stopped (PID {', '.join(pids)}).")
                return
    except Exception as e:
        print(f"\n  Failed to stop server: {e}")
        return

    print("\n  Could not find Mission Control process to stop.")


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "start"
    command = command.lower().strip()

    if command in ("start", ""):
        cmd_start()
    elif command == "status":
        cmd_status()
    elif command == "stop":
        cmd_stop()
    else:
        print(f"\n  Unknown command: {command}")
        print("  Usage: python mission-control.py [start|status|stop]")
        sys.exit(1)


if __name__ == "__main__":
    main()
