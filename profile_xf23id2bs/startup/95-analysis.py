import numpy as np

def plot_norm_trans(scanid1,scanid2,normid,label):
        plt.figure(label)
        label = plt.gca()
        dfn = db.get_table(db[normid])
        for i in range (scanid1, scanid2+1):
                df1 = db.get_table(db[i])
                df1['Norm'] = -1*np.log(df1['sclr_ch4']/dfn['sclr_ch4'])
                df1.plot(x = 'pgm_energy_readback', y = 'Norm', label = str(i), ax=label)

def plot_norm_async_tey(scanid1,scanid2,normid,label):
        plt.figure(label)
        label = plt.gca()
        dfn = db.get_table(db[normid])
        for i in range (scanid1, scanid2+1):
                df1 = db.get_table(db[i])
                df1['Norm'] = df1['norm_ch4']/dfn['norm_ch4']
                df1.plot(x = 'pgm_energy_readback', y = 'Norm', label = str(i), ax=label)

def plot_norm_async_pfy(scanid1,scanid2,normid,label):
        plt.figure(label)
        label = plt.gca()
        dfn = db.get_table(db[normid])
        for i in range (scanid1, scanid2+1):
                df1 = db.get_table(db[i])
                df1['Norm'] = df1['vortex_mca_rois_roi4_count']/dfn['sclr_ch2']
                df1.plot(x = 'pgm_energy_readback', y = 'Norm', label = str(i), ax=label)

def plot_norm_tey(scanid1,scanid2,label):
    plt.figure(label)
    label = plt.gca()
    for i in range (scanid1, scanid2+1):
        df1 = db.get_table(db[i])
        df1['Norm'] = df1['sclr_ch4']/df1['sclr_ch3']
        df1.plot(x = 'pgm_energy_readback', y = 'Norm', label = str(i), ax=label)

def plot_norm_pfy(scanid1,scanid2,label):
        plt.figure(label)
        label = plt.gca()
        for i in range (scanid1, scanid2+1):
                df1 = db.get_table(db[i])
                df1['Norm'] = df1['vortex_mca_rois_roi4_count']/df1['sclr_ch3']
                df1.plot(x = 'pgm_energy_readback', y = 'Norm', label = str(i), ax=label)

def plot_norm_pfy_ROI2(scanid1,scanid2,label):
        plt.figure(label)
        label = plt.gca()
        for i in range (scanid1, scanid2+1):
                df1 = db.get_table(db[i])
                df1['Norm'] = df1['vortex_mca_rois_roi2_count']/df1['sclr_ch3']
                df1.plot(x = 'pgm_energy_readback', y = 'Norm', label = str(i), ax=label)

def plot_norm_ipfy(scanid1,scanid2,label):
        plt.figure(label)
        label = plt.gca()
        for i in range (scanid1, scanid2+1):
                df1 = db.get_table(db[i])
                df1['Norm'] = 1/(df1['vortex_mca_rois_roi3_count']/df1['sclr_ch3'])
                df1.plot(x = 'pgm_energy_readback', y = 'Norm', label = str(i), ax=label)

def plot_raw_ipfy(scanid1,scanid2,label):
        plt.figure(label)
        label = plt.gca()
        for i in range (scanid1, scanid2+1):
                df1 = db.get_table(db[i])
                df1['IPFY'] = 1/(df1['vortex_mca_rois_roi3_count'])
                df1.plot(x = 'pgm_energy_readback', y = 'IPFY', label = str(i), ax=label)

def plot_raw_pfy(scanid1,scanid2,label):
        plt.figure(label)
        label = plt.gca()
        for i in range (scanid1, scanid2+1):
                df1 = db.get_table(db[i])
                df1.plot(x = 'pgm_energy_readback', y = 'vortex_mca_rois_roi4_count', label = str(i), ax=label)

def plot_raw_tey(scanid1,scanid2,label):
        plt.figure(label)
        label = plt.gca()
        for i in range (scanid1, scanid2+1):
                df1 = db.get_table(db[i])
                df1.plot(x = 'pgm_energy_readback', y = 'sclr_ch4', label = str(i), ax=label)

def save_mca(runid, filename, mca_name):
    hdr = db[runid]
    data_all = hdr.table()
    data_mca = data_all[mca_name]
    d = np.vstack(data_mca.values).T
    np.savetxt(filename, d)

def save_xas_csv(first_id, last_id):
    for scanid in range(first_id,last_id+1,1):
        df = db[scanid].table()
#        df['Norm'] = df['sclr_ch4']/df['sclr_ch3']
        #fn = 'csv_data/Scan_{scan_id}.csv'.format(db[scanid].start)
#        df.to_csv('~/User_Data/Hunt/Prop_302802/Scan_%d.csv' % scanid, columns=['pgm_energy_readback', 'vortex_mca_rois_roi2_count', 'vortex_mca_rois_roi3_count', 'vortex_mca_rois_roi4_count', 'sclr_ch2', 'sclr_ch3', 'sclr_$
        save = df.to_csv('~/User_Data/Hunt/Prop_302802/Scan_%d.csv' % scanid, columns=['pgm_energy_readback', 'time', 'sclr_ch2', 'sclr_ch3', 'sclr_ch4', 'norm_ch4', 'vortex_mca_rois_roi3_count', 'vortex_mca_rois_roi4_count' ], index=False)


def save_all_pfy(runid, filename, mca_name):
    np.savetext(filename, d, save)


#import h5py
#from suitcase import hdf5
#hdr = db[7789]
#hdf5.export(hdr, 'mytest.h5', use_uid=False)
#
#with h5py.File('mytest.h5') as f:
#    d = f['data_7789/primary/data/vortex_mca_spectrum'][:]
#    energy = f['data_7789/primary/data/pgm_energy_readback'][:]
#    I0 = f['data_7789/primary/data/sclr_ch3'][:]





