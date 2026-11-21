"""Keep a mock Queueserver away from the real beamline.

The mock Queueserver loads the IOS profile collection and runs plans against the simulated IOCs
(``sim/run_iocs.py``). The host that runs it is on a network that also reaches the real IOS
devices, so this guard runs *before* the profile is loaded (``sim/qs/00-00-sim-guard.py``) and
refuses to go on unless the profile can only talk to the simulation:

* Channel Access and PV Access are limited to the loopback address, on a non-default port;
  automatic address lists and name servers (gateways) are switched off;
* the sentinel PV ``IOS-SIM:Sentinel``, which only the simulated IOC serves, must answer;
* the external services the profile contacts (redis, Olog, amostra, Kafka) are stubbed or
  redirected to local ones (``sim/externals/stubs.py``).

Settings (environment variables of the mock Queueserver's units):

    IOS_SIM_CA_PORT      Channel Access port of the simulated IOC (required; not 5064)
    IOS_SIM_REDIS_PORT   plaintext redis on 127.0.0.1 (default 6379)
"""

from __future__ import annotations

import logging
import os
import pathlib
import sys

log = logging.getLogger("ios.sim")

SENTINEL_PV = "IOS-SIM:Sentinel"
SENTINEL_VALUE = "ios-sim"
DEFAULT_CA_PORT = 5064

class SimGuardError(RuntimeError):
    """The profile could not be proven to talk only to the simulation."""


def loopback_environment(ca_port: int) -> dict[str, str]:
    """The EPICS environment that confines a client to the simulated IOC."""
    return {
        "EPICS_CA_ADDR_LIST": "127.0.0.1",
        "EPICS_CA_AUTO_ADDR_LIST": "NO",
        "EPICS_CA_SERVER_PORT": str(ca_port),
        "EPICS_CA_REPEATER_PORT": str(ca_port + 1),
        "EPICS_CA_NAME_SERVERS": "",
        "EPICS_PVA_ADDR_LIST": "127.0.0.1",
        "EPICS_PVA_AUTO_ADDR_LIST": "NO",
        "EPICS_PVA_NAME_SERVERS": "",
        "EPICS_PVA_SERVER_PORT": str(ca_port + 2),
        "EPICS_PVA_BROADCAST_PORT": str(ca_port + 3),
    }


def ca_port_from_environment(environ: dict[str, str] | None = None) -> int:
    environ = os.environ if environ is None else environ
    text = environ.get("IOS_SIM_CA_PORT", "")
    try:
        port = int(text)
    except ValueError:
        raise SimGuardError("IOS_SIM_CA_PORT must be set to the simulated IOC's port") from None
    if port == DEFAULT_CA_PORT:
        raise SimGuardError(
            f"IOS_SIM_CA_PORT is the default Channel Access port {DEFAULT_CA_PORT}; use another "
            "port so that this cannot be mistaken for a real IOC"
        )
    if not 1024 <= port < 65532:
        raise SimGuardError(f"IOS_SIM_CA_PORT {port} is not a usable port")
    return port


def check_sentinel(timeout: float = 5.0) -> None:
    """Read the sentinel PV. Raises SimGuardError if it does not answer with its value."""
    from caproto.sync.client import read

    try:
        reply = read(SENTINEL_PV, timeout=timeout)
    except Exception as exc:  # caproto raises several kinds (timeout, no channel)
        raise SimGuardError(
            f"{SENTINEL_PV} does not answer ({exc}); the simulated IOC is not running or the "
            "profile does not reach it. Not loading the profile."
        ) from None
    value = _as_text(reply.data)
    if value != SENTINEL_VALUE:
        raise SimGuardError(f"{SENTINEL_PV} is {value!r}, not {SENTINEL_VALUE!r}")


def _as_text(data) -> str:
    """A string PV arrives as one string, or (a char array) as the codes of its characters."""
    items = list(data)
    if items and isinstance(items[0], (bytes, str)):
        first = items[0]
        return first.decode() if isinstance(first, bytes) else first
    return bytes(int(c) for c in items).decode(errors="replace").rstrip("\x00")


def enforce(repo_root: str | os.PathLike | None = None) -> None:
    """Confine the process to the simulation, or raise SimGuardError."""
    port = ca_port_from_environment()
    os.environ.update(loopback_environment(port))
    for name in ("EPICS_CA_NAME_SERVERS", "EPICS_PVA_NAME_SERVERS"):
        os.environ.pop(name, None)  # an empty value is the same as unset; make it unambiguous
    root = pathlib.Path(repo_root or os.environ.get("IOS_SIM_REPO", "")).resolve()
    if not (root / "sim" / "run_iocs.py").exists():
        raise SimGuardError("IOS_SIM_REPO must point at the profile collection")
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    check_sentinel()
    from sim.externals.stubs import apply_all

    apply_all()
    log.warning("IOS MOCK QUEUESERVER: simulated IOC on 127.0.0.1:%d; the real beamline is not used", port)
