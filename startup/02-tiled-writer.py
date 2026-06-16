import numpy
import os

from bluesky_tiled_plugins import TiledWriter
from bluesky.callbacks.buffer import BufferingWrapper
from tiled.client import from_uri


# Mapping from spec to mimetype for use in TiledWriter
# TODO: Only keep the necessary specs here
MIMETYPE_LOOKUP = {
        "AD_HDF5": "application/x-hdf5",
        "XSP3": "application/x-hdf5",        # iss_patches:ISSXspress3HDF5Handler, area_detector_handlers.handlers:Xspress3HDF5Handler
        "XSP3_BULK": "application/x-hdf5",
        "XSP3_FLY": "application/x-hdf5",
        "XSP3_STEP": "application/x-hdf5",   # databroker.assets.handlers:Xspress3HDF5Handler, area_detector_handlers.handlers:Xspress3HDF5Handler
        "XSP3X": "application/x-hdf5",

        "hdf5": "application/x-hdf5",
        "A1_HDF5": "application/x-hdf5",  # esm_patches:A1SoftFileHandler(HDF5DatasetSliceHandler)
        "AD_CBF": "multipart/related;type=image/tiff",
        "AD_EIGER_MX": "application/x-hdf5",
        "AD_EIGER2": "application/x-hdf5",
        "AD_JPEG": "multipart/related;type=image/jpeg",
        "AD_HDF5_GERM": "application/x-hdf5",
        "AD_HDF5_SWMR_STREAM": "application/x-hdf5",
        "AD_HDF5_SWMR_SLICE": "application/x-hdf5",
        "AD_HDF5_SWMR": "application/x-hdf5",
        "AD_HDF5_TS": "application/x-hdf5",    # area_detector_handlers.handlers:AreaDetectorHDF5TimestampHandler
        "AD_HDF5_DET_TS": "application/x-hdf5",    # csx_transforms.AreaDetectorHDF5NDArrayTimeStampHandler
        "AD_TIFF": "multipart/related;type=image/tiff",
        "APB": "application/x-pizzabox-binary",     # columns: timestamp, i0, it, ir, iff, aux1, aux2, aux3, aux4.   iss_patches:APBBinFileHandler
        "APB_TRIGGER": "application/x-pizzabox-binary",  # columns: timestamp, transition,   iss_patches:APBTriggerFileHandler
        "DEX_HDF5": "application/x-hdf5",
        "EIGER2_STREAM": "application/x-hdf5",
        "MERLIN_FLY_STREAM_V2": "application/x-hdf5",
        "MERLIN_HDF5_BULK": "application/x-hdf5",
        "PANDA": "application/x-hdf5",
        "PIL100k_HDF5": "application/x-hdf5",      # iss_patches:ISSPilatusHDF5Handler
        "PILATUS_HDF5": "application/x-hdf5",
        "ROI_HDF5_FLY": "application/x-hdf5",
        "ROI_HDF51_FLY": "application/x-hdf5",
        "SIS_HDF51_FLY_STREAM_V1": "application/x-hdf5",
        "TPX_HDF5": "application/x-hdf5",
        "NPY_SEQ": "multipart/related;type=application/x-npy",
        "SIS_HDF51": "application/x-hdf5",
        "SPECS_HDF5_SINGLE_DATAFRAME": "application/x-hdf5",    # IOS
        "XIA_XMAP_HDF5": "application/x-hdf5;type=xia-xmap",
    }


# Define document-specific patches to be applied before sending them to TiledWriter
def patch_descriptor(doc):
    if "vortex_mca_spectrum" in doc["data_keys"]:
        doc["data_keys"]["vortex_mca_spectrum"]["dtype_str"] = "<i8"

    # Ensure dtype_str has the proper numpy format (to pass the EventModel validator)
    for key, val in doc["data_keys"].items():
        if "dtype_str" in val:
            val["dtype_str"] = numpy.dtype(val["dtype_str"]).str
        val["shape"] = tuple(map(lambda x: max(x, 0), val.get("shape", [])))

    # Fix the shape of xs3_channel01_data
    if "xs3_channel01_data" in doc["data_keys"]:
        doc["data_keys"]["xs3_channel01_data"]["shape"] = (1, 4096)
        doc["data_keys"]["xs3_channel01_data"]["dims"] = ('time', 'bin_count')

    return doc

def patch_datum(doc):
    kwargs = doc.get("datum_kwargs", {})
    spec = kwargs.pop("_resource_spec", None)    # Added by RunNormalizer
    if "channel" in kwargs:
        # databroker.assets.handlers.Xspress3HDF5Handler --- general case
        kwargs["dataset"] = "entry/instrument/detector/data"
        channel = kwargs["channel"]
        kwargs["slice"] = f"(:,{channel-1},:)"
        kwargs["squeeze"] = True

    return doc

def patch_resource(doc):

    kwargs = doc.get("resource_kwargs", {})

    # Fix or add resource parameters
    if doc.get("spec") in ["XSP3", "XSP3X"]:
        kwargs.update({"dataset": 'entry/instrument/detector/data', "chunk_shape": (1, ), "join_method": "concat"})
    elif doc.get("spec") in ["AD_HDF5"]:
        kwargs.update({"dataset": 'entry/instrument/detector/data'})

    return doc


# Initialize the Tiled client and the TiledWriter
api_key = os.environ.get("TILED_BLUESKY_WRITING_API_KEY_IOS")
tiled_writing_client_sql = from_uri("https://tiled.nsls2.bnl.gov", api_key=api_key)['ios/migration']
tw = TiledWriter(client = tiled_writing_client_sql,
                 backup_directory="/tmp/tiled_backup",   # NOTE: Pick a suitable backup directory
                 patches = {"descriptor": patch_descriptor,
                            "resource": patch_resource,
                            "datum": patch_datum},
                 spec_to_mimetype = MIMETYPE_LOOKUP,
                 batch_size=10000,   # NOTE: Set to 1 to disable batching
                 validate = True     # NOTE: After Data Security -- validate in Prefect
                 )

# Thread-safe wrapper for TiledWriter
tw = BufferingWrapper(tw)

# Subscribe the TiledWriter
RE.md["tiled_access_tags"] = (RE.md["data_session"],)
RE.subscribe(tw)
