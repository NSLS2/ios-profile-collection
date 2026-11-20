"""
sim/check_happi.py
------------------
Compare a happi device database (the one the ophyd-service configuration
service loads) with the devices of the IOS profile collection.

The happi database of ophyd-service (``integration/happi/sites/ios``) was made
from the startup files and a hand-written port of their classes, before the
simulation existed. The profile collection is what runs at the beamline and the
simulated IOCs serve what its classes ask for, so where the two disagree the
profile is right. This script lists the disagreements; it changes nothing.

For every device the PV names are collected the way ``check_drift.py`` does it
(ophyd classes walked offline, no connection), once from the profile and once
from the happi entry (its ``device_class`` built with its ``prefix``).

Reported per device:

  match        same PV set
  differs      PVs only the profile has / only the happi entry has
  profile-only a device of the profile that happi does not have
  happi-only   a happi entry that the profile does not have
  not served   PVs of the happi entry that the simulated IOC does not serve:
               what a client of the configuration service would ask for and
               not get (the test that matters when the registry is used with
               the simulation)

The profile walk can miss components that are really there (offline, some
attributes are not reachable), so a PV that only happi has is not a conflict
as long as the simulated IOC serves it.

Usage
~~~~~
  python sim/check_happi.py --happi PATH/TO/happi_db.json   # human readable
  python sim/check_happi.py --happi PATH --json             # for scripts

``ios_devs.py`` (the class port) is imported from the directory of the happi
file. Exit status: 0 when every device matches, 1 otherwise, 2 when the happi
file cannot be used.
"""

from __future__ import annotations

import argparse
import importlib
import json
import pathlib
import sys

_REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO))

from sim import check_drift  # noqa: E402


def _render(value, entry):
    if isinstance(value, str):
        return value.replace("{{prefix}}", entry["prefix"]).replace("{{name}}", entry["name"])
    return value


def _happi_pvs(entry: dict) -> set[str]:
    module_name, _, class_name = entry["device_class"].rpartition(".")
    cls = getattr(importlib.import_module(module_name), class_name)
    args = [_render(a, entry) for a in entry.get("args", [])]
    kwargs = {k: _render(v, entry) for k, v in entry.get("kwargs", {}).items()}
    return check_drift._walk_pvs(cls(*args, **kwargs))


def compare(happi_path: pathlib.Path) -> dict:
    sys.path.insert(0, str(happi_path.parent))
    database = json.loads(happi_path.read_text())
    _, load_warnings, profile = check_drift.load_source_a()
    served = check_drift.load_source_b()

    result: dict = {"match": [], "differs": {}, "profile_only": [], "happi_only": [],
                    "happi_errors": {}, "not_served": {}, "profile_load_warnings": load_warnings}
    for name, entry in sorted(database.items()):
        if not entry.get("active", True):
            continue
        try:
            theirs = _happi_pvs(entry)
        except Exception as exc:  # a class that cannot be built offline is reported, not skipped
            result["happi_errors"][name] = f"{type(exc).__name__}: {exc}"
            continue
        missing = sorted(pv for pv in theirs if pv not in served)
        if missing:
            result["not_served"][name] = missing
        if name not in profile:
            result["happi_only"].append(name)
            continue
        ours = profile[name]
        if ours == theirs:
            result["match"].append(name)
        else:
            result["differs"][name] = {
                "profile_only": sorted(ours - theirs),
                "happi_only": sorted(theirs - ours),
            }
    result["profile_only"] = sorted(set(profile) - set(database))
    return result


def _print(result: dict) -> None:
    print(f"match: {len(result['match'])} devices")
    for name, diff in result["differs"].items():
        print(f"differs: {name}: {len(diff['profile_only'])} PVs only in the profile, "
              f"{len(diff['happi_only'])} only in happi")
        for pv in diff["profile_only"][:3]:
            print(f"    profile: {pv}")
        for pv in diff["happi_only"][:3]:
            print(f"    happi:   {pv}")
    for name, pvs in result["not_served"].items():
        print(f"not served by the simulation: {name}: {len(pvs)} PVs, e.g. {pvs[0]}")
    for key in ("happi_only", "profile_only"):
        for name in result[key]:
            print(f"{key.replace('_', '-')}: {name}")
    for name, error in result["happi_errors"].items():
        print(f"cannot build: {name}: {error}")
    for warning in result["profile_load_warnings"]:
        print(f"profile: {warning}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--happi", required=True, type=pathlib.Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not args.happi.is_file():
        print(f"no such file: {args.happi}", file=sys.stderr)
        return 2
    result = compare(args.happi.resolve())
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        _print(result)
    clean = not (result["differs"] or result["happi_only"] or result["profile_only"]
                 or result["happi_errors"] or result["not_served"])
    return 0 if clean else 1


if __name__ == "__main__":
    raise SystemExit(main())
