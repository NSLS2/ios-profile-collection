"""Smoke test of a running mock Queueserver (see sim/qs/run-local.sh and the Ansible role).

It opens the environment, checks the plans that the group may run, queues one ``xas_edge_ascan`` and one
``xas_pd_ascan`` item with ``meta.xas`` (as the XAS experiment model builds them), runs them, and checks
that both completed, that the start document of each run carries the ``xas`` metadata, and that a plan
outside the allowlist is refused. With ``--documents`` (the file named by ``IOS_SIM_DOC_LOG``) it reads the
start and stop documents the worker appended; with ``--data-dir`` it also checks that every run's
Xspress3 file is a link to the shared simulated file inside that directory.

    python sim/qs/smoke.py --url http://127.0.0.1:60612 --api-key KEY \
        --documents /tmp/ios-mock-qs/documents.jsonl --data-dir /tmp/ios-mock-qs/xspress3_data

Exit status 0: all checks passed.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time

EDGE = dict(
    start=700, stop=702, velocity=1.0, deadband=8.0, e_align=709, epu_table=4, epu_offset=-0.2,
    m1b1_sp=386, au_mesh_pos=-130.2, sample_pos=266.7, diag3_pos=49,
    dwell_s=0.2, pfy_min_x=400, pfy_size_x=300, ipfy_min_x=100, ipfy_size_x=200,
)
PD = dict(
    start=700, stop=702, velocity=1.0, deadband=8.0, e_align=709, epu_table=4, epu_offset=-0.2,
    m1b1_sp=386, au_mesh_pos=-130.2, pd_diag3_pos=16.3, sample_out_x=90.0, dwell_s=0.2,
)
ALLOWED = {"xas_edge_ascan", "xas_pd_ascan", "XAS_scan", "PD_scan", "find_sample", "count", "mv"}


class Check:
    def __init__(self) -> None:
        self.failures: list[str] = []

    def __call__(self, ok: bool, what: str) -> None:
        print(("ok    " if ok else "FAIL  ") + what)
        if not ok:
            self.failures.append(what)


def documents(path: pathlib.Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def wait_for_history(RM, count: int, timeout: float) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        status = RM.status()
        if status["items_in_history"] >= count and status["manager_state"] == "idle":
            return
        time.sleep(1.0)
    raise TimeoutError(f"{count} plans were not finished in {timeout:.0f} s")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--url", default="http://127.0.0.1:60612")
    parser.add_argument("--api-key", required=True)
    parser.add_argument("--documents", type=pathlib.Path)
    parser.add_argument("--data-dir", type=pathlib.Path)
    parser.add_argument("--timeout", type=float, default=240.0)
    args = parser.parse_args()

    from bluesky_queueserver_api.comm_base import RequestFailedError
    from bluesky_queueserver_api.http import REManagerAPI

    check = Check()
    RM = REManagerAPI(http_server_uri=args.url)
    RM.set_authorization_key(api_key=args.api_key)
    try:
        if not RM.status()["worker_environment_exists"]:
            RM.environment_open()
            RM.wait_for_idle(timeout=args.timeout)
        allowed = set(RM.plans_allowed()["plans_allowed"])
        check(allowed == ALLOWED, f"the group may run exactly {sorted(ALLOWED)} (got {sorted(allowed)})")

        before = RM.status()["items_in_history"]
        for name, kwargs, repeat in (("xas_edge_ascan", EDGE, 1), ("xas_pd_ascan", PD, 2)):
            RM.item_add({
                "name": name, "item_type": "plan", "args": [], "kwargs": kwargs,
                "meta": {"xas": {"experiment_id": "smoke", "plan": name, "repeat": repeat}},
            })
        RM.queue_start()
        wait_for_history(RM, before + 2, args.timeout)
        history = RM.history_get()["items"][before:]
        for item in history:
            result = item["result"]
            check(result.get("exit_status") == "completed", f"{item['name']} completed ({result.get('msg', '')[:80]})")

        try:
            RM.item_add({"name": "scan", "item_type": "plan", "args": [[], "x", 0, 1, 2]})
            check(False, "a plan outside the allowlist (scan) is refused")
        except RequestFailedError:
            check(True, "a plan outside the allowlist (scan) is refused")
    finally:
        RM.close()

    if args.documents:
        docs = documents(args.documents)
        starts = [d["doc"] for d in docs if d["name"] == "start"][-2:]
        stops = [d["doc"] for d in docs if d["name"] == "stop"][-2:]
        check(len(starts) == 2 and len(stops) == 2, "two runs wrote start and stop documents")
        for start, stop in zip(starts, stops, strict=False):
            name = start.get("xas", {}).get("plan")
            check(start.get("plan_name") == name, f"run of {name}: start document has plan_name and meta.xas")
            check(stop.get("exit_status") == "success", f"run of {name}: exit status success")
            check(stop.get("num_events", {}).get("primary", 0) > 0, f"run of {name}: primary stream has events")
        check(starts[0].get("xas", {}).get("repeat") == 1 and starts[1].get("xas", {}).get("repeat") == 2,
              "meta.xas carries the repeat")

    if args.data_dir:
        shared = (args.data_dir / ".shared" / "xspress3-sim.h5").resolve()
        links = [p for p in args.data_dir.rglob("*.h5") if p.is_symlink()]
        check(bool(links) and all(p.resolve() == shared for p in links),
              f"the Xspress3 files of the runs ({len(links)}) are links to the one shared file")

    print("all checks passed" if not check.failures else f"{len(check.failures)} check(s) failed")
    return 1 if check.failures else 0


if __name__ == "__main__":
    sys.exit(main())
