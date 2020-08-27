from time import sleep
import numpy as np
from matplotlib import pyplot as plt


def user_checkin():
    proposal_id = input('Enter your proposal number:  ')
    PI_name = input('Enter the last name of the PI:  ')
    endstation = input('Which endstation (APPES or IOXAS)?  ')
    cycle = input('Run cycle?  ')

    RE.md['PI'] = PI_name
    RE.md['proposal_id'] = proposal_id
    RE.md['endstation'] = endstation
    RE.md['cycle'] = cycle

def user_checkout():
    del RE.md['PI']
#    RE.md['group'] = ''
    del RE.md['proposal_id']
    del RE.md['endstation']
    del RE.md['cycle']

def save_xas_csv(first_id, last_id, exptype = 'normal'):
    for scanid in range(first_id,last_id+1,1):
        if exptype == 'normal':
            df = db[scanid].table()
            df.to_csv('~/User_Data/Marschilok/July2020/pristine_sample_PP_C_K1_%d.csv' % scanid, columns=['pgm_energy_readback', 'sclr_ch2', 'sclr_ch3', 'sclr_ch4', 'norm_ch4', 'vortex_mca_rois_roi3_count', 'vortex_mca_rois_roi4_count'], index=True)
        elif exptype == 'PD':
            df = db[scanid].table()
            df.to_csv('~/User_Data/Hunt/3rd_order/PD_Scan_%d.csv' % scanid, columns=['pgm_energy_readback', 'sclr_ch2', 'sclr_ch3', 'sclr_ch4'], index=False)
        elif exptype == 'PEY':
            df = db[scanid].table()
            df.to_csv('~/User_Data/Hunt/3rd_order/PEY_Scan_%d.csv' % scanid, columns=['pgm_energy_readback', 'sclr_ch2', 'sclr_ch3', 'sclr_ch4', 'specs_count'], index=False)
        else:
            print('Unknown file type')


def save_xas_csv_short(first_id, last_id):
        for scanid in range(first_id,last_id+1,1):
                df = db.get_table(db[scanid])
                #fn = 'csv_data/Scan_{scan_id}.csv'.format(db[scanid].start)
#                df.to_csv('~/User_Data/Hunt/Carbon_contamination/PD_Scan_%d.csv' % scanid, columns=['pgm_energy_readback', 'sclr_ch2', 'sclr_ch3'])
                df.to_csv('~/User_Data/May/PD_Scan_%d.csv' % scanid, columns=['pgm_energy_readback', 'sclr_ch2', 'sclr_ch3', 'sclr_ch4'])

def save_all(first_id, last_id):
        for scanid in range(first_id,last_id+1,1):
                df = db.get_table(db[scanid])
                #fn = 'csv_data/Scan_{scan_id}.csv'.format(db[scanid].start)
                df.to_csv('~/User_Data/Salmeron/Feb2020/Scan_%d.csv' % scanid, columns=['time', 'pgm_energy_readback', 'm1b1_fp', 'm3b_pit_setpoint', 'sclr_ch2', 'sclr_ch3', 'sclr_ch4', 'norm_ch4', 'vortex_mca_rois_roi1_count', 'vortex_mca_rois_roi2_count', 'vortex_mca_rois_roi3_count', 'vortex_mca_rois_roi4_count'])
#                df.to_csv('~/User_Data/Salmeron/Scan_%d.csv' % scanid)



def save_xas_csv_time(first_id, last_id):
        for scanid in range(first_id,last_id+1,1):
                df = db.get_table(db[scanid])
                #fn = 'csv_data/Scan_{scan_id}.csv'.format(db[scanid].start)
                df.to_csv('~/User_Data/Hunt/Carbon_contamination/Time_Scan_%d.csv' % scanid, columns=['time', 'sclr_ch2', 'sclr_ch3'])

def save_xas_csv_all(first_id, last_id):
        for scanid in range(first_id,last_id+1,1):
                df = db.get_table(db[scanid])
#                df['Norm'] = df['sclr_ch4']/df['sclr_ch3']
                #fn = 'csv_data/Scan_{scan_id}.csv'.format(db[scanid].start)
                df.to_csv('~/User_Data/Wen/Scan_%d.csv' % scanid, columns=['pgm_energy_readback', 'ioxas_x', 'sclr_ch2', 'sclr_ch3', 'sclr_ch4', 'vortex_mca_rois_roi2_count',  'vortex_mca_rois_roi3_count', 'vortex_mca_rois_roi4_count'], index=False)


def liveplot_photodiode():
     sclr.hints = {'fields': ['sclr_ch2']} 

def liveplot_xas():
     sclr.hints = {'fields': ['sclr_ch4']} 

def liveplot_aumesh():
     sclr.hints = {'fields': ['sclr_ch3']} 

def plot_PD_EnergyScan(scanid1,scanid2,label):
    plt.figure(label)
    label = plt.gca()
    for i in range (scanid1, scanid2+1):
        df1 = db.get_table(db[i])
        df1.plot(x = 'pgm_energy_readback', y = 'sclr_ch2', label = str(i), ax=label)

def plot_Aumesh(scanid1,scanid2,label):
    plt.figure(label)
    label = plt.gca()
    for i in range (scanid1, scanid2+1):
        df1 = db.get_table(db[i])
        df1.plot(x = 'pgm_energy_readback', y = 'sclr_ch3', label = str(i), ax=label)


def plot_PD_TimeScan(scanid1,scanid2,label):
    plt.figure(label)
    label = plt.gca()
    for i in range (scanid1, scanid2+1):
        df1 = db.get_table(db[i])
        df1.plot(x = 'time', y = 'sclr_ch2', label = str(i), ax=label)

def plot_PFY_TimeScan(scanid1,scanid2,label):
    plt.figure(label)
    label = plt.gca()
    for i in range (scanid1, scanid2+1):
        df1 = db.get_table(db[i])
        df1.plot(x = 'time', y = 'vortex_mca_rois_roi4_count', label = str(i), ax=label)

def plot_epugap(scanid1,scanid2,label):
    plt.figure(label)
    label = plt.gca()
    for i in range (scanid1, scanid2+1):
        df1 = db.get_table(db[i])
        df1['Norm'] = df1['sclr_ch2']
        df1.plot(x = 'epu1_gap_readback', y = 'Norm', label = str(i), ax=label)

def plot_sample_map_tey(scanid1,scanid2,label):
        plt.figure(label)
        label = plt.gca()
        for i in range (scanid1, scanid2+1):
                df1 = db.get_table(db[i])
                df1.plot(x = 'ioxas_x', y = 'sclr_ch4', label = str(i), ax=label)

def plot_sample_map_pfy(scanid1,scanid2,label):
        plt.figure(label)
        label = plt.gca()
        for i in range (scanid1, scanid2+1):
                df1 = db.get_table(db[i])
                df1.plot(x = 'ioxas_x', y = 'vortex_mca_rois_roi4_count', label = str(i), ax=label)

# Composite plotting routines

def plot_norm_async_xas(scanid1,scanid2,normid,label,scan_type='TEY',normto1='Y'):
        plt.figure(label)
        label = plt.gca()
        dfn = db.get_table(db[normid])
        for i in range (scanid1, scanid2+1):
                df1 = db.get_table(db[i])
                if ((scan_type == 'TEY') or (scan_type == 'tey')):
                       df1['Norm'] = df1['sclr_ch4']/dfn['sclr_ch2']
                elif ((scan_type == 'PFY') or (scan_type == 'pfy')):
                       df1['Norm'] = df1['vortex_mca_rois_roi4_count']/dfn['sclr_ch2']
                elif ((scan_type == 'TFY') or (scan_type == 'tfy')):
                       df1['Norm'] = df1['vortex_mca_rois_roi1_count']/dfn['sclr_ch2']
                elif ((scan_type == 'TRANS') or (scan_type == 'trans')):
                       df1['Norm'] = -1*np.log(df1['sclr_ch4']/dfn['sclr_ch4'])
                elif ((scan_type == 'PEY') or (scan_type == 'pey')):
                       df1['Norm'] = df1['specs_count']/dfn['sclr_ch2']
                elif ((scan_type == 'IPFY') or (scan_type == 'ipfy')):
                       df1['Norm'] = 1/(df1['vortex_mca_rois_roi3_count']/dfn['sclr_ch2'])
                
                if (normto1 == 'Y' or normto1 == 'y' or normto1 == 'yes' or normto1 == 'YES'):
                       df1['Norm'] = df1['Norm']-min(df1['Norm'])
                       df1['Norm'] = df1['Norm']/max(df1['Norm'])

                df1.plot(x = 'pgm_energy_readback', y = 'Norm', label = str(i), ax=label)

def plot_norm_xas(scanid1,scanid2,label,scan_type='TEY',normto1='Y'):
        plt.figure(label)
        label = plt.gca()
        for i in range (scanid1, scanid2+1):
                df1 = db.get_table(db[i])
                if ((scan_type == 'TEY') or (scan_type == 'tey')):
                       df1['Norm'] = df1['sclr_ch4']/df1['sclr_ch3']
                elif ((scan_type == 'PFY') or (scan_type == 'pfy')):
                       df1['Norm'] = df1['vortex_mca_rois_roi4_count']/df1['sclr_ch3']
                elif ((scan_type == 'TFY') or (scan_type == 'tfy')):
                       df1['Norm'] = df1['vortex_mca_rois_roi1_count']/df1['sclr_ch3']
                elif ((scan_type == 'IPFY') or (scan_type == 'ipfy')):
                       df1['Norm'] = 1/(df1['vortex_mca_rois_roi3_count']/df1['sclr_ch3'])
                elif ((scan_type == 'PEY') or (scan_type == 'pey')):
                       df1['Norm'] = df1['specs_count']/df1['sclr_ch3']

                if (normto1 == 'Y' or normto1 == 'y' or normto1 == 'yes' or normto1 == 'YES'):
                       df1['Norm'] = df1['Norm']-min(df1['Norm'])
                       df1['Norm'] = df1['Norm']/max(df1['Norm'])

                df1.plot(x = 'pgm_energy_readback', y = 'Norm', label = str(i), ax=label)

def plot_avg_norm_xas(scanid1,scanid2,label,scan_type='TEY',normto1='Y'):
        plt.figure(label)
        label = plt.gca()
        sum = db.get_table(db[scanid1])
        sum['Norm'] = sum['sclr_ch4']-sum['sclr_ch4']
        denom = 0
        for i in range (scanid1, scanid2+1):
                df1 = db.get_table(db[i])
                if ((scan_type == 'TEY') or (scan_type == 'tey')):
                       df1['Norm'] = df1['sclr_ch4']/df1['sclr_ch3']
                elif ((scan_type == 'PFY') or (scan_type == 'pfy')):
                       df1['Norm'] = df1['vortex_mca_rois_roi4_count']/df1['sclr_ch3']
                elif ((scan_type == 'TFY') or (scan_type == 'tfy')):
                       df1['Norm'] = df1['vortex_mca_rois_roi1_count']/df1['sclr_ch3']
                elif ((scan_type == 'IPFY') or (scan_type == 'ipfy')):
                       df1['Norm'] = 1/(df1['vortex_mca_rois_roi3_count']/df1['sclr_ch3'])
                elif ((scan_type == 'PEY') or (scan_type == 'pey')):
                       df1['Norm'] = df1['specs_count']/df1['sclr_ch3']
                
                denom = denom + 1
                sum['Norm'] = sum['Norm'] + df1['Norm']
        
        sum['Norm'] = sum['Norm']/denom

        if (normto1 == 'Y' or normto1 == 'y' or normto1 == 'yes' or normto1 == 'YES'):
                sum['Norm'] = sum['Norm']-min(sum['Norm'])
                sum['Norm'] = sum['Norm']/max(sum['Norm'])

        sum.plot(x = 'pgm_energy_readback', y = 'Norm', label = str(i), ax=label)

def plot_avg_async_xas(scanid1,scanid2,normid1,normid2,label,scan_type='TEY',normto1='Y'):
        plt.figure(label)
        label = plt.gca()

        I0sum = db.get_table(db[normid1])
        I0sum['Avg'] = I0sum['sclr_ch2']-I0sum['sclr_ch2']
        denom = 0
        for i in range (normid1, normid2+1):
                dfn = db.get_table(db[i])
                denom = denom + 1
                I0sum['Avg'] = I0sum['Avg'] + dfn['sclr_ch2']


        I0sum['Avg'] = I0sum['Avg']/denom

        I1sum = db.get_table(db[scanid1])
        I1sum['Avg'] = I1sum['sclr_ch4']-I1sum['sclr_ch4']
        denom = 0
        for i in range (scanid1, scanid2+1):
                df1 = db.get_table(db[i])
                if ((scan_type == 'TEY') or (scan_type == 'tey')):
                       df1['Norm'] = df1['sclr_ch4']/I0sum['Avg']
                elif ((scan_type == 'PFY') or (scan_type == 'pfy')):
                       df1['Norm'] = df1['vortex_mca_rois_roi4_count']/I0sum['Avg']
                elif ((scan_type == 'TFY') or (scan_type == 'tfy')):
                       df1['Norm'] = df1['vortex_mca_rois_roi1_count']/I0sum['Avg']
                elif ((scan_type == 'IPFY') or (scan_type == 'ipfy')):
                       df1['Norm'] = 1/(df1['vortex_mca_rois_roi3_count']/I0sum['Avg'])
                elif ((scan_type == 'PEY') or (scan_type == 'pey')):
                       df1['Norm'] = df1['specs_count']/I0sum['Avg']
                
                denom = denom + 1
                I1sum['Avg'] = I1sum['Avg'] + df1['Norm']

        I1sum['Avg'] = I1sum['Avg']/denom

        if (normto1 == 'Y' or normto1 == 'y' or normto1 == 'yes' or normto1 == 'YES'):
                I1sum['Avg'] = I1sum['Avg']-min(I1sum['Avg'])
                I1sum['Avg'] = I1sum['Avg']/max(I1sum['Avg'])

        I1sum.plot(x = 'pgm_energy_readback', y = 'Avg', label = str(i), ax=label)

def plot_avg_raw_xas(scanid1,scanid2,label,scan_type='TEY',normto1='Y'):
        plt.figure(label)
        label = plt.gca()
        sum = db.get_table(db[scanid1])
        sum['Norm'] = sum['sclr_ch4']-sum['sclr_ch4']
        denom = 0
        for i in range (scanid1, scanid2+1):
                df1 = db.get_table(db[i])
                if ((scan_type == 'TEY') or (scan_type == 'tey')):
                       df1['Norm'] = df1['sclr_ch4']
                elif ((scan_type == 'PFY') or (scan_type == 'pfy')):
                       df1['Norm'] = df1['vortex_mca_rois_roi4_count']
                elif ((scan_type == 'TFY') or (scan_type == 'tfy')):
                       df1['Norm'] = df1['vortex_mca_rois_roi1_count']
                elif ((scan_type == 'IPFY') or (scan_type == 'ipfy')):
                       df1['Norm'] = 1/(df1['vortex_mca_rois_roi3_count'])
                elif ((scan_type == 'PEY') or (scan_type == 'pey')):
                       df1['Norm'] = df1['specs_count']

                denom = denom + 1
                sum['Norm'] = sum['Norm'] + df1['Norm']

        sum['Norm'] = sum['Norm']/denom

        if (normto1 == 'Y' or normto1 == 'y' or normto1 == 'yes' or normto1 == 'YES'):
                sum['Norm'] = sum['Norm']-min(sum['Norm'])
                sum['Norm'] = sum['Norm']/max(sum['Norm'])

        sum.plot(x = 'pgm_energy_readback', y = 'Norm', label = str(i), ax=label)

def plot_raw_xas(scanid1,scanid2,label,scan_type='TEY',normto1='Y'):
        plt.figure(label)
        label = plt.gca()
        for i in range (scanid1, scanid2+1):
                df1 = db.get_table(db[i])
                if ((scan_type == 'TEY') or (scan_type == 'tey')):
                       df1['Raw'] = df1['sclr_ch4']
                elif ((scan_type == 'PFY') or (scan_type == 'pfy')):
                       df1['Raw'] = df1['vortex_mca_rois_roi4_count']
                elif ((scan_type == 'TFY') or (scan_type == 'tfy')):
                       df1['Raw'] = df1['vortex_mca_rois_roi1_count']
                elif ((scan_type == 'PEY') or (scan_type == 'pey')):
                       df1['Raw'] = df1['specs_count']
                elif ((scan_type == 'IPFY') or (scan_type == 'ipfy')):
                       df1['Raw'] = 1/(df1['vortex_mca_rois_roi3_count'])

                if (normto1 == 'Y' or normto1 == 'y' or normto1 == 'yes' or normto1 == 'YES'):
                       df1['Raw'] = df1['Raw']-min(df1['Raw'])
                       df1['Raw'] = df1['Raw']/max(df1['Raw'])

                df1.plot(x = 'pgm_energy_readback', y = 'Raw', label = str(i), ax=label)


def XAS_scan(e_start, e_finish, velocity, deadband, inc_vortex = True):
    if inc_vortex == True:
        for channel in ['mca.rois.roi2.count','mca.rois.roi3.count','mca.rois.roi4.count']:
            getattr(vortex, channel).kind = 'hinted'
        for channel in ['mca.rois.roi2.count','mca.rois.roi3.count']:
            getattr(vortex, channel).kind = 'normal'
        dets = [sclr, vortex, norm_ch4, ring_curr]
    else:
        dets = [sclr, norm_ch4, ring_curr]

    for channel in ['channels.chan3','channels.chan4']:
        getattr(sclr, channel).kind = 'hinted'
    for channel in ['channels.chan2']:
        getattr(sclr, channel).kind = 'normal'

    yield from bps.mov(pgm_energy, e_start)
    yield from E_ramp(dets, e_start, e_finish, velocity, deadband=deadband)

def beam_damage():
    dets = [sclr, vortex]
    for channel in ['mca.rois.roi2.count','mca.rois.roi3.count','mca.rois.roi4.count']:
        getattr(vortex, channel).kind = 'hinted'
    for channel in ['mca.rois.roi2.count', 'mca.rois.roi3.count']:
        getattr(vortex, channel).kind = 'normal'
    for channel in ['channels.chan3','channels.chan4']:
        getattr(sclr, channel).kind = 'hinted'
    for channel in ['channels.chan2', 'channels.chan3']:
        getattr(sclr, channel).kind = 'normal'
 
    a = [28, 30, 32, 34, 36, 38, 40, 42]
    b = [364.8, 365.1, 365.4, 365.7, 366, 366.3, 366.6, 366.8]
 
    for temp_offset, sample_pos in zip(a, b): 
        yield from bps.abs_set(ioxas_x, sample_pos, wait=True)
        for ii in range(0, 3):
            yield from bps.abs_set(feedback, 0)
            yield from bps.mov(pgm_energy, 290)
            yield from bps.abs_set(epu1offset, -4)
            yield from bps.sleep(10)
            yield from bps.abs_set(feedback, 1)
            yield from bps.abs_set(valve_diag3_open, 1, wait=True)
            yield from E_ramp(dets, 290, 280, 0.05, deadband=4)
            yield from bps.abs_set(feedback, 0)
            yield from bps.mov(pgm_energy, 540)
            yield from bps.abs_set(epu1offset, temp_offset)
            yield from bps.sleep(10)
            yield from bps.abs_set(feedback, 1)
            yield from bps.sleep(1200)
            yield from bps.abs_set(valve_diag3_close, 1, wait=True)
         
        yield from bps.abs_set(feedback, 0)
        yield from bps.mov(pgm_energy, 290)
        yield from bps.abs_set(epu1offset, -4)
        yield from bps.sleep(10)
        yield from bps.abs_set(feedback, 1)
        yield from bps.abs_set(valve_diag3_open, 1, wait=True)
        yield from E_ramp(dets, 290, 280, 0.05, deadband=4)
        
        yield from bps.abs_set(diag3_y, 3.87, wait=True)
        yield from bps.abs_set(feedback, 0)
        yield from bps.mov(pgm_energy, 290)
        yield from bps.abs_set(epu1offset, -4)
        yield from bps.sleep(5)
        yield from bps.abs_set(feedback, 1)
        yield from bps.abs_set(valve_diag3_open, 1, wait=True)
        yield from E_ramp(dets, 290, 280, 0.05, deadband=4)
        yield from bps.abs_set(valve_diag3_close, 1, wait=True)
        yield from bps.abs_set(diag3_y, 46, wait=True)

    yield from bps.abs_set(valve_diag3_close, 1, wait=True)
    yield from bps.abs_set(valve_mir3_close, 1, wait=True)

def PEY_init(kinE, passE, dwell):
    yield from specs.set_mode('single_count')
    yield from bps.abs_set(specs.cam.kinetic_energy, kinE)
    yield from bps.abs_set(specs.cam.pass_energy, passE)
    yield from bps.abs_set(specs.cam.acquire_time, dwell)

def PEY_XAS_scan(e_start, e_finish, velocity, deadband):
    dets = [specs, sclr]
    # dets = [sclr, norm_ch4, ring_curr]

    for channel in ['channels.chan3','channels.chan4']:
        getattr(sclr, channel).kind = 'hinted'
    for channel in ['channels.chan2']:
        getattr(sclr, channel).kind = 'normal'

    yield from bps.mov(pgm_energy, e_start)
    yield from E_ramp(dets, e_start, e_finish, velocity, deadband=deadband)

def find_beam(photonE, bindingE):
    dets = [specs, sclr]
    yield from bps.abs_set(feedback, 0)
    yield from bps.mov(pgm_energy, photonE)
    yield from bps.sleep(5)
    yield from bps.abs_set(feedback, 1)
    yield from bps.sleep(5)
    yield from specs.set_mode('single_count')
    kinE = photonE - bindingE
    yield from bps.abs_set(specs.cam.kinetic_energy, kinE)
    yield from bps.abs_set(specs.cam.pass_energy, 10)
    yield from bps.abs_set(specs.cam.acquire_time, 0.5)

    for channel in ['channels.chan4']:
        getattr(sclr, channel).kind = 'hinted'
    for channel in ['channels.chan2', 'channels.chan3']:
        getattr(sclr, channel).kind = 'normal'

    yield from bp.scan(dets, m1b1_setpoint, 290, 360, 71)


def PD_scan(e_start, e_finish, velocity, deadband):
    for channel in ['channels.chan3','channels.chan2']:
        getattr(sclr, channel).kind = 'hinted'
    for channel in ['channels.chan4']:
        getattr(sclr, channel).kind = 'normal'

    dets = [sclr, ring_curr]

    yield from bps.mov(pgm_energy, e_start)
    yield from E_ramp(dets, e_start, e_finish, velocity, deadband=deadband)


def PD_count():
    for channel in ['channels.chan3','channels.chan2']:
        getattr(sclr, channel).kind = 'hinted'
    for channel in ['channels.chan4', 'channels.chan3']:
        getattr(sclr, channel).kind = 'normal'

    dets = [sclr, ring_curr]

    yield from bp.count(dets, num=None, delay=30)

def Aumesh_count():
    for channel in ['channels.chan3','channels.chan2']:
        getattr(sclr, channel).kind = 'hinted'
    for channel in ['channels.chan4', 'channels.chan2']:
        getattr(sclr, channel).kind = 'normal'

    dets = [sclr, ring_curr]

    yield from bp.count(dets, num=None)

   
def epu_gap_scans():
    dets=[sclr, ring_curr]

    for channel in ['channels.chan2']:
        getattr(sclr, channel).kind = 'hinted'
    for channel in ['channels.chan3','channels.chan4']:
        getattr(sclr, channel).kind = 'normal'

#   1st order horizontal

    yield from bps.abs_set(epu1table, 2)
    yield from bps.sleep(20)
    yield from bps.mov(pgm_energy, 250)

    for ene_val in range(250, 1251, 50):
        yield from bps.abs_set(feedback, 0)
        yield from bps.abs_set(pgm_energy, ene_val, wait=True)
        yield from bps.abs_set(feedback, 1)
        yield from bps.sleep(10)
        yield from bps.abs_set(feedback, 0)
        yield from bps.sleep(5)
        yield from bp.rel_scan(dets, epu1.gap, -2, 2, 80)

    for ene_val2 in range(1300, 1651, 50):
        yield from bps.abs_set(feedback, 0)
        yield from bps.abs_set(pgm_energy, ene_val2, wait=True)
        yield from bps.abs_set(feedback, 1)       
        yield from bps.sleep(10)
        yield from bps.abs_set(feedback, 0)
        yield from bps.sleep(5)
        yield from bp.rel_scan(dets, epu1.gap, -3, 3, 120)

#   3rd order horizontal
    yield from bps.abs_set(epu1.phase, 0, wait=True)
    yield from bps.abs_set(epu1table, 3)
    yield from bps.sleep(20)
    yield from bps.abs_set(pgm_energy, 750, wait=True)

    for ene_val3 in range(750, 1951, 50):
        yield from bps.abs_set(feedback, 0)
        yield from bps.abs_set(pgm_energy, ene_val3, wait=True)
        yield from bps.abs_set(feedback, 1)
        yield from bps.sleep(10)
        yield from bps.abs_set(feedback, 0)
        yield from bps.sleep(5)
        yield from bp.rel_scan(dets, epu1.gap, -1, 1, 80)

#   1st order vertical
#    yield from bps.abs_set(epu1.phase, 24.6, wait=True)
#    yield from bps.abs_set(epu1table, 5)
#    yield from bps.abs_set(pgm_energy, 250, wait=True)
#    yield from bps.sleep(30)

#    for ene_val in range(250, 401, 50):
#        yield from bps.abs_set(feedback, 0)
#        yield from bps.abs_set(pgm_energy, ene_val, wait=True)
#        yield from bps.sleep(10)
#        yield from bp.scan(dets, epu1.gap, 12, 15, 120)

#    for ene_val in range(450, 1251, 50):
#        yield from bps.abs_set(feedback, 0)
#        yield from bps.abs_set(pgm_energy, ene_val, wait=True)
#        yield from bps.abs_set(feedback, 1)
#        yield from bps.sleep(10)
#        yield from bps.abs_set(feedback, 0)
#        yield from bps.sleep(5)
#        yield from bp.rel_scan(dets, epu1.gap, -2, 2, 80)

#    for ene_val2 in range(1300, 1651, 50):
#        yield from bps.abs_set(feedback, 0)
#        yield from bps.abs_set(pgm_energy, ene_val2, wait=True)
#        yield from bps.abs_set(feedback, 1)
#        yield from bps.sleep(10)
#        yield from bps.abs_set(feedback, 0)
#        yield from bps.sleep(5)
#        yield from bp.rel_scan(dets, epu1.gap, -3, 3, 60)

#   3rd order vertical


#    yield from bps.abs_set(epu1table ,9)
#    yield from bps.sleep(20)
#    yield from bps.abs_set(pgm_energy, 750, wait=True)

#    for ene_val in range(750, 1151, 50):
#        yield from bps.abs_set(feedback, 0)
#        yield from bps.abs_set(pgm_energy, ene_val, wait=True)
#        yield from bps.sleep(10)
#        yield from bp.scan(dets, epu1.gap, 12, 15, 120)


#    for ene_val3 in range(1200, 1951, 50):
#        yield from bps.abs_set(feedback, 0)
#        yield from bps.abs_set(pgm_energy, ene_val3, wait=True)
#        yield from bps.abs_set(feedback, 1)
#        yield from bps.sleep(10)
#        yield from bps.abs_set(feedback, 0)
#        yield from bps.sleep(5)
#        yield from bp.rel_scan(dets, epu1.gap, -1, 1, 80)

    yield from bps.abs_set(valve_diag3_close, 1, wait=True)
    yield from bps.abs_set(valve_mir3_close, 1, wait=True)
    yield from bps.mov(diag3_y, 46) 




def nexafs_pey(e_start, e_finish, speed, deadbnd):

    #turn off feedback before moving energy
    # caput('XF:23ID2-OP{FBck}Sts:FB-Sel',0)
    yield from bps.mov(mirror_feedback, 0)
    yield from bps.sleep(2)
    #to close downstream shutter
    # caput('XF:23ID2-PPS{PSh}Cmd:Cls-Cmd',1)
    yield from bps.mov(ds_shutter, 'Close')
    # sleep(2)
    print ('Moving to start energy...')
    #move energy to start position
    yield from bps.mov(pgm_energy, e_start)

    yield from bps.sleep(2)

    print ('Scan is starting...')

    #to open downstream shutter just when scan is started
    # caput('XF:23ID2-PPS{PSh}Cmd:Opn-Cmd',1)
    yield from bps.mov(ds_shutter, 'Open')    
    yield from bps.sleep(3)
    
    #turn on feedback
    # caput('XF:23ID2-OP{FBck}Sts:FB-Sel',1)
    yield from bps.mov(mirror_feedback, 1)    
    #caput('XF:23IDA-OP:2{Mir:1A-Ax:FPit}Mtr_POS_SP',50)
    #sleep(2)

    #to start the scan
    #RE(ascan(pgm_energy, e_start, e_finish, e_points), group='nexafs')
    yield from XAS_scan(e_start, e_finish, speed, deadbnd, inc_vortex=False)

    # caput('XF:23ID2-OP{FBck}Sts:FB-Sel',0)
    yield from bps.mov(mirror_feedback, 0)
    yield from bps.sleep(2)
    #to close downstream shutter
    # caput('XF:23ID2-PPS{PSh}Cmd:Cls-Cmd',1)
    yield from bps.mov(ds_shutter, 'Close')
    # sleep(2)
    yield from bps.sleep(2)

    #to open downstream shutter just when scan is started
    # caput('XF:23ID2-PPS{PSh}Cmd:Opn-Cmd',1)
    yield from bps.mov(ds_shutter, 'Open')    
    yield from bps.sleep(3)
    
    #turn on feedback
    # caput('XF:23ID2-OP{FBck}Sts:FB-Sel',1)
    yield from bps.mov(mirror_feedback, 1)    

    #saving scan
#    save_q = input("The scan is finished. Do you want to save the data (as csv)? (yes/no) ")
#    if save_q in ["yes", "Y", "Yes", "y", "YES"]:
#        filename = input("Type file name here (no spaces, no special characters other than dash or underscore): ")
#        savedname = filename+'.csv'
#        df = db.get_table(db[-1])
#        df.to_csv('Documents/Yildiz/savedname')
#        print ('The scan has been saved as', savedname)
#    else:
#        print ('The scan has not been saved!')

def test():
    yield from abs_set(pgm_energy, 890, wait=True)
    yield from E_ramp(890, 895, 0.1, deadband=8)

CONTAINER = None
REF_EDGES = {'Al' : {'energy': 1565 , 'epu_table': 5 , 'vortex_low': 2000 , 'vortex_high': 2800},
             'Cu' : {'energy': 932  , 'epu_table': 4 , 'vortex_low': 900 , 'vortex_high': 1100},
             'O'  : {'energy': 540  , 'epu_table': 4 , 'vortex_low': 500 , 'vortex_high': 700},
             'Ni' : {'energy': 854  , 'epu_table': 4 , 'vortex_low': 900 , 'vortex_high': 1100},
             'Fe' : {'energy': 710  , 'epu_table': 4 , 'vortex_low': 700  , 'vortex_high': 1000},
             'F'  : {'energy': 691  , 'epu_table': 4 , 'vortex_low': 700  , 'vortex_high': 1000},
             'Na' : {'energy': 1075 , 'epu_table': 4 , 'vortex_low': 1000 , 'vortex_high': 1400},
             'N'  : {'energy': 407  , 'epu_table': 4 , 'vortex_low': 400  , 'vortex_high': 600},
             'Co' : {'energy': 781  , 'epu_table': 4 , 'vortex_low': 850  , 'vortex_high': 1000},
             'Mn' : {'energy': 654  , 'epu_table': 4 , 'vortex_low': 700  , 'vortex_high': 800},
             'Ti' : {'energy': 466  , 'epu_table': 4 , 'vortex_low': 400  , 'vortex_high': 650},
             'Mo' : {'energy': 380  , 'epu_table': 4 , 'vortex_low': 300  , 'vortex_high': 500},
             'C' : {'energy': 293 , 'epu_table': 4 , 'vortex_low': 220 , 'vortex_high': 400},
             'Cd' : {'energy': 620  , 'epu_table': 4 , 'vortex_low': 700  , 'vortex_high': 800},
             'La' : {'energy': 860  , 'epu_table': 4 , 'vortex_low': 800  , 'vortex_high': 1000},
             'S' : {'energy': 840  , 'epu_table': 4 , 'vortex_low': 2200  , 'vortex_high': 2800},
             'Si' : {'energy': 1860  , 'epu_table': 5 , 'vortex_low': 1800  , 'vortex_high': 2200},
             'Rb' : {'energy': 1806  , 'epu_table': 5 , 'vortex_low': 1600  , 'vortex_high': 1800},
             'Cl' : {'energy': 945  , 'epu_table': 4 , 'vortex_low': 2800  , 'vortex_high': 3400},
}

def find_sample(edge, xstart, xstop, step):
    edge_params = REF_EDGES[edge]
    pts = abs(int(round((xstop-xstart)/step)))
    yield from bps.abs_set(feedback, 0)
    yield from bps.abs_set(pgm_energy, edge_params['energy'], wait=True)
    yield from bps.abs_set(epu1table, edge_params['epu_table'], wait=True)
    yield from bps.sleep(15)
    yield from bps.abs_set(feedback, 1)
    yield from bps.abs_set(vortex.mca.rois.roi2.lo_chan, edge_params['vortex_low'], wait=True)
    yield from bps.abs_set(vortex.mca.rois.roi2.hi_chan, edge_params['vortex_high'], wait=True)
    old_hints_vortex = save_hint_state(vortex)
    old_hints_sclr = save_hint_state(sclr)
    for channel in ['mca.rois.roi2.count']:
        getattr(vortex, channel).kind = 'hinted'
    for channel in ['mca.rois.roi3.count','mca.rois.roi4.count']:
        getattr(vortex, channel).kind = 'normal'
    for channel in ['channels.chan4']:
        getattr(sclr, channel).kind = 'hinted'
    for channel in ['channels.chan2','channels.chan3']:
        getattr(sclr, channel).kind = 'normal'
    dets = [sclr, vortex]
#    vortex.mca.rois.roi2.count.kind = 'hinted'
#    yield from bp.scan(dets, appes_y, xstart, xstop, pts)
    yield from bp.scan(dets, ioxas_x, xstart, xstop, pts)
    yield from bps.sleep(2)
    restore_hint_state(vortex, old_hints_vortex)
    restore_hint_state(sclr, old_hints_sclr)


#def find_sample(energy, xstart, xstop, pts):
        # gs no longer supported
    #gs.TABLE_COLS.append('vortex_mca_rois_roi2_count')
    #gs.PLOT_Y = 'vortex_mca_rois_roi2_count'
#    mov(vortex.mca.rois.roi2.lo_chan, 1400)
#    mov(vortex.mca.rois.roi2.hi_chan, 2000)
#    yield from bps.abs_set(vortex.mca.rois.roi2.lo_chan, 700)
#    yield from bps.abs_set(vortex.mca.rois.roi2.hi_chan, 1000)
#    old_hints = save_hint_state(vortex)
#    for channel in ['mca.rois.roi2.count']:
#        getattr(vortex, channel).kind = 'hinted'
#    for channel in ['mca.rois.roi3.count','mca.rois.roi4.count']:
#        getattr(vortex, channel).kind = 'normal'
#    vortex.mca.rois.roi2.count.kind = 'hinted'
#    yield from bps.abs_set(feedback, 0)
#    yield from bps.abs_set(pgm_energy, energy, wait=True)
#    yield from bps.abs_set(feedback, 1)
#    yield from bps.sleep(2)
#    yield from bp.scan([vortex], ioxas_x, xstart, xstop, pts)
#    yield from bps.sleep(2)
#    restore_hint_state(vortex, old_hints)
    #gs.TABLE_COLS.remove('vortex_mca_rois_roi2_count')
    #gs.PLOT_Y = 'vortex_mca_rois_roi4_count'

def save_hint_state(dev):
    return {c: getattr(dev, c).kind for c in dev.read_attrs}

def restore_hint_state(dev, prev_state):
    for channel, state in prev_state.items():
        getattr(dev, channel).kind = state

#Mono stability scans

#foe_DI_P_in = EpicsSignalRO('XF:23IDA-UT{DI}P:Supply-I', name='foe_DI_P_in')
#foe_DI_P_out = EpicsSignalRO('XF:23IDA-UT{DI}P:Return-I', name='foe_DI_P_out')
#mirr_DI_T_in = EpicsSignalRO('XF:23ID1-OP{TCtrl:1-Chan:A}T-I', name='mirr_DI_T_in') # in K
#mirr_DI_T_out = EpicsSignalRO('XF:23ID1-OP{TCtrl:1-Chan:C}T-I', name='mirr_DI_T_out') # in K
#grt_DI_T_in = EpicsSignalRO('XF:23ID1-OP{TCtrl:1-Chan:B}T-I', name='grt_DI_T_in') # in K
#grt_DI_T_out = EpicsSignalRO('XF:23ID1-OP{TCtrl:1-Chan:D}T-I', name='grt_DI_T_out') # in K
#mono_air_T = EpicsSignalRO('XF:23ID1-OP{TCtrl:1-Chan:D5}T-I', name='mono_air_T') # in K
#mirr_T = EpicsSignalRO('XF:23ID2-OP{Mon-Mir}T-I', name='mirr_T')
#grt1_T = EpicsSignalRO('XF:23ID2-OP{Mon-Grt:1}T-I', name='grt1_T')
#grt2_T = EpicsSignalRO('XF:23ID2-OP{Mon-Grt:2}T-I', name='grt2_T')
#grt3_T = EpicsSignalRO('XF:23ID2-OP{Mon-Grt:3}T-I', name='grt3_T')
#grt4_T = EpicsSignalRO('XF:23ID2-OP{Mon-Grt:4}T-I', name='grt4_T')

# dets definition, all relevant variables around
#dets_stab = [specs, ring_curr, foe_DI_P_in, foe_DI_P_out, mono_air_T, mirr_T, grt1_T, grt2_T, grt3_T, grt4_T, epu1.gap, epu2.gap]
dets_stab = [specs, ring_curr, epu1.gap, epu2.gap]


def mono_stability():
    ring_curr.kind='hinted'
#    grt1_T.kind='normal'
#    grt3_T.kind='normal'
#    grt4_T.kind='normal'
#    mirr_T.kind='normal'
#    for channel in ['channels.chan4']:
#        getattr(sclr, channel).kind = 'hinted'
#    for channel in ['channels.chan2','channels.chan3']:
#        getattr(sclr, channel).kind = 'normal'
#    yield from bps.abs_set(pgm_energy, 932.4, wait=True)
    yield from count(dets_stab,num=None, delay=0.2)
#    yield from bps.abs_set(valve_mir3_close, 1)  
#    yield from bps.abs_set(ds_shutter, 'Close')
#    yield from bps.abs_set(us_shutter, 'Close')

CONTAINER = None
CORE_LEVELS = {'C1s' : {'binding_en': 1560 , 'epu_table': 2},
             'Ag3d' : {'binding_en': 368  , 'epu_table': 2},
}

def beam_studies():
    ring_curr.kind='hinted'
   
    yield from specs.set_mode('single_count')
    yield from bps.abs_set(specs.cam.pass_energy, 10)
    yield from bps.abs_set(specs.cam.acquire_time, 0.2)


    yield from bps.abs_set(feedback, 0)
    yield from bps.abs_set(pgm_energy, 700, wait=True)
    yield from bps.abs_set(epu1table, 2, wait=True)
    yield from bps.sleep(10)
    yield from bps.abs_set(feedback, 1)
 
    yield from bps.abs_set(specs.cam.kinetic_energy, 332)
    yield from count(dets_stab,num=None, delay=0.2)

 

