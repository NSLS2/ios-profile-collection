"""
sim/run_iocs.py
---------------
Start all simulated caproto IOCs for the IOS profile collection.

Every EPICS PV name is identical to the real beamline IOC.  Only the
CA addressing differs: this server binds to 127.0.0.1 on a fixed port
and expects clients to set::

    EPICS_CA_ADDR_LIST=127.0.0.1
    EPICS_CA_AUTO_ADDR_LIST=NO

Usage::

    python sim/run_iocs.py            # foreground, logs to stdout
    python sim/run_iocs.py --list-pvs # print all served PV names and exit

The script can also be invoked via the pixi task::

    pixi run sim-iocs

Environment variables (all optional):

    IOS_SIM_CA_PORT   CA server port (default: 5064, the EPICS standard). The repeater/beacon
                      port is this plus one. A mock Queueserver on a shared network uses a
                      non-default port so that it cannot be mistaken for a real IOC.
    IOS_SIM_LOG_LEVEL log level name (default: WARNING)
    IOS_SIM_FALLBACK  1: answer for every PV name that no PVGroup serves, with a plain value (0.0,
                      or a string for names that look like text). For a mock Queueserver that must
                      load the whole profile although the simulation does not cover every PV yet
                      (see sim/check_drift.py for the gaps). Each fabricated PV is logged once, at
                      WARNING level, and listed in IOS_SIM_FALLBACK_LOG if that is set. Default: off.

The sim IOC serves the sentinel PV ``IOS-SIM:Sentinel`` (the string ``ios-sim``). The sim guard of
the mock Queueserver (sim/qs/00-00-sim-guard.py) refuses to load the profile unless that PV answers,
which proves that the profile is talking to this IOC and not to a real beamline.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
import time

# Ensure the repo root is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from caproto import ChannelType
from caproto.server import run, PVGroup, pvproperty, SubGroup

from sim.pvgroups.motors import MotorFields, MOTOR_PREFIX_MAP
from sim.pvgroups.scaler_signals import (
    ScalerIOC,
    StandaloneSignalsIOC,
    ShutterIOC,
    SHUTTER_PREFIX_MAP,
)
from sim.pvgroups.positioners import (
    EPU1IOC,
    EPU2IOC,
    EPUStopIOC,
    M1A_IOC,
    M1B1_IOC,
    M1B2_IOC,
    M3B_IOC,
    MirrorStandaloneIOC,
    FeedbackLoopIOC,
    PGMEnergyIOC,
    VortexIOC,
)
from sim.pvgroups.detectors import SpecsIOC
from sim.pvgroups.xspress3 import build as build_xspress3

log = logging.getLogger("ios.sim")

SENTINEL_PV = "IOS-SIM:Sentinel"
SENTINEL_VALUE = "ios-sim"


class SentinelIOC(PVGroup):
    """A PV that exists only in the simulation (see the module docstring)."""

    sentinel = pvproperty(
        value=SENTINEL_VALUE, name=SENTINEL_PV, dtype=ChannelType.STRING, read_only=True
    )


# ---------------------------------------------------------------------------
# Build the combined PVGroup list
# ---------------------------------------------------------------------------

def build_ioc_groups() -> list[tuple[type, str]]:
    """Return a list of (PVGroup subclass, prefix) pairs for every IOC."""

    groups: list[tuple[type, str]] = []

    groups.append((SentinelIOC, ""))

    # -- Motors ------------------------------------------------------------
    for name, prefix in MOTOR_PREFIX_MAP.items():
        groups.append((MotorFields, prefix))

    # -- Scaler -----------------------------------------------------------
    groups.append((ScalerIOC, "XF:23ID2-ES{{Sclr:1}}"))

    # -- Standalone signals (one flat group, prefix="" so PV names are full)
    groups.append((StandaloneSignalsIOC, ""))

    # -- Shutters ---------------------------------------------------------
    for name, prefix in SHUTTER_PREFIX_MAP.items():
        groups.append((ShutterIOC, prefix))

    # -- EPU --------------------------------------------------------------
    # EPU1IOC/EPU2IOC use absolute PV names (prefix split mid-brace), so prefix="".
    groups.append((EPU1IOC, ""))
    groups.append((EPU2IOC, ""))
    groups.append((EPUStopIOC, ""))   # absolute-PV stop signals, no prefix

    # -- Mirrors (split-brace prefixes — use absolute-PV IOC classes) ------
    groups.append((M1A_IOC,  ""))
    groups.append((M1B1_IOC, ""))
    groups.append((M1B2_IOC, ""))
    groups.append((M3B_IOC,  ""))
    groups.append((MirrorStandaloneIOC, ""))

    # -- Mirror feedback --------------------------------------------------
    groups.append((FeedbackLoopIOC, "XF:23ID2-OP{{FBck}}"))

    # -- PGM (absolute PV names, prefix="") --------------------------------
    groups.append((PGMEnergyIOC, ""))

    # -- Vortex MCA -------------------------------------------------------
    groups.append((VortexIOC, "XF:23ID2-ES{{Vortex}}"))

    # -- SPECS analyzer (flat group, absolute PV names — prefix must be "") --
    groups.append((SpecsIOC, ""))

    # -- Xspress3 (flat group, absolute PV names — prefix must be "") ------
    groups.append((build_xspress3(), ""))

    return groups


# ---------------------------------------------------------------------------
# Merge all groups into a single top-level PVGroup for caproto
# ---------------------------------------------------------------------------

def assemble_pvgroup(groups: list[tuple[type, str]]) -> type:
    """
    Dynamically assemble all (PVGroup subclass, prefix) pairs into a single
    top-level PVGroup subclass that caproto's ``run()`` can host.

    Each entry becomes a SubGroup descriptor at the class level.  The top-level
    group is instantiated with prefix="" so each sub-group's prefix is its
    full absolute PV prefix.
    """
    attrs: dict = {}
    for i, (cls, prefix) in enumerate(groups):
        # Note: caproto skips attributes starting with '_', so use 'ioc_N'.
        attr_name = f"ioc_{i}"
        attrs[attr_name] = SubGroup(cls, prefix=prefix)

    TopLevel = type("IOSSimIOC", (PVGroup,), attrs)
    return TopLevel


async def run_with_startup(ioc_instance):
    """Run _startup() hooks on any sub-group that defines one."""
    for attr_name in vars(type(ioc_instance)):
        if not attr_name.startswith("ioc_"):
            continue
        child = getattr(ioc_instance, attr_name)
        if hasattr(child, "_startup") and asyncio.iscoroutinefunction(child._startup):
            await child._startup()
        # One level deeper (e.g. Xspress3IOC contains sub-PVGroups)
        for sub_attr in vars(type(child)):
            if sub_attr.startswith("_"):
                continue
            sub = getattr(child, sub_attr, None)
            if sub is None:
                continue
            if hasattr(sub, "_startup") and asyncio.iscoroutinefunction(sub._startup):
                await sub._startup()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="IOS sim IOCs (caproto)")
    p.add_argument(
        "--list-pvs",
        action="store_true",
        help="Print all served PV names and exit without starting the server.",
    )
    p.add_argument(
        "--log-level",
        default=os.environ.get("IOS_SIM_LOG_LEVEL", "WARNING"),
        help="Logging level (default: WARNING)",
    )
    return p.parse_args()


_TEXT_ENDINGS = (
    ".EGU", ".DESC", ".NAME", "Name", "Name_RBV", "FilePath", "FilePath_RBV", "FileName",
    "FileName_RBV", "FileTemplate", "FileTemplate_RBV", "FullFileName_RBV", "StatusMessage_RBV",
    "Message", "Message_RBV", "PluginType_RBV", "Manufacturer_RBV", "Model_RBV", "PortName_RBV",
    "NDAttributesFile",
)


class FallbackPVDB(dict):
    """The PV database, answering for every name that it does not hold.

    The first request for an unknown name makes a plain channel for it: a string for names that
    look like text, a floating point number (0.0) otherwise. It holds no behaviour: a mock that
    needs one has to add a PVGroup. Every fabricated name is logged once.
    """

    def __init__(self, base, log_path: str | None = None):
        super().__init__(base)
        self._log_path = log_path
        self.fabricated: list[str] = []

    def __contains__(self, key):
        return True

    def __missing__(self, key):
        from caproto import ChannelDouble, ChannelString

        if key.endswith(_TEXT_ENDINGS):
            channel = ChannelString(value="", string_encoding="utf-8")
        else:
            channel = ChannelDouble(value=0.0)
        self[key] = channel
        self.fabricated.append(key)
        log.warning("fallback PV fabricated: %s", key)
        if self._log_path:
            with open(self._log_path, "a", encoding="utf-8") as handle:
                handle.write(key + "\n")
        return channel


def start_repeater():
    """Start a caproto repeater on the repeater port (the IOC's beacons and the clients' registrations)."""
    import pathlib
    import subprocess

    exe = pathlib.Path(sys.executable).with_name("caproto-repeater")
    if not exe.exists():
        log.warning("caproto-repeater not found next to %s; beacons will fail", sys.executable)
        return None
    process = subprocess.Popen([str(exe), "-q"], env=os.environ.copy())
    time.sleep(1.0)  # the first beacons need a listener
    return process


def main() -> None:
    args = parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.WARNING),
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )

    ca_port = int(os.environ.get("IOS_SIM_CA_PORT", "5064"))
    interfaces = ["127.0.0.1"]
    # caproto reads the server and beacon ports and addresses from the environment; a non-default
    # port and loopback-only beacons keep the sim off the real networks.
    os.environ["EPICS_CA_SERVER_PORT"] = str(ca_port)
    os.environ["EPICS_CAS_SERVER_PORT"] = str(ca_port)
    os.environ["EPICS_CA_REPEATER_PORT"] = str(ca_port + 1)
    os.environ["EPICS_CAS_INTF_ADDR_LIST"] = "127.0.0.1"
    # Beacons go only to the loopback address, to a caproto repeater started below (an address
    # nobody listens on makes the send fail, and with the defaults the IOC would broadcast).
    os.environ["EPICS_CAS_AUTO_BEACON_ADDR_LIST"] = "no"
    os.environ["EPICS_CAS_BEACON_ADDR_LIST"] = "127.0.0.1"
    os.environ["EPICS_CAS_BEACON_PORT"] = str(ca_port + 1)

    groups = build_ioc_groups()

    if args.list_pvs:
        # Instantiate briefly to collect PV names, then exit
        TopLevel = assemble_pvgroup(groups)
        ioc = TopLevel(prefix="")
        pvdb = ioc.pvdb
        for pvname in sorted(pvdb.keys()):
            print(pvname)
        print(f"\n{len(pvdb)} PVs served", file=sys.stderr)
        return

    TopLevel = assemble_pvgroup(groups)

    log.warning(
        "Starting IOS sim IOC on 127.0.0.1:%d  (%d device groups)",
        ca_port,
        len(groups),
    )
    log.warning(
        "Set EPICS_CA_ADDR_LIST=127.0.0.1 EPICS_CA_AUTO_ADDR_LIST=NO "
        "before starting the profile."
    )

    ioc = TopLevel(prefix="")
    repeater = start_repeater()

    async def _startup(async_lib):
        """Seed PVs that need pre-populated values (Xspress3 roi_name, etc.)."""
        await run_with_startup(ioc)

    pvdb = ioc.pvdb
    if os.environ.get("IOS_SIM_FALLBACK") == "1":
        pvdb = FallbackPVDB(pvdb, os.environ.get("IOS_SIM_FALLBACK_LOG"))
        log.warning("IOS_SIM_FALLBACK=1: PVs that are not simulated are fabricated on request")
    try:
        run(
            pvdb,
            startup_hook=_startup,
            interfaces=interfaces,
            log_pv_names=False,
        )
    finally:
        if repeater is not None:
            repeater.terminate()


if __name__ == "__main__":
    main()
