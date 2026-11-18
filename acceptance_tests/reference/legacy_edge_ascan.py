# The edge_ascan plan as it was before it became a wrapper around xas_edge_ascan (startup/99-settings.py,
# up to 2026-11-04). It is a reference for test_xas_edge_plans.py, which checks that the new
# edge_ascan runs the same steps in the same order. It is not part of the profile.

def legacy_edge_ascan(sample_name, edge, md=None):
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
#    dets = [sclr, ring_curr]
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
        yield from bps.sleep(3)
        yield from open_all_valves(all_valves)
#        res = yield from bp.scan(dets, pgm_energy, e_scan_params['start'], e_scan_params['stop'], points)
#        yield from bps.sleep(10)
#        res = yield from bp.list_scan(dets, pgm_energy, np.concatenate([np.linspace(278, 290, 121),np.linspace(290, 300, 51),np.linspace(300, 320, 41),np.linspace(320,380,61)]))      
        res = yield from bpp.subs_wrapper(E_ramp(dets, **scan_kwargs), {'stop': save_csv})
#        yield from bps.abs_set(valve_diag3_close, 1, wait=True)
#        yield from bps.abs_set(valve_mir3_close, 1, wait=True)
        yield from bps.sleep(5)
        if res is None:
            res = []
        ret.extend(res)
        if not ret:
            return ret

    return ret

