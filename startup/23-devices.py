#from ophyd.controls import ProsilicaDetector, EpicsSignal, EpicsScaler
from ophyd import EpicsScaler
from ophyd.device import Component as C
from ophyd.device import DynamicDeviceComponent as DDC
from ophyd.scaler import _scaler_fields
from ophyd.signal import waveform_to_string
from time import sleep
import numpy as np

#SPECS Sputter Gun
sputter = EpicsSignal('XF:23ID2-ES{SPECS-PS1}Mode:Opr-Sel', name='sputter')
degas = EpicsSignal('XF:23ID2-ES{SPECS-PS1}Cmd:Degas-Cmd', name='degas')

def sputter_sample_holder(n):
    for ii in range(0,n):
        yield from bps.abs_set(sputter, 2)
        print ('Sputtering...')
        yield from bps.sleep(7200)
        yield from bps.abs_set(sputter, 0)
        print ('Sputtering off, cooling down...')
        yield from bps.sleep(900)

