import logging

logging.getLogger('ophyd').setLevel('WARNING')

from databroker import Broker

db = Broker.named('csx2')

import nslsii
nslsii.configure_base(get_ipython().user_ns, db)
# make sure Best Effort Callback does not plot the baseline readings
bec.noplot_streams.append('pgm_energy_monitor')


### comment this out to:
### disable the zmq servce and re-enable best effort callback plotting locally
bec.disable_plots()

from bluesky.callbacks.zmq import Publisher
pub = Publisher('xf23id-ca:5577')
RE.subscribe(pub)
#####



# TODO not need this
from epics import caget, caput
from amostra.client.commands import SampleReference, ContainerReference


# Optional: set any metadata that rarely changes.

# convenience imports

def ensure_proposal_id(md):
   if 'proposal_id' not in md:
       raise ValueError("Please run user_checkin() first")


from time import sleep
import numpy as np

sample_reference = SampleReference(host='xf23id-ca.cs.nsls2.local', port=7772)
container_reference = ContainerReference(host='xf23id-ca.cs.nsls2.local', port=7772)

from bluesky.callbacks.mpl_plotting import plot_peak_stats


# Set up default metadata.
RE.md['group'] = ''
RE.md['config'] = {}
RE.md['beamline_id'] = 'CSX-2'


from functools import partial
from pyOlog import SimpleOlogClient
from bluesky.callbacks.olog import logbook_cb_factory

# Set up the logbook. This configures bluesky's summaries of
# data acquisition (scan type, ID, etc.).

LOGBOOKS = ['Data Acquisition']  # list of logbook names to publish to
simple_olog_client = SimpleOlogClient()
generic_logbook_func = simple_olog_client.log
configured_logbook_func = partial(generic_logbook_func, logbooks=LOGBOOKS)
desc_template = """
{{- start.plan_name }} ['{{ start.uid[:6] }}'] (scan num: {{ start.scan_id }})
Scan Plan
---------
{{ start.plan_type }}
{%- for k, v in start.plan_args | dictsort %}
    {{ k }}: {{ v }}
{%-  endfor %}
{% if 'signature' in start -%}
Call:
    {{ start.signature }}
{% endif %}
Metadata
--------
{% for k, v in start.items() -%}
{%- if k not in ['plan_type', 'plan_args'] -%}{{ k }} : {{ v }}
{% endif -%}
{%- endfor -%}"""

desc_dispatch = {'edge_ascan': """
{{- start.name }} [{{ start.plan_name }} '{{ start.uid[:6] }}'] (scan num: {{ start.scan_id }})"""}

cb = logbook_cb_factory(configured_logbook_func, desc_template=desc_template,
                        desc_dispatch=desc_dispatch)
nslsii.configure_olog(get_ipython().user_ns, callback=cb)

# WARNING: gs. is no longer supported by bluesky
# if needed, you may uncomment these lines and define your own gs at your own
# risk
#class gs:
    #DETS=[]

from pathlib import Path

import appdirs

try:
    from bluesky.utils import PersistentDict
except ImportError:
    import msgpack
    import msgpack_numpy
    import zict

    class PersistentDict(zict.Func):
        def __init__(self, directory):
            self._directory = directory
            self._file = zict.File(directory)
            super().__init__(self._dump, self._load, self._file)

        @property
        def directory(self):
            return self._directory

        def __repr__(self):
            return f"<{self.__class__.__name__} {dict(self)!r}>"

        @staticmethod
        def _dump(obj):
            "Encode as msgpack using numpy-aware encoder."
            # See https://github.com/msgpack/msgpack-python#string-and-binary-type
            # for more on use_bin_type.
            return msgpack.packb(
                obj,
                default=msgpack_numpy.encode,
                use_bin_type=True)

        @staticmethod
        def _load(file):
            return msgpack.unpackb(
                file,
                object_hook=msgpack_numpy.decode,
                raw=False)

runengine_metadata_dir = appdirs.user_data_dir(appname="bluesky") / Path("runengine-metadata")

# PersistentDict will create the directory if it does not exist
RE.md = PersistentDict(runengine_metadata_dir)

