# Parameterized edge scans for Queueserver and for the Skybeam XAS model.
#
# edge_ascan(sample_name, edge) (99-settings.py) looks up its values in the spreadsheets
# (SAMPLE_MAP, DET_SETTINGS, EDGE_MAP). A queue item can only carry plain arguments, so these
# plans take the values directly, and edge_ascan is a thin wrapper around xas_edge_ascan. The
# steps and their order are those of the original edge_ascan.
#
# The argument names differ from the names of the devices of this profile (au_mesh_pos, diag3_pos,
# epu_offset, dwell_s) so that an argument never shadows a device.
#
# start and stop are the values of the spreadsheet (start < stop): the energy is ramped from the
# stop energy down to the start energy.

from collections import ChainMap


def _close_valves():
    '''Close the diag3 and mir3 valves.'''
    yield from bps.abs_set(valve_diag3_close, 1, wait=True)
    yield from bps.abs_set(valve_mir3_close, 1, wait=True)


def _set_amplifier(gain_signal, gain, decade_signal, decade):
    if gain is not None:
        yield from bps.abs_set(gain_signal, gain, wait=True)
    if decade is not None:
        yield from bps.abs_set(decade_signal, decade, wait=True)


def _align_beam(e_align, epu_table, epu_offset, m1b1_sp, settle_s):
    '''Feedback off, energy to e_align, EPU table and offset, wait, mirror setpoint, then run the
    feedback for 5 s and turn it off again.'''
    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(pgm_energy, e_align, wait=True)
    yield from bps.abs_set(epu1table, epu_table, wait=True)
    yield from bps.abs_set(epu1offset, epu_offset, wait=True)
    yield from bps.sleep(settle_s)
    yield from bps.abs_set(m1b1_setpoint, m1b1_sp, wait=True)
    yield from bps.abs_set(feedback, 1, wait=True)
    yield from bps.sleep(5)
    yield from bps.abs_set(feedback, 0, wait=True)


def _valves_after(close_valves_after):
    '''Plan that runs after a scan that completed: the valves stay open unless asked.'''
    if close_valves_after:
        yield from _close_valves()


def xas_edge_ascan(*, start, stop, velocity, deadband,
                   e_align, epu_table, epu_offset, m1b1_sp, au_mesh_pos,
                   sample_pos=None, diag3_pos=None, vortex_pos=None,
                   samplegain=None, sampledecade=None,
                   aumeshgain=None, aumeshdecade=None,
                   pd_gain=None, pd_decade=None, dwell_s=None,
                   pfy_min_x=None, pfy_size_x=None, ipfy_min_x=None, ipfy_size_x=None,
                   scan_count=1, intervals=0,
                   close_valves_after=True, save_csv_on_stop=False, md=None):
    '''Edge scan of a sample with the values given as arguments.

    The steps are those of edge_ascan: sample position and diag3_y, au_mesh, the beam alignment
    (feedback off, energy to e_align, EPU table and offset, wait, mirror setpoint, feedback on for
    5 s and off), the detector settings, then for each of scan_count repeats the sample position
    (``sample_pos + (j - (scan_count - 1) / 2) * intervals``), the alignment again, the stop
    energy, the valves open and an energy ramp from stop down to start.

    The diag3 and mir3 valves are closed if the plan is aborted or fails, and after it completes
    if close_valves_after is true.

    Parameters
    ----------
    start, stop : float
        Energy range in eV; the ramp runs from ``stop`` down to ``start``.
    velocity, deadband : float
        Arguments of E_ramp.
    e_align : float
        Energy at which the beam is aligned.
    epu_table, epu_offset : int, float
        EPU table (4: first harmonic, 5: third harmonic) and energy offset.
    m1b1_sp : float
        Setpoint of the mirror feedback (m1b1_setpoint).
    au_mesh_pos : float
        Position of the gold mesh (mm).
    sample_pos, diag3_pos : float, optional
        Positions of ioxas_x and diag3_y (mm). Without ``sample_pos`` the sample is not moved
        and the repeats are not spread.
    vortex_pos : float, optional
        Position of vortex_x (mm).
    samplegain, sampledecade, aumeshgain, aumeshdecade, pd_gain, pd_decade : str, optional
        Settings of the three amplifiers.
    dwell_s : float, optional
        Scaler time (sclr_time).
    pfy_min_x, pfy_size_x, ipfy_min_x, ipfy_size_x : float, optional
        Windows of the Xspress3 ROIs 4 (PFY) and 3 (IPFY), in channels.
    scan_count, intervals : int, float
        Number of scans and the distance between them (mm). The Skybeam XAS model calls the plan
        once per repeat and leaves these at their defaults.
    close_valves_after : bool
        Close the diag3 and mir3 valves when the plan completes.
    save_csv_on_stop : bool
        Write a CSV file when a run stops (needs ``name`` and ``edge`` in the metadata).
    md : dict, optional
        Metadata for the runs.
    '''
    md = ChainMap({} if md is None else md, {'plan_name': 'xas_edge_ascan'})

    def scan():
        if sample_pos is not None:
            yield from bps.abs_set(ioxas_x, sample_pos, wait=True)
        if diag3_pos is not None:
            yield from bps.abs_set(diag3_y, diag3_pos, wait=True)
        yield from bps.mov(au_mesh, au_mesh_pos)
        yield from _align_beam(e_align, epu_table, epu_offset, m1b1_sp, 30)

        if vortex_pos is not None:
            yield from bps.abs_set(vortex_x, vortex_pos, wait=True)
        yield from _set_amplifier(sample_sclr_gain, samplegain, sample_sclr_decade, sampledecade)
        yield from _set_amplifier(aumesh_sclr_gain, aumeshgain, aumesh_sclr_decade, aumeshdecade)
        if dwell_s is not None:
            yield from bps.abs_set(sclr_time, dwell_s, wait=True)
        yield from _set_amplifier(pd_sclr_gain, pd_gain, pd_sclr_decade, pd_decade)
        for signal, value in ((xs3.channel01.mcaroi04.min_x, pfy_min_x),
                              (xs3.channel01.mcaroi04.size_x, pfy_size_x),
                              (xs3.channel01.mcaroi03.min_x, ipfy_min_x),
                              (xs3.channel01.mcaroi03.size_x, ipfy_size_x)):
            if value is not None:
                yield from bps.abs_set(signal, value, wait=True)
        # the decades are set once more, as in edge_ascan
        for signal, value in ((sample_sclr_decade, sampledecade),
                              (aumesh_sclr_decade, aumeshdecade),
                              (pd_sclr_decade, pd_decade)):
            if value is not None:
                yield from bps.abs_set(signal, value, wait=True)

        dets = [sclr, xs3, norm_ch4, ring_curr]
        for channel in ['channel01.mcaroi01.total_rbv', 'channel01.mcaroi02.total_rbv',
                        'channel01.mcaroi03.total_rbv', 'channel01.mcaroi04.total_rbv']:
            getattr(xs3, channel).kind = 'hinted'
        for channel in ['channel01.mcaroi01.total_rbv', 'channel01.mcaroi02.total_rbv']:
            getattr(xs3, channel).kind = 'normal'
        for channel in ['channels.chan2', 'channels.chan3', 'channels.chan4']:
            getattr(sclr, channel).kind = 'hinted'
        for channel in ['channels.chan2']:
            getattr(sclr, channel).kind = 'normal'

        ret = []
        for j in range(scan_count):
            if sample_pos is not None:
                tmp_pos = sample_pos + (j - ((scan_count - 1) / 2)) * intervals
                yield from bps.abs_set(ioxas_x, tmp_pos, wait=True)
            yield from _align_beam(e_align, epu_table, epu_offset, m1b1_sp, 10)
            yield from bps.abs_set(pgm_energy, stop, wait=True)
            yield from bps.sleep(3)
            yield from open_all_valves(all_valves)
            ramp = E_ramp(dets, start=stop, stop=start, velocity=velocity,
                          deadband=deadband, md=md)
            if save_csv_on_stop:
                ramp = bpp.subs_wrapper(ramp, {'stop': save_csv})
            res = yield from ramp
            yield from bps.sleep(5)
            if res is None:
                res = []
            ret.extend(res)
            if not ret:
                return ret
        return ret

    return (yield from bpp.contingency_wrapper(
        scan(),
        except_plan=lambda exc: _close_valves(),
        else_plan=lambda: _valves_after(close_valves_after)))


def xas_pd_ascan(*, start, stop, velocity, deadband,
                 e_align, epu_table, epu_offset, m1b1_sp, au_mesh_pos,
                 pd_diag3_pos, sample_out_x,
                 pd_gain=None, pd_decade=None, aumeshgain=None, aumeshdecade=None,
                 dwell_s=None, close_valves_after=True, md=None):
    '''Energy scan of the photodiode, with the beam set up as for an edge.

    Anticipated from PD_scan and edge_ascan; to be reviewed with the IOS staff. The sample bar is
    fully retracted (``ioxas_x`` to ``sample_out_x``), the photodiode is put in the beam
    (``diag3_y`` to ``pd_diag3_pos``), the beam is aligned as in xas_edge_ascan, and the energy is
    ramped from ``stop`` down to ``start`` with the detectors of PD_scan (the scaler channels
    chan3 and chan2 hinted, and the ring current). No fluorescence detector is used.

    The valves are closed if the plan is aborted or fails, and after it completes if
    close_valves_after is true.
    '''
    md = ChainMap({} if md is None else md, {'plan_name': 'xas_pd_ascan'})

    def scan():
        yield from bps.abs_set(ioxas_x, sample_out_x, wait=True)
        yield from bps.abs_set(diag3_y, pd_diag3_pos, wait=True)
        yield from bps.mov(au_mesh, au_mesh_pos)
        yield from _align_beam(e_align, epu_table, epu_offset, m1b1_sp, 30)

        yield from _set_amplifier(pd_sclr_gain, pd_gain, pd_sclr_decade, pd_decade)
        yield from _set_amplifier(aumesh_sclr_gain, aumeshgain, aumesh_sclr_decade, aumeshdecade)
        if dwell_s is not None:
            yield from bps.abs_set(sclr_time, dwell_s, wait=True)

        for channel in ['channels.chan3', 'channels.chan2']:
            getattr(sclr, channel).kind = 'hinted'
        for channel in ['channels.chan4']:
            getattr(sclr, channel).kind = 'normal'
        dets = [sclr, ring_curr]

        yield from bps.abs_set(pgm_energy, stop, wait=True)
        yield from bps.sleep(3)
        yield from open_all_valves(all_valves)
        res = yield from E_ramp(dets, start=stop, stop=start, velocity=velocity,
                                deadband=deadband, md=md)
        yield from bps.sleep(5)
        return [] if res is None else res

    return (yield from bpp.contingency_wrapper(
        scan(),
        except_plan=lambda exc: _close_valves(),
        else_plan=lambda: _valves_after(close_valves_after)))
