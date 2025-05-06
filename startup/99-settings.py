#new figure feature
import os
import json
import bluesky.plans as bp
import bluesky.plan_stubs as bps
import bluesky.preprocessors as bpp
from bluesky.suspenders import SuspendBoolHigh
import uuid
from cycler import cycler
import pandas as pd


# Add suspender for shutter
# Note: to clear suspenders use RE.clear_suspenders()
suspend_fe_shutter = SuspendBoolHigh(EpicsSignalRO('XF:23ID-PPS{Sh:FE}Pos-Sts'))
RE.install_suspender(suspend_fe_shutter)

suspend_ds_shutter = SuspendBoolHigh(EpicsSignalRO('XF:23ID2-PPS{PSh}Pos-Sts'))
RE.install_suspender(suspend_ds_shutter)


def relabel_fig(fig, new_label):
    fig.set_label(new_label)
    fig.canvas.manager.set_window_title(fig.get_label())

# NOTE : This now requires DETS as a list
def multi_part_ascan(DETS, motor1, steps, motor2, asc_p):
    for d in steps:
        yield from bps.abs_set(motor1, d, wait=True)
        yield from bp.scan(DETS, motor2, *asc_p)

def open_all_valves(valve_list):
    '''Open all the listed valves

    Parameters
    ----------
    valve_list : sequence
        The valves to open

    '''
    for v in valve_list:
        yield from bps.abs_set(v, 1, group='valve_set')
    yield from bps.wait('valve_set')
    # sleep might not be needed
    yield from bps.sleep(2)

#_edge_fn = os.path.join(os.path.dirname(__file__), 'edge_map.json')
#with open(_edge_fn, 'rt') as fin:
#    EDGE_MAP = json.load(fin)

#def save_edge_map(edge_map, fname=None):
#    if fname is None:
#        fname = _edge_fn
#    with open(fname, 'wt') as fout:
#        json.dump(edge_map, fout, indent=4)



CONTAINER = None
#SAMPLE_MAP = {'sample1': {'name': 'AS-21_Spent', 'pos': 252, 'interesting_edges': []},
#              'sample2': {'name': 'AS-21', 'pos': 259, 'interesting_edges': []},
#              'sample3': {'name': 'AS-4-1_Spent', 'pos': 267, 'interesting_edges': []},
#              'sample4': {'name': '30CoCeO2', 'pos': 276, 'interesting_edges': ['Ce_M', 'Co_L2', 'O_K']},
#              'sample5': {'name': '8CoCeO2', 'pos': 282, 'interesting_edges': ['Ce_M2', 'Co_L', 'O_K']},
#              'sample6': {'name': '2CoCeO2', 'pos': 290, 'interesting_edges': ['Ce_M', 'Co_L', 'O_K2']},
#}

#DET_SETTINGS = {'O_K': {'samplegain': '2', 'sampledecade': '1 nA/V', 'aumeshgain': '5', 'aumeshdecade': '1 nA/V', 'vortex_pos': -220, 'scan_count': 2},
#              'Ce_M': {'samplegain': '2', 'sampledecade': '1 nA/V', 'aumeshgain': '2', 'aumeshdecade': '1 nA/V', 'vortex_pos': -220, 'scan_count': 2},
#              'Co_L': {'samplegain': '1', 'sampledecade': '1 nA/V', 'aumeshgain': '2', 'aumeshdecade': '1 nA/V', 'vortex_pos': -220, 'scan_count': 2},
#          'Co_L2': {'samplegain': '5', 'sampledecade': '1 nA/V', 'aumeshgain': '2', 'aumeshdecade': '1 nA/V', 'vortex_pos': -220, 'scan_count':2},
#          'Ce_M2': {'samplegain': '1', 'sampledecade': '1 nA/V', 'aumeshgain': '2', 'aumeshdecade': '1 nA/V', 'vortex_pos': -220, 'scan_count': 2},
#          'O_K2': {'samplegain': '1', 'sampledecade': '1 nA/V', 'aumeshgain': '5', 'aumeshdecade': '1 nA/V', 'vortex_pos': -220, 'scan_count': 2},
#}



#for k in SAMPLE_MAP:
#    samp = SAMPLE_MAP[k]
#    samp['sample_index'] = k
#    res = list(sample_reference.find(name=samp['name']))
#    if res:
#        sample_reference.update(query={'name': samp['name']},
#                                update=samp
#                                )
#    else:
#        sample_reference.create(**SAMPLE_MAP[k], container=CONTAINER)


def _read_excel(fname, **kwargs):
    df = pd.read_excel(fname, **kwargs)
    # Drop the columns if all values are NaNs:
    df = df.dropna(how='all', axis='columns')
    # Drop the rows if there is at least one NaN value:
    df = df.dropna(how='any', axis='rows')
    return df


def load_samples(fname, container=CONTAINER):
    f = _read_excel(fname)
    SAMPLE_MAP2 = dict()
    loaded_excel = f.T.to_dict().values()
    for entry in loaded_excel:
        samp_idx = entry.pop('sample_index')
        entry['interesting_edges'] = str(entry['interesting_edges']).split(', ')
        entry['sample_index'] = samp_idx
        SAMPLE_MAP2[samp_idx] = entry
#    for k in SAMPLE_MAP2:
#        samp = SAMPLE_MAP2[k]
#        res = list(sample_reference.find(name=samp['name']))
#        if res:
#            sample_reference.update(query={'name': samp['name']},
#                                    update=samp
#                                )
#        else:
#            sample_reference.create(**SAMPLE_MAP2[k], container=container)
    return SAMPLE_MAP2

def load_pey_samples(fname, container=CONTAINER):
    f = _read_excel(fname)
    SAMPLE_MAP2 = dict()
    loaded_excel = f.T.to_dict().values()
    for entry in loaded_excel:
        samp_idx = entry.pop('sample_index')
        entry['interesting_edges'] = str(entry['interesting_edges']).split(', ')
        entry['sample_index'] = samp_idx
        SAMPLE_MAP2[samp_idx] = entry
#    for k in SAMPLE_MAP2:
#        samp = SAMPLE_MAP2[k]
#        res = list(sample_reference.find(name=samp['name']))
#        if res:
#            sample_reference.update(query={'name': samp['name']},
#                                    update=samp
#                                )
#        else:
#            sample_reference.create(**SAMPLE_MAP2[k], container=container)
    return SAMPLE_MAP2


def load_det_settings(fname, container=CONTAINER):
    f = _read_excel(fname, dtype=object)
    SAMPLE_MAP2 = dict()
    loaded_excel = f.T.to_dict().values()
    for entry in loaded_excel:
        edge_idx = entry.pop('edge_index')
        entry['samplegain'] = str(entry['samplegain'])
        entry['aumeshgain'] = str(entry['aumeshgain'])
        entry['pd_gain'] = str(entry['pd_gain'])
        entry['edge_index'] = edge_idx
        SAMPLE_MAP2[edge_idx] = entry
#    for k in SAMPLE_MAP2:
#        samp = SAMPLE_MAP2[k]
#        res = list(sample_reference.find(name=samp['name']))
#        if res:
#            sample_reference.update(query={'name': samp['name']},
#                                    update=samp
#                                    )
#        else:
#            sample_reference.create(**SAMPLE_MAP2[k], container=container)
    return SAMPLE_MAP2

def load_pey_det_settings(fname, container=CONTAINER):
    f = _read_excel(fname, dtype=object)
    SAMPLE_MAP2 = dict()
    loaded_excel = f.T.to_dict().values()
    for entry in loaded_excel:
        edge_idx = entry.pop('edge_index')
        entry['samplegain'] = str(entry['samplegain'])
        entry['aumeshgain'] = str(entry['aumeshgain'])
        entry['pd_gain'] = str(entry['pd_gain'])
        entry['edge_index'] = edge_idx
        SAMPLE_MAP2[edge_idx] = entry
#    for k in SAMPLE_MAP2:
#        samp = SAMPLE_MAP2[k]
#        res = list(sample_reference.find(name=samp['name']))
#        if res:
#            sample_reference.update(query={'name': samp['name']},
#                                    update=samp
#                                    )
#        else:
#            sample_reference.create(**SAMPLE_MAP2[k], container=container)
    return SAMPLE_MAP2

def load_scan_parameters(fname, container=CONTAINER):
    f = _read_excel(fname, dtype=object)
    SAMPLE_MAP2 = dict()
    loaded_excel = f.T.to_dict().values()
    for entry in loaded_excel:
        edge_idx = entry.pop('edge_index')
        entry['edge_index'] = edge_idx
        SAMPLE_MAP2[edge_idx] = entry
    return SAMPLE_MAP2

def load_pey_scan_parameters(fname, container=CONTAINER):
    f = _read_excel(fname, dtype=object)
    SAMPLE_MAP2 = dict()
    loaded_excel = f.T.to_dict().values()
    for entry in loaded_excel:
        edge_idx = entry.pop('edge_index')
        entry['edge_index'] = edge_idx
        SAMPLE_MAP2[edge_idx] = entry
    return SAMPLE_MAP2

def load_all_excel():
    global SAMPLE_MAP, DET_SETTINGS, EDGE_MAP
    SAMPLE_MAP = load_samples('sample_list.xlsx')
    DET_SETTINGS = load_det_settings('det_settings.xlsx')
    EDGE_MAP = load_scan_parameters('scan_parameters.xlsx')
    yield from bps.sleep(1)

# SAMPLE_MAP = load_samples('/home/xf23id2/Desktop/mock_sample.xlsx', container=CONTAINER)

#VORTEX_SETTINGS = {'Cu_L': {'vortex.peaking_time': 0.4,
#                            'vortex.energy_threshold': 0.05,
#                            'mca.rois.roi4.lo_chan': 900,
#                            'mca.rois.roi4.hi_chan': 1200},

#                   'Ni_L': {'vortex.peaking_time': 0.4,
#                            'vortex.energy_threshold': 0.05,
#                            'mca.rois.roi4.lo_chan': 800,
#                            'mca.rois.roi4.hi_chan': 1000},

#                   'Al_K': {'vortex.peaking_time': 0.4,
#                            'vortex.energy_threshold': 0.05,
#                            'mca.rois.roi4.lo_chan': 1500,
#                            'mca.rois.roi4.hi_chan': 1900},

#                   'Fe_L': {'vortex.peaking_time': 0.4,
#                            'vortex.energy_threshold': 0.05,
#                            'mca.rois.roi4.lo_chan': 700,
#                            'mca.rois.roi4.hi_chan': 900},

#                   'Ti_L': {'vortex.peaking_time': 0.4,
#                            'vortex.energy_threshold': 0.05,
#                            'mca.rois.roi4.lo_chan': 400,
#                            'mca.rois.roi4.hi_chan': 600},

#                   'O_K': {'vortex.peaking_time': 0.4,
#                            'vortex.energy_threshold': 0.05,
#                            'mca.rois.roi4.lo_chan': 500,
#                            'mca.rois.roi4.hi_chan': 700},

#                   'O_K_IPFY': {'vortex.peaking_time': 0.4,
#                            'vortex.energy_threshold': 0.05,
#                            'mca.rois.roi3.lo_chan': 500,
#                            'mca.rois.roi3.hi_chan': 700},

#                   'O_K2': {'vortex.peaking_time': 0.4,
#                            'vortex.energy_threshold': 0.05,
#                            'mca.rois.roi4.lo_chan': 500,
#                            'mca.rois.roi4.hi_chan': 700},


#                   'Zn_L': {'vortex.peaking_time': 0.4,
#                            'vortex.energy_threshold': 0.05,
#                            'mca.rois.roi4.lo_chan': 900,
#                            'mca.rois.roi4.hi_chan': 1150},

#                   'Mo_M': {'vortex.peaking_time': 0.4,
#                            'vortex.energy_threshold': 0.05,
#                            'mca.rois.roi4.lo_chan': 400,
#                            'mca.rois.roi4.hi_chan': 700},

#                   'Si_K': {'vortex.peaking_time': 0.4,
#                            'vortex.energy_threshold': 0.05,
#                            'mca.rois.roi4.lo_chan': 1800,
#                            'mca.rois.roi4.hi_chan': 2200},

#                   'Co_L': {'vortex.peaking_time': 0.4,
#                            'vortex.energy_threshold': 0.05,
#                            'mca.rois.roi4.lo_chan': 700,
#                            'mca.rois.roi4.hi_chan': 1000},

#                   'Co_L2': {'vortex.peaking_time': 0.4,
#                            'vortex.energy_threshold': 0.05,
#                            'mca.rois.roi4.lo_chan': 700,
#                            'mca.rois.roi4.hi_chan': 1000},

#                   'Ce_M': {'vortex.peaking_time': 0.4,
#                            'vortex.energy_threshold': 0.05,
#                            'mca.rois.roi4.lo_chan': 900,
#                            'mca.rois.roi4.hi_chan': 1100},


#                   'Ce_M2': {'vortex.peaking_time': 0.4,
#                            'vortex.energy_threshold': 0.05,
#                            'mca.rois.roi4.lo_chan': 900,
#                            'mca.rois.roi4.hi_chan': 1100},

#                   'Ga_L': {'vortex.peaking_time': 0.4,
#                            'vortex.energy_threshold': 0.05,
#                            'mca.rois.roi4.lo_chan': 1000,
#                            'mca.rois.roi4.hi_chan': 1300},
#                   'Rh_L': {'vortex.peaking_time': 0.4,
#                            'vortex.energy_threshold': 0.05,
#                            'mca.rois.roi4.lo_chan': 1600,
#                            'mca.rois.roi4.hi_chan': 1800},
#                   'Mn_L': {'vortex.peaking_time': 0.4,
#                            'vortex.energy_threshold': 0.05,
#                            'mca.rois.roi4.lo_chan': 700,
#                            'mca.rois.roi4.hi_chan': 800},
#}

def XAS_edge_scan(sample_name, edge, md=None):
    '''Run a multi-edge nexafs scan for single sample and edge

    Parameters
    ----------
    sample_name : str
        Base sample name

    sample_position : float
        Postion of sample on manipulator arm

    edge : str
        Key into EDGE_MAP


    '''
    if md is None:
        md = {}
    local_md = {'plan_name': 'edge_ascan'}
    local_md['edge'] = edge
    md = ChainMap(md, local_md)

    e_scan_params = EDGE_MAP[edge]
    # TODO configure the vortex
    det_settings = DET_SETTINGS[edge]
    sample_props = SAMPLE_MAP[sample_name]
#    sample_props = list(sample_manager.find(name=sample_name))
    local_md.update(sample_props)

    # init_group = 'ME_INIT_' + str(uuid.uuid4())
#    yield from bps.abs_set(ioxas_x, sample_props['pos'], wait=True)
#    yield from bps.mov(appes_x, sample_props['pos_x'])
#    yield from bps.mov(appes_y, sample_props['pos_y'])
    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(pgm_energy, e_scan_params['stop'], wait=True)
    yield from bps.abs_set(epu1table, e_scan_params['epu_table'], wait=True)
    yield from bps.abs_set(epu1offset, e_scan_params['epu1offset'], wait=True)
    yield from bps.sleep(15)
    yield from bps.abs_set(m1b1_fp, 186.1)
#    yield from bps.abs_set(feedback, 1, wait=True)
    yield from bps.sleep(5)
#    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(vortex_x, det_settings['vortex_pos'], wait=True)
    yield from bps.abs_set(sample_sclr_gain, det_settings['samplegain'], wait=True)
    yield from bps.abs_set(sample_sclr_decade, det_settings['sampledecade'], wait=True)
    yield from bps.abs_set(aumesh_sclr_gain, det_settings['aumeshgain'], wait=True)
    yield from bps.abs_set(aumesh_sclr_decade, det_settings['aumeshdecade'], wait=True)
    yield from bps.abs_set(sclr_time, det_settings['sclr_time'], wait=True)

 #   yield from open_all_valves(all_valves)
    # yield from bp.wait(init_group)

# TODO make this an ohypd obj!!!!!!
    #caput('XF:23IDA-PPS:2{PSh}Cmd:Opn-Cmd',1)
#   yield from bp.sleep(2)
    # TODO make this an ohypd obj!!!!!!
    # TODO ask stuart
    #caput('XF:23IDA-OP:2{Mir:1A-Ax:FPit}Mtr_POS_SP',50)
    yield from bps.sleep(5)

#    yield from bps.configure(vortex, VORTEX_SETTINGS[edge])
#    yield from bps.sleep(2)
# Using the blue box for PFY:
#    yield from bps.abs_set(vortex.mca.rois.roi4.lo_chan, det_settings['vortex_low'], wait=True)
#    yield from bps.abs_set(vortex.mca.rois.roi4.hi_chan, det_settings['vortex_high'], wait=True)
#    yield from bps.abs_set(vortex.mca.rois.roi3.lo_chan, det_settings['IPFY_low'], wait=True)
#    yield from bps.abs_set(vortex.mca.rois.roi3.hi_chan, det_settings['IPFY_high'], wait=True)
#    yield from bps.abs_set(vortex.mca.preset_real_time, det_settings['vortex_time'], wait=True)

# Using the Xpress3 for PFY:
    yield from bps.abs_set(xs3.channel01.mcaroi04.min_x, det_settings['vortex_low'], wait=True)
    yield from bps.abs_set(xs3.channel01.mcaroi04.size_x, det_settings['vortex_high']-det_settings['vortex_low'], wait=True)
    yield from bps.abs_set(xs3.channel01.mcaroi03.min_x, det_settings['IPFY_low'], wait=True)
    yield from bps.abs_set(xs3.channel01.mcaroi03.size_x, det_settings['IPFY_high']-det_settings['IPFY_low'], wait=True)
#    yield from bps.abs_set(vortex.mca.preset_real_time, det_settings['vortex_time'], wait=True)

    yield from bps.abs_set(sample_sclr_decade, det_settings['sampledecade'], wait=True)
    yield from bps.abs_set(aumesh_sclr_decade, det_settings['aumeshdecade'], wait=True)

    dets = [sclr, xs3, norm_ch4, ring_curr]
    for channel in ['channel01.mcaroi01.total_rbv','channel01.mcaroi02.total_rbv','channel01.mcaroi03.total_rbv','channel01.mcaroi04.total_rbv']:
            getattr(xs3, channel).kind = 'hinted'
    for channel in ['channel01.mcaroi01.total_rbv','channel01.mcaroi02.total_rbv','channel01.mcaroi03.total_rbv']:
            getattr(xs3, channel).kind = 'normal'
    for channel in ['channels.chan2','channels.chan3','channels.chan4']:
        getattr(sclr, channel).kind = 'hinted'
    for channel in ['channels.chan2']:
        getattr(sclr, channel).kind = 'normal'

   
    scan_kwargs = {'start': e_scan_params['stop'],
                   'stop': e_scan_params['start'],
                   'velocity': e_scan_params['velocity'],
                   'deadband': e_scan_params['deadband'],
                   'md': md}
    ret = []
    for j in range(e_scan_params['scan_count']):
#        tmp_pos = sample_props['pos'] + (j-((e_scan_params['scan_count']-1)/2))*e_scan_params['intervals']
#        yield from bps.mov(appes_y, tmp_pos)
#        yield from bps.abs_set(ioxas_x, tmp_pos, wait=True)
        yield from bps.abs_set(feedback, 0, wait=True)
        yield from bps.abs_set(pgm_energy, e_scan_params['stop'], wait=True)
        yield from bps.abs_set(epu1table, e_scan_params['epu_table'], wait=True)
        yield from bps.abs_set(epu1offset, e_scan_params['epu1offset'], wait=True)
        yield from bps.sleep(5)
        yield from bps.abs_set(m1b1_fp, 186.1)
#        yield from bps.abs_set(feedback, 1, wait=True)
        yield from bps.sleep(5)
#        yield from bps.abs_set(feedback, 0, wait=True)
        yield from bps.abs_set(pgm_energy, e_scan_params['stop'], wait=True)
        yield from open_all_valves(all_valves)
        res = yield from bpp.subs_wrapper(E_ramp(dets, **scan_kwargs), {'stop': save_csv})
        yield from bps.abs_set(valve_diag3_close, 1, wait=True)
        yield from bps.abs_set(valve_mir3_close, 1, wait=True)
        yield from bps.sleep(5)
        if res is None:
            res = []
        ret.extend(res)
        if not ret:
            return ret

    return ret

def edge_ascan(sample_name, edge, md=None):
    '''Run a multi-edge nexafs scan for single sample and edge

    Parameters
    ----------
    sample_name : str
        Base sample name

    sample_position : float
        Postion of sample on manipulator arm

    edge : str
        Key into EDGE_MAP


    '''
    if md is None:
        md = {}
    local_md = {'plan_name': 'edge_ascan'}
    local_md['edge'] = edge
    md = ChainMap(md, local_md)
    
#    global SAMPLE_MAP, DET_SETTINGS, EDGE_MAP
#    SAMPLE_MAP=load_samples('sample_list.xlsx')
#    DET_SETTINGS=load_det_settings('det_settings.xlsx')
#    EDGE_MAP=load_scan_parameters('scan_parameters.xlsx')
 
    e_scan_params = EDGE_MAP[edge]
    # TODO configure the vortex
    det_settings = DET_SETTINGS[edge]
    sample_props = SAMPLE_MAP[sample_name]
#    sample_props = list(sample_manager.find(name=sample_name))
    local_md.update(sample_props)

    # init_group = 'ME_INIT_' + str(uuid.uuid4())
    yield from bps.abs_set(ioxas_x, sample_props['pos'], wait=True)
#    yield from bps.abs_set(m3b.pit, sample_props['m3b_pitch'], wait=True)
    yield from bps.abs_set(diag3_y, sample_props['diag3_y'], wait=True)
#    yield from bps.mov(appes_x, sample_props['pos_x'])
#    yield from bps.mov(appes_y, sample_props['pos_y'])
    yield from bps.mov(au_mesh, e_scan_params['au_mesh'])
#    yield from bps.mov(appes_t, sample_props['pos_theta'])
    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(pgm_energy, e_scan_params['e_align'], wait=True)
    yield from bps.abs_set(epu1table, e_scan_params['epu_table'], wait=True)
    yield from bps.abs_set(epu1offset, e_scan_params['epu1offset'], wait=True)
    yield from bps.sleep(30)

##   FOR USING BEAM POSITION ON DIAG2 YAG ##
#    yield from bps.abs_set(m1b1_fp, 150, wait=True)
#    yield from bps.abs_set(feedback, 1, wait=True)
#    yield from bps.sleep(5)
#    yield from bps.abs_set(feedback, 0, wait=True)

##  FOR USING BEAM POSITION WITH FIXED M1B1 FINE PITCH ##
#    yield from bps.abs_set(m1b1_fp, e_scan_params['m1b1_fp'], wait=True)
#    yield from bps.sleep(5)

##  FOR USING BEAM POSITION WITH FIXED M1B1 SETPOINT  ##
    yield from bps.abs_set(m1b1_setpoint, e_scan_params['m1b1_sp'], wait=True)
    yield from bps.abs_set(feedback, 1, wait=True)
    yield from bps.sleep(5)
    yield from bps.abs_set(feedback, 0, wait=True)

##  FOR USING BEAM POSITION USING M1B1 COARSE PITCH  ##
#    yield from bps.abs_set(feedback, 0, wait=True)
#    yield from cp_align(e_scan_params['m1b1_sp'], 0.004)
#    yield from bps.sleep(5)

    yield from bps.abs_set(vortex_x, det_settings['vortex_pos'], wait=True)
    yield from bps.abs_set(sample_sclr_gain, det_settings['samplegain'], wait=True)
    yield from bps.abs_set(sample_sclr_decade, det_settings['sampledecade'], wait=True)
    yield from bps.abs_set(aumesh_sclr_gain, det_settings['aumeshgain'], wait=True)
    yield from bps.abs_set(aumesh_sclr_decade, det_settings['aumeshdecade'], wait=True)
    yield from bps.abs_set(sclr_time, det_settings['sclr_time'], wait=True)
    yield from bps.abs_set(pd_sclr_gain, det_settings['pd_gain'], wait=True)
    yield from bps.abs_set(pd_sclr_decade, det_settings['pd_decade'], wait=True)
 
 #   yield from open_all_valves(all_valves)
    # yield from bp.wait(init_group)

# TODO make this an ohypd obj!!!!!!
    #caput('XF:23IDA-PPS:2{PSh}Cmd:Opn-Cmd',1)
#   yield from bp.sleep(2)
    # TODO make this an ohypd obj!!!!!!
    # TODO ask stuart
    #caput('XF:23IDA-OP:2{Mir:1A-Ax:FPit}Mtr_POS_SP',50)
#    yield from bps.sleep(5)

#    yield from bps.configure(vortex, VORTEX_SETTINGS[edge])
#    yield from bps.sleep(2)
#    yield from bps.abs_set(vortex.mca.rois.roi4.lo_chan, det_settings['vortex_low'], wait=True)
#    yield from bps.abs_set(vortex.mca.rois.roi4.hi_chan, det_settings['vortex_high'], wait=True)
#    yield from bps.abs_set(vortex.mca.rois.roi3.lo_chan, det_settings['IPFY_low'], wait=True)
#    yield from bps.abs_set(vortex.mca.rois.roi3.hi_chan, det_settings['IPFY_high'], wait=True)
#    yield from bps.abs_set(vortex.mca.preset_real_time, det_settings['vortex_time'], wait=True)

# Using the Xpress3 for PFY:
    yield from bps.abs_set(xs3.channel01.mcaroi04.min_x, det_settings['vortex_low'], wait=True)
    yield from bps.abs_set(xs3.channel01.mcaroi04.size_x, det_settings['vortex_high']-det_settings['vortex_low'], wait=True)
    yield from bps.abs_set(xs3.channel01.mcaroi03.min_x, det_settings['IPFY_low'], wait=True)
    yield from bps.abs_set(xs3.channel01.mcaroi03.size_x, det_settings['IPFY_high']-det_settings['IPFY_low'], wait=True)
#    yield from bps.abs_set(vortex.mca.preset_real_time, det_settings['vortex_time'], wait=True)

    yield from bps.abs_set(sample_sclr_decade, det_settings['sampledecade'], wait=True)
    yield from bps.abs_set(aumesh_sclr_decade, det_settings['aumeshdecade'], wait=True)
    yield from bps.abs_set(pd_sclr_decade, det_settings['pd_decade'], wait=True)

#    dets = [sclr, vortex, norm_ch4, ring_curr]
#    for channel in ['mca.rois.roi2.count','mca.rois.roi3.count','mca.rois.roi4.count']:
#            getattr(vortex, channel).kind = 'hinted'
#    for channel in ['mca.rois.roi2.count','mca.rois.roi3.count']:
#            getattr(vortex, channel).kind = 'normal'
#    for channel in ['channels.chan3','channels.chan4']:
#        getattr(sclr, channel).kind = 'hinted'
#    for channel in ['channels.chan2']:
#        getattr(sclr, channel).kind = 'normal'

# Using the Xpress3 with the Vortex:
    dets = [sclr, xs3, norm_ch4, ring_curr]
    for channel in ['channel01.mcaroi01.total_rbv','channel01.mcaroi02.total_rbv','channel01.mcaroi03.total_rbv','channel01.mcaroi04.total_rbv']:
        getattr(xs3, channel).kind = 'hinted'
    for channel in ['channel01.mcaroi01.total_rbv','channel01.mcaroi02.total_rbv']:
        getattr(xs3, channel).kind = 'normal'
    for channel in ['channels.chan2','channels.chan3','channels.chan4']:
        getattr(sclr, channel).kind = 'hinted'
    for channel in ['channels.chan2']:
        getattr(sclr, channel).kind = 'normal'

    scan_kwargs = {'start': e_scan_params['stop'],
                   'stop': e_scan_params['start'],
                   'velocity': e_scan_params['velocity'],
                   'deadband': e_scan_params['deadband'],
                   'md': md}
    ret = []
    for j in range(e_scan_params['scan_count']):
        tmp_pos = sample_props['pos'] + (j-((e_scan_params['scan_count']-1)/2))*e_scan_params['intervals']
#        points = ((e_scan_params['stop'] - e_scan_params['start'])/e_scan_params['velocity']) + 1
        yield from bps.abs_set(ioxas_x, tmp_pos, wait=True)
        yield from bps.abs_set(feedback, 0, wait=True)
        yield from bps.abs_set(pgm_energy, e_scan_params['e_align'], wait=True)
        yield from bps.abs_set(epu1table, e_scan_params['epu_table'], wait=True)
        yield from bps.abs_set(epu1offset, e_scan_params['epu1offset'], wait=True)
        yield from bps.sleep(10)

###   FOR USING BEAM POSITION ON DIAG2 YAG ##
    #    yield from bps.abs_set(m1b1_fp, 150, wait=True)
    #    yield from bps.abs_set(feedback, 1, wait=True)
    #    yield from bps.sleep(5)
    #    yield from bps.abs_set(feedback, 0, wait=True)

##  FOR USING BEAM POSITION WITH FIXED M1B1 FINE PITCH ##
#        yield from bps.abs_set(m1b1_fp, e_scan_params['m1b1_fp'], wait=True)
#        yield from bps.sleep(5)

##  FOR USING BEAM POSITION WITH FIXED M1B1 SETPOINT ##
        yield from bps.abs_set(m1b1_setpoint, e_scan_params['m1b1_sp'], wait=True)
        yield from bps.abs_set(feedback, 1, wait=True)
        yield from bps.sleep(5)
        yield from bps.abs_set(feedback, 0, wait=True)

##  FOR USING BEAM POSITION USING M1B1 COARSE PITCH  ##
#        yield from bps.abs_set(feedback, 0, wait=True)
#        yield from cp_align(e_scan_params['m1b1_sp'], 0.004)
#        yield from bps.sleep(5)

        yield from bps.abs_set(pgm_energy, e_scan_params['stop'], wait=True)
#        yield from bps.sleep(20)
        yield from open_all_valves(all_valves)
#        res = yield from bp.scan(dets, pgm_energy, e_scan_params['start'], e_scan_params['stop'], points)
#        yield from bps.sleep(10)
#        res = yield from bp.list_scan(dets, pgm_energy, np.concatenate([np.linspace(278, 290, 121),np.linspace(290, 300, 51),np.linspace(300, 320, 41),np.linspace(320,380,61)]))      
        res = yield from bpp.subs_wrapper(E_ramp(dets, **scan_kwargs), {'stop': save_csv})
        yield from bps.abs_set(valve_diag3_close, 1, wait=True)
        yield from bps.abs_set(valve_mir3_close, 1, wait=True)
        yield from bps.sleep(5)
        if res is None:
            res = []
        ret.extend(res)
        if not ret:
            return ret

    return ret

def edge_stepscan(sample_name, edge, md=None):
    '''Run a multi-edge nexafs scan for single sample and edge

    Parameters
    ----------
    sample_name : str
        Base sample name

    sample_position : float
        Postion of sample on manipulator arm

    edge : str
        Key into EDGE_MAP


    '''
    if md is None:
        md = {}
    local_md = {'plan_name': 'edge_ascan'}
    local_md['edge'] = edge
    md = ChainMap(md, local_md)

    e_scan_params = EDGE_MAP[edge]
    # TODO configure the vortex
    det_settings = DET_SETTINGS[edge]
    sample_props = SAMPLE_MAP[sample_name]
#    sample_props = list(sample_manager.find(name=sample_name))
    local_md.update(sample_props)

    # init_group = 'ME_INIT_' + str(uuid.uuid4())
    yield from bps.abs_set(ioxas_x, sample_props['pos'], wait=True)
#    yield from bps.abs_set(m3b.pit, sample_props['m3b_pitch'], wait=True)
    yield from bps.abs_set(diag3_y, sample_props['diag3_y'], wait=True)
#    yield from bps.mov(appes_x, sample_props['pos_x'])
#    yield from bps.mov(appes_y, sample_props['pos_y'])
    yield from bps.mov(au_mesh, e_scan_params['au_mesh'])
#    yield from bps.mov(appes_t, sample_props['pos_theta'])
    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(pgm_energy, e_scan_params['e_align'], wait=True)
    yield from bps.abs_set(epu1table, e_scan_params['epu_table'], wait=True)
    yield from bps.abs_set(epu1offset, e_scan_params['epu1offset'], wait=True)
    yield from bps.sleep(40)
#    yield from bps.abs_set(m1b1_fp, 100)
    yield from bps.abs_set(feedback, 1, wait=True)
    yield from bps.sleep(5)
#    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(vortex_x, det_settings['vortex_pos'], wait=True)
    yield from bps.abs_set(sample_sclr_gain, det_settings['samplegain'], wait=True)
    yield from bps.abs_set(sample_sclr_decade, det_settings['sampledecade'], wait=True)
    yield from bps.abs_set(aumesh_sclr_gain, det_settings['aumeshgain'], wait=True)
    yield from bps.abs_set(aumesh_sclr_decade, det_settings['aumeshdecade'], wait=True)
    yield from bps.abs_set(sclr_time, det_settings['sclr_time'], wait=True)
    yield from bps.abs_set(pd_sclr_gain, det_settings['pd_gain'], wait=True)
    yield from bps.abs_set(pd_sclr_decade, det_settings['pd_decade'], wait=True)
 
 #   yield from open_all_valves(all_valves)
    # yield from bp.wait(init_group)

# TODO make this an ohypd obj!!!!!!
    #caput('XF:23IDA-PPS:2{PSh}Cmd:Opn-Cmd',1)
#   yield from bp.sleep(2)
    # TODO make this an ohypd obj!!!!!!
    # TODO ask stuart
    #caput('XF:23IDA-OP:2{Mir:1A-Ax:FPit}Mtr_POS_SP',50)
    yield from bps.sleep(5)

#    yield from bps.configure(vortex, VORTEX_SETTINGS[edge])
#    yield from bps.sleep(2)
#    yield from bps.abs_set(vortex.mca.rois.roi4.lo_chan, det_settings['vortex_low'], wait=True)
#    yield from bps.abs_set(vortex.mca.rois.roi4.hi_chan, det_settings['vortex_high'], wait=True)
#    yield from bps.abs_set(vortex.mca.rois.roi3.lo_chan, det_settings['IPFY_low'], wait=True)
#    yield from bps.abs_set(vortex.mca.rois.roi3.hi_chan, det_settings['IPFY_high'], wait=True)
#    yield from bps.abs_set(vortex.mca.preset_real_time, det_settings['vortex_time'], wait=True)

# Using the Xpress3 for PFY:
    yield from bps.abs_set(xs3.channel01.mcaroi04.min_x, det_settings['vortex_low'], wait=True)
    yield from bps.abs_set(xs3.channel01.mcaroi04.size_x, det_settings['vortex_high']-det_settings['vortex_low'], wait=True)
    yield from bps.abs_set(xs3.channel01.mcaroi03.min_x, det_settings['IPFY_low'], wait=True)
    yield from bps.abs_set(xs3.channel01.mcaroi03.size_x, det_settings['IPFY_high']-det_settings['IPFY_low'], wait=True)
#    yield from bps.abs_set(vortex.mca.preset_real_time, det_settings['vortex_time'], wait=True)

    yield from bps.abs_set(sample_sclr_decade, det_settings['sampledecade'], wait=True)
    yield from bps.abs_set(aumesh_sclr_decade, det_settings['aumeshdecade'], wait=True)
    yield from bps.abs_set(pd_sclr_decade, det_settings['pd_decade'], wait=True)

#    dets = [sclr, vortex, norm_ch4, ring_curr]
#    for channel in ['mca.rois.roi2.count','mca.rois.roi3.count','mca.rois.roi4.count']:
#            getattr(vortex, channel).kind = 'hinted'
#    for channel in ['mca.rois.roi2.count','mca.rois.roi3.count']:
#            getattr(vortex, channel).kind = 'normal'
#    for channel in ['channels.chan3','channels.chan4']:
#        getattr(sclr, channel).kind = 'hinted'
#    for channel in ['channels.chan2']:
#        getattr(sclr, channel).kind = 'normal'

# Using the Xpress3 with the Vortex:
    dets = [sclr, xs3, norm_ch4, ring_curr]
    for channel in ['channel01.mcaroi01.total_rbv','channel01.mcaroi02.total_rbv','channel01.mcaroi03.total_rbv','channel01.mcaroi04.total_rbv']:
        getattr(xs3, channel).kind = 'hinted'
    for channel in ['channel01.mcaroi01.total_rbv','channel01.mcaroi02.total_rbv']:
        getattr(xs3, channel).kind = 'normal'
    for channel in ['channels.chan2','channels.chan3','channels.chan4']:
        getattr(sclr, channel).kind = 'hinted'
    for channel in ['channels.chan2']:
        getattr(sclr, channel).kind = 'normal'

    scan_kwargs = {'start': e_scan_params['stop'],
                   'stop': e_scan_params['start'],
                   'velocity': e_scan_params['velocity'],
                   'deadband': e_scan_params['deadband'],
                   'md': md}
    ret = []
    for j in range(e_scan_params['scan_count']):
        tmp_pos = sample_props['pos'] + (j-((e_scan_params['scan_count']-1)/2))*e_scan_params['intervals']
        points = ((e_scan_params['stop'] - e_scan_params['start'])/e_scan_params['velocity']) + 1
        yield from bps.abs_set(ioxas_x, tmp_pos, wait=True)
        yield from bps.abs_set(feedback, 0, wait=True)
        yield from bps.abs_set(pgm_energy, e_scan_params['e_align'], wait=True)
        yield from bps.abs_set(epu1table, e_scan_params['epu_table'], wait=True)
        yield from bps.abs_set(epu1offset, e_scan_params['epu1offset'], wait=True)
        yield from bps.sleep(5)
#       yield from bps.abs_set(m1b1_fp, 100)
        yield from bps.abs_set(feedback, 1, wait=True)
        yield from bps.sleep(5)
        yield from bps.abs_set(feedback, 0, wait=True)
        yield from bps.sleep(5)
        yield from bps.abs_set(pgm_energy, e_scan_params['start'], wait=True)
        yield from bps.sleep(5)
        yield from bps.abs_set(feedback, 1, wait=True)
        yield from open_all_valves(all_valves)
        res = yield from bp.scan(dets, pgm_energy, e_scan_params['start'], e_scan_params['stop'], points)
#        yield from bps.sleep(10)
#        res = yield from bp.list_scan(dets, pgm_energy, np.concatenate([np.linspace(278, 290, 121),np.linspace(290, 300, 51),np.linspace(300, 320, 41),np.linspace(320,380,61)]))      
#        res = yield from bpp.subs_wrapper(E_ramp(dets, **scan_kwargs), {'stop': save_csv})
        yield from bps.abs_set(valve_diag3_close, 1, wait=True)
        yield from bps.abs_set(valve_mir3_close, 1, wait=True)
        yield from bps.sleep(5)
        if res is None:
            res = []
        ret.extend(res)
        if not ret:
            return ret

    return ret


def pey_edge_ascan(sample_name, edge, md=None):
    '''Run a multi-edge nexafs scan for single sample and edge

    Parameters
    ----------
    sample_name : str
        Base sample name

    sample_position : float
        Postion of sample on manipulator arm

    edge : str
        Key into EDGE_MAP


    '''
    if md is None:
        md = {}
    local_md = {'plan_name': 'edge_ascan'}
    local_md['edge'] = edge
    md = ChainMap(md, local_md)

    pey_e_scan_params = PEY_EDGE_MAP[edge]
    # TODO configure the vortex
    pey_det_settings = PEY_DET_SETTINGS[edge]
    pey_sample_props = PEY_SAMPLE_MAP[sample_name]
#    sample_props = list(sample_manager.find(name=sample_name))
    local_md.update(pey_sample_props)

    # init_group = 'ME_INIT_' + str(uuid.uuid4())
#    yield from bps.abs_set(ioxas_x, sample_props['pos'], wait=True)
#    yield from bps.abs_set(m3b.pit, sample_props['m3b_pitch'], wait=True)
    yield from bps.abs_set(diag3_y, pey_sample_props['diag3_y'], wait=True)
#    yield from bps.mov(appes_x, sample_props['pos_x'])
#    yield from bps.mov(appes_y, sample_props['pos_y'])
    yield from bps.mov(au_mesh, pey_e_scan_params['au_mesh'])
#    yield from bps.mov(appes_t, sample_props['pos_theta'])
    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(pgm_energy, pey_e_scan_params['e_align'], wait=True)
    yield from bps.abs_set(epu1table, pey_e_scan_params['epu_table'], wait=True)
    yield from bps.abs_set(epu1offset, pey_e_scan_params['epu1offset'], wait=True)
    yield from bps.abs_set(m1b1_setpoint, pey_e_scan_params['m1b1_setpoint'], wait=True)
    yield from bps.sleep(25)
#    yield from bps.abs_set(m1b1_fp, 100)
    yield from bps.abs_set(feedback, 1, wait=True)
    yield from bps.sleep(5)
#    yield from bps.abs_set(feedback, 0, wait=True)
#    yield from bps.abs_set(vortex_x, det_settings['vortex_pos'], wait=True)
    yield from bps.abs_set(sample_sclr_gain, pey_det_settings['samplegain'], wait=True)
    yield from bps.abs_set(sample_sclr_decade, pey_det_settings['sampledecade'], wait=True)
    yield from bps.abs_set(aumesh_sclr_gain, pey_det_settings['aumeshgain'], wait=True)
    yield from bps.abs_set(aumesh_sclr_decade, pey_det_settings['aumeshdecade'], wait=True)
    yield from bps.abs_set(sclr_time, pey_det_settings['sclr_time'], wait=True)
    yield from bps.abs_set(pd_sclr_gain, pey_det_settings['pd_gain'], wait=True)
    yield from bps.abs_set(pd_sclr_decade, pey_det_settings['pd_decade'], wait=True)
 
 #   yield from open_all_valves(all_valves)
    # yield from bp.wait(init_group)

# TODO make this an ohypd obj!!!!!!
    #caput('XF:23IDA-PPS:2{PSh}Cmd:Opn-Cmd',1)
#   yield from bp.sleep(2)
    # TODO make this an ohypd obj!!!!!!
    # TODO ask stuart
    #caput('XF:23IDA-OP:2{Mir:1A-Ax:FPit}Mtr_POS_SP',50)
    yield from bps.sleep(5)

    yield from bps.abs_set(sample_sclr_decade, pey_det_settings['sampledecade'], wait=True)
    yield from bps.abs_set(aumesh_sclr_decade, pey_det_settings['aumeshdecade'], wait=True)
    yield from bps.abs_set(pd_sclr_decade, pey_det_settings['pd_decade'], wait=True)
    yield from specs.set_mode('single_count')
    yield from bps.abs_set(specs.cam.kinetic_energy, pey_det_settings['specs_ke'], wait=True)
    yield from bps.abs_set(specs.cam.pass_energy, pey_det_settings['specs_pe'], wait=True)
    yield from bps.abs_set(specs.cam.acquire_time, pey_det_settings['specs_time'], wait=True)
    yield from bps.abs_set(specs.cam.lens_mode, 0, wait=True)


    dets = [specs, sclr, norm_ch4, ring_curr]
    for channel in ['channels.chan3','channels.chan4']:
        getattr(sclr, channel).kind = 'hinted'
    for channel in ['channels.chan2']:
        getattr(sclr, channel).kind = 'normal'
    
   
    scan_kwargs = {'start': pey_e_scan_params['stop'],
                   'stop': pey_e_scan_params['start'],
                   'velocity': pey_e_scan_params['velocity'],
                   'deadband': pey_e_scan_params['deadband'],
                   'md': md}
    ret = []
    for j in range(pey_e_scan_params['scan_count']):
#        tmp_pos = sample_props['pos'] + (j-((e_scan_params['scan_count']-1)/2))*e_scan_params['intervals']
#        points = ((e_scan_params['stop'] - e_scan_params['start'])/e_scan_params['velocity']) + 1
#        yield from bps.abs_set(ioxas_x, tmp_pos, wait=True)
        yield from bps.abs_set(feedback, 0, wait=True)
        yield from bps.abs_set(pgm_energy, pey_e_scan_params['e_align'], wait=True)
        yield from bps.abs_set(epu1table, pey_e_scan_params['epu_table'], wait=True)
        yield from bps.abs_set(epu1offset, pey_e_scan_params['epu1offset'], wait=True)
        yield from bps.abs_set(m1b1_setpoint, pey_e_scan_params['m1b1_setpoint'], wait=True)
        yield from bps.sleep(15)
#       yield from bps.abs_set(m1b1_fp, 100)
        yield from bps.abs_set(feedback, 1, wait=True)
        yield from bps.sleep(10)
        yield from bps.abs_set(feedback, 0, wait=True)
#        yield from bps.sleep(5)
        yield from bps.abs_set(pgm_energy, pey_e_scan_params['stop'], wait=True)
        yield from open_all_valves(all_valves)
#        res = yield from bp.scan(dets, pgm_energy, e_scan_params['start'], e_scan_params['stop'], points)
#        yield from bps.sleep(10)
#        res = yield from bp.list_scan(dets, pgm_energy, np.concatenate([np.linspace(278, 290, 121),np.linspace(290, 300, 51),np.linspace(300, 320, 41),np.linspace(320,380,61)]))      
        res = yield from bpp.subs_wrapper(E_ramp(dets, **scan_kwargs), {'stop': save_pey_csv})
        yield from bps.abs_set(valve_diag3_close, 1, wait=True)
        yield from bps.abs_set(valve_mir3_close, 1, wait=True)
        yield from bps.sleep(5)
        if res is None:
            res = []
        ret.extend(res)
        if not ret:
            return ret

    return ret

def pass_filter(sample_name, edge):
    return edge in SAMPLE_MAP[sample_name]['interesting_edges']

def pey_pass_filter(sample_name, edge):
    return edge in PEY_SAMPLE_MAP[sample_name]['interesting_edges']


def multi_sample_edge(*, edge_list=None, sample_list=None):
    global SAMPLE_MAP, DET_SETTINGS, EDGE_MAP
    SAMPLE_MAP=load_samples('sample_list.xlsx')
    DET_SETTINGS=load_det_settings('det_settings.xlsx')
    EDGE_MAP=load_scan_parameters('scan_parameters.xlsx')
    if sample_list is None:
        sample_list = list(SAMPLE_MAP)
    if edge_list is None:
        edge_list = list(EDGE_MAP)
#    edge_list = sorted(edge_list, key=lambda k: EDGE_MAP[k]['start'])
    cy = cycler('edge', edge_list) * cycler('sample_name', sample_list)
    for inp in cy:
        if pass_filter(**inp):
            yield from edge_ascan(**inp)
    yield from bps.abs_set(valve_diag3_close, 1)
    yield from bps.abs_set(valve_mir3_close, 1)

def multi_step_scan(*, edge_list=None, sample_list=None):
    if sample_list is None:
        sample_list = list(SAMPLE_MAP)
    if edge_list is None:
        edge_list = list(EDGE_MAP)
#    edge_list = sorted(edge_list, key=lambda k: EDGE_MAP[k]['start'])
    cy = cycler('edge', edge_list) * cycler('sample_name', sample_list)
    for inp in cy:
        if pass_filter(**inp):
            yield from edge_stepscan(**inp)
    yield from bps.abs_set(valve_diag3_close, 1)
    yield from bps.abs_set(valve_mir3_close, 1)


def multi_pey_edge(*, edge_list=None, sample_list=None):
    if sample_list is None:
        sample_list = list(PEY_SAMPLE_MAP)
    if edge_list is None:
        edge_list = list(PEY_EDGE_MAP)
#    edge_list = sorted(edge_list, key=lambda k: EDGE_MAP[k]['start'])
    cy = cycler('edge', edge_list) * cycler('sample_name', sample_list)
    for inp in cy:
        if pey_pass_filter(**inp):
            yield from pey_edge_ascan(**inp)
    yield from bps.abs_set(valve_diag3_close, 1)
    yield from bps.abs_set(valve_mir3_close, 1)



def multi_edge(*, edge_list=None, sample_list=None):
    if sample_list is None:
        sample_list = list(SAMPLE_MAP)
    if edge_list is None:
        edge_list = list(EDGE_MAP)
#    edge_list = sorted(edge_list, key=lambda k: EDGE_MAP[k]['start'])
    cy = cycler('edge', edge_list) * cycler('sample_name', sample_list)
    for inp in cy:
        if pass_filter(**inp):
            yield from XAS_edge_scan(**inp)
    yield from bps.abs_set(valve_diag3_close, 1)
    yield from bps.abs_set(valve_mir3_close, 1)


def dummy_edge_scan(sample_name, edge, md=None):
    from bluesky.examples import det, motor, det2

    if md is None:
        md = {}
    local_md = {'plan_name': 'edge_ascan'}
    md = ChainMap(md, local_md)

    e_scan_params = EDGE_MAP[edge]
    # TODO configure the vortex

    sample_props = SAMPLE_MAP[sample_name]
    # sample_props = list(sample_manager.find(sample_name))[0]
    local_md.update(sample_props)
    lp_list = []
    for n in ['det', 'det2']:
        fig = plt.figure(edge + ': ' + n)
        lp = bs.callbacks.LivePlot(n, 'motor', fig=fig)
        lp_list.append(lp)
    yield from bpp.subs_wrapper(bp.relative_scan([det, det2], motor, -5, 5, 15, md=md),
                               lp_list)
def finish_XAS():
    yield from bps.abs_set(ioxas_x, 0, wait=True)
    yield from bps.abs_set(ioxas_ll_close, 1)
    yield from bps.abs_set(vortex_x, 0, wait=True)

#def save_csv(name, stop_doc):
#    required_columns=['pgm_energy_readback', 'sclr_ch3', 'sclr_ch4', 'norm_ch4', 'vortex_mca_rois_roi4_count', 'vortex_mca_rois_roi3_count']
#    h = db[stop_doc['run_start']]
#    df = db.get_table(h)
#    fn = '{name}_{edge}_{scan_id}.csv'.format(**h.start)

    # verify the required columns are there
#    in_list = True
#    for element in required_columns:
#        if element not in df.columns:
#            in_list = False

#    if in_list:
#        df.to_csv(fn,columns=required_columns)
#    else:
#        f = open(fn, "a")
#        f.write("Error, missing columns")
#        f.write("Got: {}\nExpected: {}".format(df.columns, required_columns))
#        f.close()

def save_csv(edge, stop_doc):
#    required_columns=['pgm_energy_readback', 'sclr_ch2', 'sclr_ch3', 'sclr_ch4', 'norm_ch4', 'vortex_mca_rois_roi4_count', 'vortex_mca_rois_roi3_count']
    required_columns=['pgm_energy_readback', 'sclr_ch2', 'sclr_ch3', 'sclr_ch4', 'norm_ch4', 'TFY', 'IPFY', 'PFY']
    h = db[stop_doc['run_start']]
    df = db.get_table(h)
    fn = '{name}_{edge}_{scan_id}.csv'.format(**h.start)

    # verify the required columns are there
    in_list = True
    for element in required_columns:
        if element not in df.columns:
            in_list = False

    if in_list:
        df.to_csv(fn,columns=required_columns)
    else:
        f = open(fn, "a")
        f.write("Error, missing columns")
        f.write("Got: {}\nExpected: {}".format(df.columns, required_columns))
        f.close()

def save_pey_csv(edge, stop_doc):
    required_columns=['pgm_energy_readback', 'sclr_ch2', 'sclr_ch3', 'sclr_ch4', 'norm_ch4', 'specs_count']
    h = db[stop_doc['run_start']]
    df = db.get_table(h)
    fn = '{name}_{edge}_{scan_id}.csv'.format(**h.start)
#    fn = '{edge}_{scan_id}.csv'.format(**h.start)


    # verify the required columns are there
    in_list = True
    for element in required_columns:
        if element not in df.columns:
            in_list = False

    if in_list:
        df.to_csv(fn,columns=required_columns)
    else:
        f = open(fn, "a")
        f.write("Error, missing columns")
        f.write("Got: {}\nExpected: {}".format(df.columns, required_columns))
        f.close()



#def save_csv_callback(name, doc):

#    if name != 'stop':
#        return
#    print(doc)
#    start_doc = doc['run_start']
#    hdr = db[start_doc]
#    if
#    table = db.get_table(hdr)

#    fn_template = '/tmp/scan_{name}.csv'
#    file_name = fn_template.format(**hdr['start'])
#    table.to_csv(file_name, index=False)
#    print('saved CVS to: {!r}'.format(file_name))

## Test
def cp_align(centroid, jog):

    counter = 0
    yield from bps.abs_set(m1b1_cp_jog_sp, jog, wait=True)
    centroid_rb = yag_centroid.read()['yag_centroid']['value']

    while (abs(centroid-centroid_rb) > 3.0):
        if (centroid_rb-centroid) > 1.0:
            yield from bps.abs_set(m1b1_cp_jog_ng, 1, wait=True)
            yield from bps.abs_set(m1b1_cp_mv, 1, wait=True)
            yield from bps.sleep(3)
        else:
            yield from bps.abs_set(m1b1_cp_jog_ps, 1, wait=True)
            yield from bps.abs_set(m1b1_cp_mv, 1, wait=True)
            yield from bps.sleep(3)
        centroid_rb = yag_centroid.read()['yag_centroid']['value']

        counter = counter + 1
        if counter>10:
            break

