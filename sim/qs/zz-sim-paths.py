# Last startup file of the mock Queueserver (see sim/qs/guard.py): the profile writes the Xspress3
# files below /nsls2/data/ios/legacy/xspress3_data, a real data path. The mock must never write
# there. The simulated IOC writes only below IOS_SIM_DATA_DIR (and reports other paths as
# missing); this file points the plugin at that directory, so that a ramp stages and captures.
import os
import pathlib

_root = str(pathlib.Path(os.environ["IOS_SIM_DATA_DIR"]).resolve())
for _name in ("xs3_root_path", "xs3_data_dir"):
    globals().pop(_name, None)
xs3_root_path = _root
xs3_data_dir = os.path.join(_root, "%Y/%m/%d")
xs3.hdf5plugin.root_path.put(xs3_root_path)
xs3.hdf5plugin.path_template.put(xs3_data_dir)
