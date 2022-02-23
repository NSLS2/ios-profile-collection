###############################################################################
# TODO: remove this block once https://github.com/bluesky/ophyd/pull/959 is
# merged/released.
from datetime import datetime
from ophyd.signal import EpicsSignalBase, EpicsSignal, DEFAULT_CONNECTION_TIMEOUT

def print_now():
    return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')

def wait_for_connection_base(self, timeout=DEFAULT_CONNECTION_TIMEOUT):
    '''Wait for the underlying signals to initialize or connect'''
    if timeout is DEFAULT_CONNECTION_TIMEOUT:
        timeout = self.connection_timeout
    # print(f'{print_now()}: waiting for {self.name} to connect within {timeout:.4f} s...')
    start = time.time()
    try:
        self._ensure_connected(self._read_pv, timeout=timeout)
        # print(f'{print_now()}: waited for {self.name} to connect for {time.time() - start:.4f} s.')
    except TimeoutError:
        if self._destroyed:
            raise DestroyedError('Signal has been destroyed')
        raise

def wait_for_connection(self, timeout=DEFAULT_CONNECTION_TIMEOUT):
    '''Wait for the underlying signals to initialize or connect'''
    if timeout is DEFAULT_CONNECTION_TIMEOUT:
        timeout = self.connection_timeout
    # print(f'{print_now()}: waiting for {self.name} to connect within {timeout:.4f} s...')
    start = time.time()
    self._ensure_connected(self._read_pv, self._write_pv, timeout=timeout)
    # print(f'{print_now()}: waited for {self.name} to connect for {time.time() - start:.4f} s.')

EpicsSignalBase.wait_for_connection = wait_for_connection_base
EpicsSignal.wait_for_connection = wait_for_connection
###############################################################################

from ophyd.signal import EpicsSignalBase
# EpicsSignalBase.set_default_timeout(timeout=10, connection_timeout=10)  # old style
EpicsSignalBase.set_defaults(timeout=10, connection_timeout=10)  # new style

import logging

from databroker import Broker

db = Broker.named('ios')

import nslsii
nslsii.configure_base(get_ipython().user_ns, db, publish_documents_with_kafka=True)
# make sure Best Effort Callback does not plot the baseline readings
bec.noplot_streams.append('pgm_energy_monitor')


### comment this out to:
### disable the zmq servce and re-enable best effort callback plotting locally
bec.disable_plots()

from bluesky.callbacks.zmq import Publisher
# pub = Publisher('xf23id-ca.nsls2.bnl.local:5577')
pub = Publisher('localhost:5577')
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

sample_reference = SampleReference(host='xf23id-ca.nsls2.bnl.local', port=7772)
container_reference = ContainerReference(host='xf23id-ca.nsls2.bnl.local', port=7772)

from bluesky.callbacks.mpl_plotting import plot_peak_stats


# Set up default metadata.
RE.md['group'] = ''
RE.md['config'] = {}
RE.md['beamline_id'] = 'IOS'


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
        """
        A MutableMapping which syncs it contents to disk.
        The contents are stored as msgpack-serialized files, with one file per item
        in the mapping.
        Note that when an item is *mutated* it is not immediately synced:
        >>> d['sample'] = {"color": "red"}  # immediately synced
        >>> d['sample']['shape'] = 'bar'  # not immediately synced
        but that the full contents are synced to disk when the PersistentDict
        instance is garbage collected.
        """
        def __init__(self, directory):
            self._directory = directory
            self._file = zict.File(directory)
            self._cache = {}
            super().__init__(self._dump, self._load, self._file)
            self.reload()

            # Similar to flush() or _do_update(), but without reference to self
            # to avoid circular reference preventing collection.
            # NOTE: This still doesn't guarantee call on delete or gc.collect()!
            #       Explicitly call flush() if immediate write to disk required.
            def finalize(zfile, cache, dump):
                zfile.update((k, dump(v)) for k, v in cache.items())

            import weakref
            self._finalizer = weakref.finalize(
                self, finalize, self._file, self._cache, PersistentDict._dump)

        @property
        def directory(self):
            return self._directory

        def __setitem__(self, key, value):
            self._cache[key] = value
            super().__setitem__(key, value)

        def __getitem__(self, key):
            return self._cache[key]

        def __delitem__(self, key):
            del self._cache[key]
            super().__delitem__(key)

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

        def flush(self):
            """Force a write of the current state to disk"""
            for k, v in self.items():
                super().__setitem__(k, v)

        def reload(self):
            """Force a reload from disk, overwriting current cache"""
            self._cache = dict(super().items())

runengine_metadata_dir = appdirs.user_data_dir(appname="bluesky") / Path("runengine-metadata")

# PersistentDict will create the directory if it does not exist
RE.md = PersistentDict(runengine_metadata_dir)

