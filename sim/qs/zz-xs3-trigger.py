# Sorts after zz-sim-paths.py. A second way for an Xspress3 trigger to finish in the mock
# Queueserver (sim/qs/xs3_trigger.py): scans stalled when the client missed the short 1 of Acquire_RBV.
from sim.qs.xs3_trigger import install as _install_xs3_trigger

_install_xs3_trigger(xs3)
