# First startup file of the mock Queueserver (see sim/qs/guard.py). If this raises, the profile is
# not loaded and the worker does not start.
import os
import sys

_repo = os.environ.get("IOS_SIM_REPO", "")
if _repo and _repo not in sys.path:
    sys.path.insert(0, _repo)

from sim.qs.guard import enforce

enforce()
