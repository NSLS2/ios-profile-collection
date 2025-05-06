from ophyd import EpicsMotor, PVPositioner, PVPositionerPC, EpicsSignal, EpicsSignalRO, Device
from ophyd import Component as Cpt, FormattedComponent as FmtCpt
from ophyd import (EpicsMCA, EpicsDXP)

# Vortex MCA

class Vortex(Device):
    mca = Cpt(EpicsMCA, 'mca1')
    vortex = Cpt(EpicsDXP, 'dxp1:')

    @property
    def trigger_signals(self):
        return [self.mca.erase_start]

    def describe(self):
        ret = super().describe()
        ret["vortex_mca_spectrum"].setdefault("dtype_str", "<i8")  # Update specificity for dtype as 'array'
        return ret
