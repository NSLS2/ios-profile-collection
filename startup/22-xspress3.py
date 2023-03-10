print(f'Loading {__file__}...')

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
xs3_root_path = "/nsls2/data/ios/shared/xspress3_data/"
xs3_data_dir = os.path.join(xs3_root_path, "%Y/%m/%d")

xspress3_class = build_xspress3_class(
        channel_numbers=(1,),
        mcaroi_numbers=(1,),
        image_data_key="data",
        xspress3_parent_classes=(Xspress3Detector, Xspress3Trigger),
        extra_class_members={
            "hdf5plugin": Component(
                Xspress3HDF5Plugin,
                "HDF1:",
                name="h5p",
                root_path=xs3_root_path,
                path_template=xs3_data_dir,
                resource_kwargs={},
            ),
#            "proc_plugin": Component(ProcessPlugin, 'Proc1:')
        },
    )

xs3 = xspress3_class(prefix=xs3_pv_prefix, name="xs3")



