import os
import datetime
from ophyd import Component as Cpt
from ophyd.areadetector import Xspress3Detector, ProcessPlugin
from nslsii.areadetector.xspress3 import (
    Xspress3Trigger,
    build_xspress3_class,
    Xspress3HDF5Plugin,
)
from ophyd.status import SubscriptionStatus

def now():
    return datetime.datetime.now().isoformat()


xs3_pv_prefix = "XF:23ID2-ES{Xsp:1}:"
xs3_root_path = "/nsls2/data3/ios/legacy/xspress3_data"
xs3_data_dir = os.path.join(xs3_root_path, "%Y/%m/%d")

xspress3_class = build_xspress3_class(
        channel_numbers=(1,),
        mcaroi_numbers=(1, 2, 3, 4,),
        image_data_key="data",
        xspress3_parent_classes=(Xspress3Detector, Xspress3Trigger),
        extra_class_members={
            "hdf5plugin": Cpt(
                Xspress3HDF5Plugin,
                "HDF1:",
                name="h5p",
                root_path=xs3_root_path,
                path_template=xs3_data_dir,
                resource_kwargs={},
            ),
            # "proc_plugin": Cpt(ProcessPlugin, 'Proc1:')
        },
    )

xs3 = xspress3_class(prefix=xs3_pv_prefix, name="xs3")
# TODO: check why xs3.hdf5plugin.warmup() hangs.

# Hint the fields below to have the events generated:
for channel in xs3.iterate_channels():
    channel.kind = "normal"
    channel.data.kind = "normal"
    for mcaroi in channel.iterate_mcarois():
        mcaroi.kind = "hinted"
        mcaroi.total_rbv.kind = "hinted"
        _roi_name = mcaroi.roi_name.get()
        if _roi_name:
            mcaroi.total_rbv.name = _roi_name
        else:
            mcaroi.total_rbv.name = f"{mcaroi.name}_roi"
            print(f"No PV set for {mcaroi.roi_name.name}, setting default name for total_rbv for {mcaroi.name}")
