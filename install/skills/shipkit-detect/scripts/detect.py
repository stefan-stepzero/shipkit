#!/usr/bin/env python3
"""
shipkit-detect - Unified detection and queue creation

Usage:
    python detect.py --mode=services
    python detect.py --mode=contracts
    python detect.py --mode=changes
    python detect.py --mode=ux-gaps
"""

import argparse
import sys
from pathlib import Path

# Import scan modules
from scan_services import scan as scan_services, create_queue as create_services_queue
from scan_contracts import scan as scan_contracts, create_queue as create_contracts_queue
from scan_changes import scan as scan_changes, create_queue as create_changes_queue
from scan_ux_gaps import scan as scan_ux_gaps, create_queue as create_ux_gaps_queue


MODES = {
    "services": (scan_services, create_services_queue),
    "contracts": (scan_contracts, create_contracts_queue),
    "changes": (scan_changes, create_changes_queue),
    "ux-gaps": (scan_ux_gaps, create_ux_gaps_queue),
}


def main():
    parser = argparse.ArgumentParser(description="Unified detection skill")
    parser.add_argument("--mode", required=True, choices=MODES.keys(),
                        help="Detection mode to run")
    args = parser.parse_args()

    mode = args.mode
    scan_fn, queue_fn = MODES[mode]

    print(f"[shipkit-detect] Running mode: {mode}")

    try:
        # Run detection
        detected = scan_fn()

        if not detected:
            print(f"[shipkit-detect] No items detected for {mode}")
            return 0

        # Create queue
        queue_path = queue_fn(detected)
        print(f"[shipkit-detect] Created queue: {queue_path}")
        print(f"[shipkit-detect] Items queued: {len(detected)}")

        return 0

    except FileNotFoundError as e:
        print(f"[shipkit-detect] File not found: {e}")
        return 1
    except Exception as e:
        print(f"[shipkit-detect] Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
