"""Wait until the simulated IOC answers (the sentinel PV), or exit with a message.

Run before the mock Queueserver's RE Manager starts, so that the guard (sim/qs/guard.py) does not
find the IOC still starting. It uses the same loopback-only environment as the guard.

    python sim/qs/wait_for_sim.py --timeout 60
"""

from __future__ import annotations

import argparse
import os
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from sim.qs.guard import SimGuardError, ca_port_from_environment, check_sentinel, loopback_environment


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--timeout", type=float, default=60.0)
    args = parser.parse_args()
    try:
        os.environ.update(loopback_environment(ca_port_from_environment()))
    except SimGuardError as exc:
        print(f"wait_for_sim: {exc}", file=sys.stderr)
        return 2
    deadline = time.monotonic() + args.timeout
    last = ""
    while True:
        try:
            check_sentinel(timeout=2.0)
            return 0
        except SimGuardError as exc:
            last = str(exc)
        if time.monotonic() >= deadline:
            print(f"wait_for_sim: gave up after {args.timeout:.0f} s: {last}", file=sys.stderr)
            return 1
        time.sleep(2.0)


if __name__ == "__main__":
    sys.exit(main())
