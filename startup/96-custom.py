
from time import sleep
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

#---------------------INSPIRE SCANS----------------------------------------------------------------------------------------------------
def bdc_z_scan_move_kbhroll():
    dets=[sclr, ring_curr]

    for channel in ['channels.chan2']:
        getattr(sclr, channel).kind = 'hinted'
    for channel in ['channels.chan3','channels.chan4']:
        getattr(sclr, channel).kind = 'normal'
    kbh_roll = -800
    while kbh_roll <= 1200:
        yield from bps.mov(hkb_roll, kbh_roll)
        yield from bps.mov(bdc_z, -1.5)
        yield from bps.sleep(5)
        yield from bp.scan(dets, bdc_z, -1.5, -0.6, 901)
        kbh_roll = kbh_roll + 100

def bdc_z_scan_move_bdc_x():
    dets=[sclr, ring_curr]

    for channel in ['channels.chan2']:
        getattr(sclr, channel).kind = 'hinted'
    for channel in ['channels.chan3','channels.chan4']:
        getattr(sclr, channel).kind = 'normal'

    kbh_roll = -24
    while kbh_roll <= 1200:
        yield from bps.mov(hkb_roll, kbh_roll)
        yield from bps.mov(bdc_z, -1.5)
        yield from bps.sleep(5)
        yield from bp.scan(dets, bdc_z, -1.5, -0.6, 901)
        kbh_roll = kbh_roll + 2


def bdc_z_scan_move_kbroll_and_kb_x():
    dets=[sclr, ring_curr]

    for channel in ['channels.chan2']:
        getattr(sclr, channel).kind = 'hinted'
    for channel in ['channels.chan3','channels.chan4']:
        getattr(sclr, channel).kind = 'normal'

    kbroll = 8100
    kbx = -2.289
    bdc_start = -2.82
    
    while kbroll <= 1600:
        yield from bps.mov(kb_roll, kbroll)
        yield from bps.sleep(20)
        kbx = -2.289 + 0.1314*((kbroll+5000)/200)
        yield from bps.mov(kb_x, kbx)
        yield from bps.sleep(20)
        n = 1
        for i in range(n):
             yield from bps.mov(bdc_z, bdc_start)
             bdc_end = bdc_start + 0.5 
             yield from bp.scan(dets, bdc_z, bdc_start, bdc_end, 201)
        kbroll = kbroll + 200
        yield from bps.mov(kb_roll, kbroll)
        yield from bps.sleep(20)
        kbroll =  kbroll + 200
        bdc_start = bdc_start + 0.04

def test_kbx_corr():
    kbroll = -1600
    kbx = -0.32215
    while kbroll <= 1700:
        yield from bps.mov(kb_roll, kbroll)
        yield from bps.sleep(10)
        kbx = kbx + 0.27
        yield from bps.mov(kb_x, kbx)
        yield from bps.sleep(30)
        kbroll = kbroll + 100



def bdc_z_scan_hslit():
    dets=[sclr, ring_curr]

    for channel in ['channels.chan2']:
        getattr(sclr, channel).kind = 'hinted'
    for channel in ['channels.chan3','channels.chan4']:
        getattr(sclr, channel).kind = 'normal'

    hslit = -1.6
    while hslit <= -2:
        yield from bps.mov(dm1_slt, hslit)
#        n = 1
#        for i in range(n):
        yield from bps.mov(bdc_z, -7.1)
        yield from bps.sleep(10)
        yield from bp.scan(dets, bdc_z, -7.1, -6.95, 301)
        hslit = hslit + 0.05

def bdc_y_scan_move_kb_y():
    dets=[sclr, ring_curr]

    for channel in ['channels.chan2']:
        getattr(sclr, channel).kind = 'hinted'
    for channel in ['channels.chan3','channels.chan4']:
        getattr(sclr, channel).kind = 'normal'

    kb_height = 1.0
    bdc_start = 7.84

    while kb_height <= 2.0:
        yield from bps.mov(kb_yi, kb_height)
        yield from bps.mov(kb_yo, kb_height)
        yield from bps.sleep(5)
        kbh_roll = 000
        while kbh_roll <= 1700:
            yield from bps.mov(hkb_roll, kbh_roll)
            yield from bps.sleep(10)
            yield from bps.mov(bdc_y, bdc_start)
            bdc_end = bdc_start + 0.32
            yield from bp.scan(dets, bdc_y, bdc_start, bdc_end, 641)
            kbh_roll = kbh_roll + 400
        kb_height = kb_height + 0.4
        bdc_start = bdc_start + 0.36


def bdc_y_scan_move_kb_z():
    dets=[sclr, ring_curr]

    for channel in ['channels.chan2']:
        getattr(sclr, channel).kind = 'hinted'
    for channel in ['channels.chan3','channels.chan4']:
        getattr(sclr, channel).kind = 'normal'

    kb_long = -6
    bdc_start = 8

    while kb_long <= 6.2:
        yield from bps.mov(kb_z, kb_long)
        yield from bps.mov(bdc_y, bdc_start)
        bdc_end = bdc_start + 0.2
        yield from bps.sleep(5)
        yield from bp.scan(dets, bdc_y, bdc_start, bdc_end, 401)
        kb_long = kb_long + 0.2
        bdc_start = bdc_start - 0.0084

def bdc_z_scan_move_bdc_x():
    dets=[sclr, ring_curr]

    for channel in ['channels.chan2']:
        getattr(sclr, channel).kind = 'hinted'
    for channel in ['channels.chan3','channels.chan4']:
        getattr(sclr, channel).kind = 'normal'

    bdc_long = -24
    bdc_start = -5.1

    while bdc_long <= 4.2:
        yield from bps.mov(bdc_x, bdc_long)
        yield from bps.mov(bdc_z, bdc_start)
        bdc_end = bdc_start + 0.1
        yield from bps.sleep(5)
        yield from bp.scan(dets, bdc_z, bdc_start, bdc_end, 201)
        bdc_long = bdc_long + 2
        bdc_start = bdc_start - 0.03

def bdc_z_scan_move_kbh_pitch():
    dets=[sclr, ring_curr]

    for channel in ['channels.chan2']:
        getattr(sclr, channel).kind = 'hinted'
    for channel in ['channels.chan3','channels.chan4']:
        getattr(sclr, channel).kind = 'normal'

    kbh_pitch = -100
    bdc_start = -5.46

    while kbh_pitch <= 50:
        yield from bps.mov(hkb_pitch, kbh_pitch)
        yield from bps.mov(bdc_z, bdc_start)
        bdc_end = bdc_start + 0.1
        yield from bps.sleep(5)
        yield from bp.scan(dets, bdc_z, bdc_start, bdc_end, 201)
        kbh_pitch = kbh_pitch + 10
        bdc_start = bdc_start - 0.056

def bdc_z_scan_move_kbh_roll():
    dets=[sclr, ring_curr]

    for channel in ['channels.chan2']:
        getattr(sclr, channel).kind = 'hinted'
    for channel in ['channels.chan3','channels.chan4']:
        getattr(sclr, channel).kind = 'normal'

    kbh_roll = 10300
    bdc_start = -5.9

    while kbh_roll <= 11000:
        yield from bps.mov(hkb_roll, kbh_roll)
        yield from bps.mov(bdc_z, bdc_start)
        bdc_end = bdc_start + 0.1
        yield from bps.sleep(5)
        yield from bp.scan(dets, bdc_z, bdc_start, bdc_end, 201)
        kbh_roll = kbh_roll + 200
        bdc_start = bdc_start - 0.022

def bdc_y_scan_move_kbh_roll():
    dets=[sclr, ring_curr]

    for channel in ['channels.chan2']:
        getattr(sclr, channel).kind = 'hinted'
    for channel in ['channels.chan3','channels.chan4']:
        getattr(sclr, channel).kind = 'normal'

    kbh_roll = 8100
    bdc_start = -80.1

    while kbh_roll <= 11000:
        yield from bps.mov(hkb_roll, kbh_roll)
        yield from bps.mov(bdc_y, bdc_start)
        bdc_end = bdc_start + 0.15
        yield from bps.sleep(5)
        yield from bp.scan(dets, bdc_y, bdc_start, bdc_end, 301)
        kbh_roll = kbh_roll + 200
        bdc_start = bdc_start - 0.0167

def bdc_y_scan_move_bdc_x():
    dets=[sclr, ring_curr]

    for channel in ['channels.chan2']:
        getattr(sclr, channel).kind = 'hinted'
    for channel in ['channels.chan3','channels.chan4']:
        getattr(sclr, channel).kind = 'normal'

    bdc_long = -24
    bdc_start = -80.32

    while bdc_long <= 4.2:
        yield from bps.mov(bdc_x, bdc_long)
        yield from bps.mov(bdc_y, bdc_start)
        bdc_end = bdc_start + 0.4
        yield from bps.sleep(5)
        yield from bp.scan(dets, bdc_y, bdc_start, bdc_end, 401)
        bdc_long = bdc_long + 50
        bdc_start = bdc_start + 0.12


#def bdc_z_scan_move_bdc_x_and_kbh_pitch():
#    dets=[sclr, ring_curr]

#    for channel in ['channels.chan2']:
#        getattr(sclr, channel).kind = 'hinted'
#    for channel in ['channels.chan3','channels.chan4']:
#        getattr(sclr, channel).kind = 'normal'

#    bdc_long = -24
#    bdc_start = -5.1
#    kbhpit = -250

#    while bdc_long <= 4.2:
#        yield from bps.mov(bdc_x, bdc_long)
#            while kbhpit <= 400:
#                 yield from bps.mov(bdc_z, bdc_start)
#                 yield from bps.mov(kbh_pitch, kbhpit) 
#                 bdc_end = bdc_start + 0.1
#                 yield from bps.sleep(5)
#                 yield from bp.scan(dets, bdc_z, bdc_start, bdc_end, 201)
#                 kbhpit = kbhpit + 50
#                 bdc_start = bdc_start - 0.28
#        bdc_long = bdc_long + 2
#        bdc_start = bdc_start - 0.03

#--------------INSPIRE PEAK FITTING ---------------------------------------------------------------------------------------------------

def gaussian(x, a, x0, sigma, c):
    return a * np.exp(-(x - x0)**2 / (2 * sigma**2)) + c

def plot_1stderiv(scanid1,scanid2,label,axis):
        plt.figure(label)
        label = plt.gca()
        for i in range (scanid1, scanid2+1):
             # First calculate the first derivative
             func = db.get_table(db[i])
             if axis == 'vert':
                   x_axis = func['bdc_y']
             elif axis == 'horz':
                   x_axis = func['bdc_z']
             elif axis == 'dm1_x':
                   x_axis = func['dm1_x']
             dx = x_axis[2]-x_axis[1]
             func['deriv'] = np.gradient(func['sclr_ch2'],dx)

             # Now fit a Gaussian to the first derivative
             init_max = max(func['deriv'])
             init_sigma = 0.005
             init_min = 0

             if axis == 'vert':
                  init_center = func['bdc_y'][np.argmax(func['deriv'])]
                  init_guess = [init_max, init_center, init_sigma, init_min]
                  popt,pcov = curve_fit(gaussian, func['bdc_y'], func['deriv'], p0 = init_guess)
                  print("The width of the fit at 10% amplitude for scan ID", i, "is:", round(2*2.146*popt[2],4), "mm.")
                  print("The FWHM of the fit for scan ID", i, "is:", round(2.35482*popt[2],4), "mm.")

                  # Plet everything together
                  func['gaussian'] = gaussian(func['bdc_y'], *popt)
                  func.plot(x = 'bdc_y', y = 'deriv', label = str(i), ax=label)
                  func.plot(x = 'bdc_y', y = 'gaussian', label = str(i)+" Gaussian fit", ax=label)

             elif axis == 'horz':
                  init_center = func['bdc_z'][np.argmax(func['deriv'])]
                  init_guess = [init_max, init_center, init_sigma, init_min]
                  popt,pcov = curve_fit(gaussian, func['bdc_z'], func['deriv'], p0 = init_guess)
                  print("The width of the fit at 10% amplitude for scan ID", i, "is:", round(2*2.146*popt[2],4), "mm.")
                  print("The FWHM of the fit for scan ID", i, "is:", round(2.35482*popt[2],4), "mm.")

                  # Plet everything together
                  func['gaussian'] = gaussian(func['bdc_z'], *popt)
                  func.plot(x = 'bdc_z', y = 'deriv', label = str(i), ax=label)
                  func.plot(x = 'bdc_z', y = 'gaussian', label = str(i)+" Gaussian fit", ax=label)

             elif axis == 'dm1_x':
                  init_center = func['dm1_x'][np.argmax(func['deriv'])]
                  init_guess = [init_max, init_center, init_sigma, init_min]
                  popt,pcov = curve_fit(gaussian, func['dm1_x'], func['deriv'], p0 = init_guess)
                  print("The width of the fit at 10% amplitude for scan ID", i, "is:", round(2*2.146*popt[2],4), "mm.")
                  print("The FWHM of the fit for scan ID", i, "is:", round(2.35482*popt[2],4), "mm.")

                  # Plet everything together
                  func['gaussian'] = gaussian(func['dm1_x'], *popt)
                  func.plot(x = 'dm1_x', y = 'deriv', label = str(i), ax=label)
                  func.plot(x = 'dm1_x', y = 'gaussian', label = str(i)+" Gaussian fit", ax=label)

def plot_gaussian_fit(scanid1,scanid2,label,axis):
        plt.figure(label)
        label = plt.gca()
        for i in range (scanid1, scanid2+1):
             func = db.get_table(db[i])
             init_max = max(func['sclr_ch2'])
             init_sigma = 0.1
             init_min = 0

             if axis == 'dm1_x':
                  init_center = func['dm1_x'][np.argmax(func['sclr_ch2'])]
                  init_guess = [init_max, init_center, init_sigma, init_min]
                  popt,pcov = curve_fit(gaussian, func['dm1_x'], func['sclr_ch2'], p0 = init_guess)
                  print("The width of the fit at 10% amplitude for scan ID", i, "is:", round(2*2.146*popt[2],4), "mm.")
                  #print("The centroid for scan ID", i, "is:", round(popt[1],4), "mm.")
                  #print("The maximum for scan ID", i, "is:", round(popt[0],4), "counts.")
                  print("The FWHM of the fit for scan ID", i, "is:", round(2.35482*popt[2],4), "mm.")

                  # Plot everything together
                  func['gaussian'] = gaussian(func['dm1_x'], *popt)
                  func.plot(x = 'dm1_x', y = 'sclr_ch2', label = str(i), ax=label)
                  func.plot(x = 'dm1_x', y = 'gaussian', label = str(i)+" Gaussian fit", ax=label)






#-------------OLD CUSTOM SCANS--------------------------------------------------------------------------------------------------------------
def adrians_xps():
    yield from bps.mov(pgm_energy, 842)
    yield from bps.sleep(3730)
    yield from bps.mov(pgm_energy, 894)
    yield from bps.sleep(3730)
    yield from bps.mov(pgm_energy, 942)
    yield from bps.sleep(3730)
    yield from bps.mov(pgm_energy, 990)
    yield from bps.sleep(3730)
    yield from bps.mov(pgm_energy, 1090)
    yield from bps.sleep(3730)
    yield from bps.mov(valve_diag3_close, 1)
    yield from bps.mov(valve_mir3_close, 1)

"""def Felix_and_Friends():
    dets = [sclr, vortex, norm_ch4, ring_curr]
 
    for channel in ['mca.rois.roi2.count','mca.rois.roi3.count','mca.rois.roi4.count']:
        getattr(vortex, channel).kind = 'hinted'
    for channel in ['mca.rois.roi2.count','mca.rois.roi3.count']:
        getattr(vortex, channel).kind = 'normal'

    for channel in ['channels.chan3','channels.chan4']:
        getattr(sclr, channel).kind = 'hinted'
    for channel in ['channels.chan2']:
        getattr(sclr, channel).kind = 'normal'

    yield from bps.mov(appes_x, 39)
    yield from bps.mov(appes_y,-145)
    yield from bps.mov(pgm_energy, 1245)
    yield from E_ramp(dets, 1245, 1170, 0.2, deadband=18)

    yield from bps.mov(appes_x, 39)
    yield from bps.mov(appes_y,-137.5)
    yield from bps.mov(pgm_energy, 1245)
    yield from E_ramp(dets, 1245, 1170, 0.2, deadband=18)

    yield from bps.mov(appes_x, 45)
    yield from bps.mov(appes_y,-145)
    yield from bps.mov(pgm_energy, 1245)
    yield from E_ramp(dets, 1245, 1170, 0.2, deadband=18)

    yield from bps.mov(appes_x, 45)
    yield from bps.mov(appes_y,-137.5)
    yield from bps.mov(pgm_energy, 1245)
    yield from E_ramp(dets, 1245, 1170, 0.2, deadband=18)
"""

def multi_XAS():
    for channel in ['mca.rois.roi2.count','mca.rois.roi3.count','mca.rois.roi4.count']:
        getattr(vortex, channel).kind = 'hinted'
    for channel in ['mca.rois.roi2.count','mca.rois.roi3.count']:
        getattr(vortex, channel).kind = 'normal'
    dets = [sclr, vortex, norm_ch4, ring_curr]

    for channel in ['channels.chan3','channels.chan4']:
        getattr(sclr, channel).kind = 'hinted'
    for channel in ['channels.chan2']:
        getattr(sclr, channel).kind = 'normal'

# Make sure Au mesh is in position
    yield from bps.abs_set(au_mesh, -103.950, wait=True)


#   Al K measurements
    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(pgm_energy, 1565, wait=True)
    yield from bps.abs_set(epu1table, 7, wait=True)
    yield from bps.abs_set(epu1offset, 6, wait=True)
    yield from bps.sleep(10)
    yield from bps.abs_set(feedback, 1, wait=True)
    yield from bps.sleep(10)
    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(sample_sclr_gain, 1, wait=True)
    yield from bps.abs_set(sample_sclr_decade, 2, wait=True)
    yield from bps.abs_set(aumesh_sclr_gain, 1, wait=True)
    yield from bps.abs_set(aumesh_sclr_decade, 2, wait=True)
    yield from bps.abs_set(vortex.mca.rois.roi2.lo_chan, 1500, wait=True)
    yield from bps.abs_set(vortex.mca.rois.roi2.hi_chan, 1900, wait=True)


    yield from bps.abs_set(ioxas_x, 278.6, wait=True)
    yield from E_ramp(dets, 1592, 1552, 0.1, deadband=4)
    yield from bps.abs_set(pgm_energy, 1592, wait=True)

    yield from bps.abs_set(ioxas_x, 290.0, wait=True)
    yield from E_ramp(dets, 1592, 1552, 0.1, deadband=4)
    yield from bps.abs_set(pgm_energy, 1592, wait=True)

#    yield from bps.abs_set(ioxas_x, 253.3, wait=True)
#    yield from E_ramp(dets, 1552, 1592, 0.05, deadband=1.2)
#    yield from bps.abs_set(pgm_energy, 1565, wait=True)

#    yield from bps.abs_set(ioxas_x, 256.5, wait=True)
#    yield from E_ramp(dets, 1552, 1592, 0.05, deadband=1.2)
#    yield from bps.abs_set(pgm_energy, 1565, wait=True)

#    yield from bps.abs_set(ioxas_x, 259.1, wait=True)
#    yield from E_ramp(dets, 1552, 1592, 0.05, deadband=1.2)
#    yield from bps.abs_set(pgm_energy, 1565, wait=True)
#    yield from bps.abs_set(ioxas_x, 250.4, wait=True)
#    yield from E_ramp(dets, 1552, 1592, 0.05, deadband=1.2)
#    yield from bps.abs_set(pgm_energy, 1565, wait=True)

#   Si K measurements
#    yield from bps.abs_set(feedback, 0, wait=True)
#    yield from bps.abs_set(pgm_energy, 1845, wait=True)
#    yield from bps.abs_set(epu1table, 7, wait=True)
#    yield from bps.abs_set(epu1offset, 10, wait=True)
#    yield from bps.sleep(10)
#    yield from bps.abs_set(feedback, 1, wait=True)
#    yield from bps.sleep(5)
#    yield from bps.abs_set(feedback, 0, wait=True)
#    yield from bps.abs_set(sample_sclr_gain, 2, wait=True)
#    yield from bps.abs_set(sample_sclr_decade, 2, wait=True)
#    yield from bps.abs_set(aumesh_sclr_gain, 2, wait=True)
#    yield from bps.abs_set(aumesh_sclr_decade, 2, wait=True)

#    yield from bps.abs_set(ioxas_x, 250.3, wait=True)
#    yield from E_ramp(dets, 1830, 1875, 0.1, deadband=4)
#    yield from bps.abs_set(pgm_energy, 1565, wait=True)

#    yield from bps.abs_set(ioxas_x, 253.2, wait=True)
#    yield from E_ramp(dets, 1830, 1875, 0.1, deadband=4)
#    yield from bps.abs_set(pgm_energy, 1565, wait=True)

#    yield from bps.abs_set(ioxas_x, 256.35, wait=True)
#    yield from E_ramp(dets, 1830, 1875, 0.1, deadband=4)
#    yield from bps.abs_set(pgm_energy, 1565, wait=True)

#    yield from bps.abs_set(ioxas_x, 259.1, wait=True)
#    yield from E_ramp(dets, 1830, 1875, 0.1, deadband=4)
#    yield from bps.abs_set(pgm_energy, 1565, wait=True)

#O K measurement
    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(pgm_energy, 540, wait=True)
    yield from bps.abs_set(epu1table, 6, wait=True)
    yield from bps.abs_set(epu1offset, 1, wait=True)
    yield from bps.sleep(10)
    yield from bps.abs_set(feedback, 1, wait=True)
    yield from bps.sleep(10)
    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(sample_sclr_gain, 2, wait=True)
    yield from bps.abs_set(sample_sclr_decade, 3, wait=True)
    yield from bps.abs_set(aumesh_sclr_gain, 2, wait=True)
    yield from bps.abs_set(aumesh_sclr_decade, 3, wait=True)
    yield from bps.abs_set(vortex.mca.rois.roi2.lo_chan, 500, wait=True)
    yield from bps.abs_set(vortex.mca.rois.roi2.hi_chan, 700, wait=True)


#    yield from bps.abs_set(ioxas_x, 250.3, wait=True)
#    yield from E_ramp(dets, 520, 570, 0.05, deadband=8)
#    yield from bps.abs_set(pgm_energy, 520, wait=True)
    
    yield from bps.abs_set(ioxas_x, 254.8, wait=True)
    yield from E_ramp(dets, 575, 520, 0.1, deadband=6)
    yield from bps.abs_set(pgm_energy, 575, wait=True)

    yield from bps.abs_set(ioxas_x, 266.7, wait=True)
    yield from E_ramp(dets, 575, 520, 0.1, deadband=6)
    yield from bps.abs_set(pgm_energy, 575, wait=True)

    yield from bps.abs_set(ioxas_x, 278.6, wait=True)
    yield from E_ramp(dets, 575, 520, 0.1, deadband=6)
    yield from bps.abs_set(pgm_energy, 575, wait=True)

    yield from bps.abs_set(ioxas_x, 290.0, wait=True)
    yield from E_ramp(dets, 575, 520, 0.1, deadband=6)
    yield from bps.abs_set(pgm_energy, 575, wait=True)

#Ni L2,3  measurements
    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(pgm_energy, 855, wait=True)
    yield from bps.abs_set(epu1table, 6, wait=True)
    yield from bps.abs_set(epu1offset, 1, wait=True)
    yield from bps.sleep(10)
    yield from bps.abs_set(feedback, 1, wait=True)
    yield from bps.sleep(10)
    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(sample_sclr_gain, 1, wait=True)
    yield from bps.abs_set(sample_sclr_decade, 3, wait=True)
    yield from bps.abs_set(aumesh_sclr_gain, 0, wait=True)
    yield from bps.abs_set(aumesh_sclr_decade, 3, wait=True)
    yield from bps.abs_set(vortex.mca.rois.roi2.lo_chan, 900, wait=True)
    yield from bps.abs_set(vortex.mca.rois.roi2.hi_chan, 1100, wait=True)

    yield from bps.abs_set(ioxas_x, 254.8, wait=True)
    yield from E_ramp(dets, 882, 842, 0.1, deadband=6)
    yield from bps.abs_set(pgm_energy, 882, wait=True)

    yield from bps.abs_set(ioxas_x, 266.7, wait=True)
    yield from E_ramp(dets, 882, 842, 0.1, deadband=6)
    yield from bps.abs_set(pgm_energy, 882, wait=True)

    yield from bps.abs_set(ioxas_x, 278.6, wait=True)
    yield from E_ramp(dets, 882, 842, 0.1, deadband=6)
    yield from bps.abs_set(pgm_energy, 882, wait=True)

    yield from bps.abs_set(ioxas_x, 290.0, wait=True)
    yield from E_ramp(dets, 882, 842, 0.1, deadband=6)
    yield from bps.abs_set(pgm_energy, 882, wait=True)

#F K measurements
    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(pgm_energy, 705, wait=True)
    yield from bps.abs_set(epu1table, 6, wait=True)
    yield from bps.abs_set(epu1offset, 1, wait=True)
    yield from bps.sleep(10)
    yield from bps.abs_set(feedback, 1, wait=True)
    yield from bps.sleep(10)
    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(sample_sclr_gain, 1, wait=True)
    yield from bps.abs_set(sample_sclr_decade, 3, wait=True)
    yield from bps.abs_set(aumesh_sclr_gain, 0, wait=True)
    yield from bps.abs_set(aumesh_sclr_decade, 3, wait=True)
    yield from bps.abs_set(vortex.mca.rois.roi2.lo_chan, 700, wait=True)
    yield from bps.abs_set(vortex.mca.rois.roi2.hi_chan, 900, wait=True)

    yield from bps.abs_set(ioxas_x, 254.8, wait=True)
    yield from E_ramp(dets, 715, 680, 0.1, deadband=6)
    yield from bps.abs_set(pgm_energy, 715, wait=True)

    yield from bps.abs_set(ioxas_x, 266.7, wait=True)
    yield from E_ramp(dets, 715, 680, 0.1, deadband=6)
    yield from bps.abs_set(pgm_energy, 715, wait=True)

    yield from bps.abs_set(ioxas_x, 278.6, wait=True)
    yield from E_ramp(dets, 715, 680, 0.1, deadband=6)
    yield from bps.abs_set(pgm_energy, 715, wait=True)

    yield from bps.abs_set(ioxas_x, 290.0, wait=True)
    yield from E_ramp(dets, 715, 680, 0.1, deadband=6)
    yield from bps.abs_set(pgm_energy, 715, wait=True)

#Co L2,3 measurements
    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(pgm_energy, 785, wait=True)
    yield from bps.abs_set(epu1table, 6, wait=True)
    yield from bps.abs_set(epu1offset, 1, wait=True)
    yield from bps.sleep(10)
    yield from bps.abs_set(feedback, 1, wait=True)
    yield from bps.sleep(10)
    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(sample_sclr_gain, 1, wait=True)
    yield from bps.abs_set(sample_sclr_decade, 3, wait=True)
    yield from bps.abs_set(aumesh_sclr_gain, 0, wait=True)
    yield from bps.abs_set(aumesh_sclr_decade, 3, wait=True)
    yield from bps.abs_set(vortex.mca.rois.roi2.lo_chan, 900, wait=True)
    yield from bps.abs_set(vortex.mca.rois.roi2.hi_chan, 1000, wait=True)

    yield from bps.abs_set(ioxas_x, 254.8, wait=True)
    yield from E_ramp(dets, 810, 770, 0.1, deadband=6)
    yield from bps.abs_set(pgm_energy, 810, wait=True)

    yield from bps.abs_set(ioxas_x, 266.7, wait=True)
    yield from E_ramp(dets, 810, 770, 0.1, deadband=6)
    yield from bps.abs_set(pgm_energy, 810, wait=True)

    yield from bps.abs_set(ioxas_x, 278.6, wait=True)
    yield from E_ramp(dets, 810, 770, 0.1, deadband=6)
    yield from bps.abs_set(pgm_energy, 810, wait=True)

    yield from bps.abs_set(ioxas_x, 290.0, wait=True)
    yield from E_ramp(dets, 810, 770, 0.1, deadband=6)
    yield from bps.abs_set(pgm_energy, 810, wait=True)

# Make sure Au mesh is out of the way
    yield from bps.abs_set(au_mesh, -73.950, wait=True)

# C K measurements
    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(pgm_energy, 291.5, wait=True)
    yield from bps.abs_set(epu1table, 6, wait=True)
    yield from bps.abs_set(epu1offset, 1.5, wait=True)
    yield from bps.sleep(10)
    yield from bps.abs_set(feedback, 1, wait=True)
    yield from bps.sleep(10)
    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(sample_sclr_gain, 2, wait=True)
    yield from bps.abs_set(sample_sclr_decade, 2, wait=True)
    yield from bps.abs_set(aumesh_sclr_gain, 2, wait=True)
    yield from bps.abs_set(aumesh_sclr_decade, 2, wait=True)
    yield from bps.abs_set(vortex.mca.rois.roi2.lo_chan, 220, wait=True)
    yield from bps.abs_set(vortex.mca.rois.roi2.hi_chan, 400, wait=True)

    yield from bps.abs_set(ioxas_x, 253.8, wait=True)
    yield from E_ramp(dets, 320, 275, 0.05, deadband=4)
    yield from bps.abs_set(pgm_energy, 320, wait=True)

    yield from bps.abs_set(ioxas_x, 259.5, wait=True)
    yield from E_ramp(dets, 320, 275, 0.05, deadband=4)
    yield from bps.abs_set(pgm_energy, 320, wait=True)

    yield from bps.abs_set(ioxas_x, 265.7, wait=True)
    yield from E_ramp(dets, 320, 275, 0.05, deadband=4)
    yield from bps.abs_set(pgm_energy, 320, wait=True)

    yield from bps.abs_set(ioxas_x, 270.1, wait=True)
    yield from E_ramp(dets, 320, 275, 0.05, deadband=4)
    yield from bps.abs_set(pgm_energy, 320, wait=True)

    yield from bps.abs_set(ioxas_x, 277.6, wait=True)
    yield from E_ramp(dets, 320, 275, 0.05, deadband=4)
    yield from bps.abs_set(pgm_energy, 320, wait=True)

    yield from bps.abs_set(ioxas_x, 283.8, wait=True)
    yield from E_ramp(dets, 320, 275, 0.05, deadband=4)
    yield from bps.abs_set(pgm_energy, 320, wait=True)

    yield from bps.abs_set(ioxas_x, 289, wait=True)
    yield from E_ramp(dets, 320, 275, 0.05, deadband=4)
    yield from bps.abs_set(pgm_energy, 320, wait=True)

    yield from bps.abs_set(ioxas_x, 294.4, wait=True)
    yield from E_ramp(dets, 320, 275, 0.05, deadband=4)
    yield from bps.abs_set(pgm_energy, 320, wait=True)


def PD_scans():
    dets = [sclr, norm_ch4, ring_curr]
    for channel in ['channels.chan3','channels.chan4']:
        getattr(sclr, channel).kind = 'hinted'

    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(pgm_energy, 845, wait=True)
    yield from bps.abs_set(epu1table, 6, wait=True)
    yield from bps.abs_set(epu1offset, 0, wait=True)
    yield from bps.sleep(10)
    yield from bps.abs_set(feedback, 1, wait=True)
    yield from bps.abs_set(pd_sclr_gain, 2, wait=True)
    yield from bps.abs_set(pd_sclr_decade, 7, wait=True)
    yield from bps.abs_set(aumesh_sclr_gain, 2, wait=True)
    yield from bps.abs_set(aumesh_sclr_decade, 3, wait=True)
    yield from bps.abs_set(au_mesh, -76.3, wait=True)

    for ii in range(0,4):
        yield from bps.abs_set(pgm_energy, 845, wait=True)
        yield from E_ramp(dets, 845, 877, 0.1, deadband=8)

    for ii in range(0,4):
        yield from bps.abs_set(pgm_energy, 770, wait=True)
        yield from E_ramp(dets, 845, 885, 0.1, deadband=8)


    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(pgm_energy, 845, wait=True)
    yield from bps.abs_set(epu1table, 6, wait=True)
    yield from bps.abs_set(epu1offset, 0, wait=True)
    yield from bps.sleep(10)
    yield from bps.abs_set(feedback, 1, wait=True)
    yield from bps.abs_set(pd_sclr_gain, 1, wait=True)
    yield from bps.abs_set(pd_sclr_decade, 7, wait=True)
    yield from bps.abs_set(aumesh_sclr_gain, 2, wait=True)
    yield from bps.abs_set(aumesh_sclr_decade, 3, wait=True)
    yield from bps.abs_set(au_mesh, -106.3, wait=True)

    for ii in range(0,4):
        yield from bps.abs_set(pgm_energy, 845, wait=True)
        yield from E_ramp(dets, 845, 877, 0.1, deadband=8)

    for ii in range(0,4):
        yield from bps.abs_set(pgm_energy, 770, wait=True)
        yield from E_ramp(dets, 845, 885, 0.1, deadband=8)


    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(pgm_energy, 380, wait=True)
    yield from bps.abs_set(epu1table, 6, wait=True)
    yield from bps.abs_set(epu1offset, 0, wait=True)
    yield from bps.sleep(10)
    yield from bps.abs_set(feedback, 1, wait=True)
    yield from bps.abs_set(pd_sclr_gain, 2, wait=True)
    yield from bps.abs_set(pd_sclr_decade, 6, wait=True)
    yield from bps.abs_set(aumesh_sclr_gain, 1, wait=True)
    yield from bps.abs_set(aumesh_sclr_decade, 3, wait=True)

    for ii in range(0,4):
        yield from bps.abs_set(pgm_energy, 380, wait=True)
        yield from E_ramp(dets, 380, 430, 0.05, deadband=4)

    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(pgm_energy, 430, wait=True)
    yield from bps.abs_set(epu1table, 6, wait=True)
    yield from bps.abs_set(epu1offset, 0, wait=True)
    yield from bps.sleep(10)
    yield from bps.abs_set(feedback, 1, wait=True)
    yield from bps.abs_set(pd_sclr_gain, 2, wait=True)
    yield from bps.abs_set(pd_sclr_decade, 6, wait=True)
    yield from bps.abs_set(aumesh_sclr_gain, 1, wait=True)
    yield from bps.abs_set(aumesh_sclr_decade, 3, wait=True)

    for ii in range(0,4):
        yield from bps.abs_set(pgm_energy, 430, wait=True)
        yield from E_ramp(dets, 430, 470, 0.1, deadband=8)

    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(pgm_energy, 520, wait=True)
    yield from bps.abs_set(epu1table, 6, wait=True)
    yield from bps.abs_set(epu1offset, 0, wait=True)
    yield from bps.sleep(10)
    yield from bps.abs_set(feedback, 1, wait=True)
    yield from bps.abs_set(pd_sclr_gain, 0, wait=True)
    yield from bps.abs_set(pd_sclr_decade, 7, wait=True)
    yield from bps.abs_set(aumesh_sclr_gain, 2, wait=True)
    yield from bps.abs_set(aumesh_sclr_decade, 3, wait=True)

    for ii in range(0,4):
        yield from bps.abs_set(pgm_energy, 520, wait=True)
        yield from E_ramp(dets, 520, 570, 0.1, deadband=8)

    for ii in range(0,4):
        yield from bps.abs_set(pgm_energy, 520, wait=True)
        yield from E_ramp(dets, 520, 570, 0.05, deadband=8)

    for ii in range(0,4):
        yield from bps.abs_set(pgm_energy, 520, wait=True)
        yield from E_ramp(dets, 520, 565, 0.1, deadband=8)

    for ii in range(0,4):
        yield from bps.abs_set(pgm_energy, 525, wait=True)
        yield from E_ramp(dets, 525, 570, 0.1, deadband=8)

    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(pgm_energy, 655, wait=True)
    yield from bps.abs_set(epu1table, 6, wait=True)
    yield from bps.abs_set(epu1offset, 0, wait=True)
    yield from bps.sleep(10)
    yield from bps.abs_set(feedback, 1, wait=True)
    yield from bps.abs_set(pd_sclr_gain, 1, wait=True)
    yield from bps.abs_set(pd_sclr_decade, 7, wait=True)
    yield from bps.abs_set(aumesh_sclr_gain, 2, wait=True)
    yield from bps.abs_set(aumesh_sclr_decade, 3, wait=True)

    for ii in range(0,4):
        yield from bps.abs_set(pgm_energy, 655, wait=True)
        yield from E_ramp(dets, 655, 710, 0.1, deadband=8)

    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(pgm_energy, 770, wait=True)
    yield from bps.abs_set(epu1table, 6, wait=True)
    yield from bps.abs_set(epu1offset, 0, wait=True)
    yield from bps.sleep(10)
    yield from bps.abs_set(feedback, 1, wait=True)
    yield from bps.abs_set(pd_sclr_gain, 1, wait=True)
    yield from bps.abs_set(pd_sclr_decade, 7, wait=True)
    yield from bps.abs_set(aumesh_sclr_gain, 2, wait=True)
    yield from bps.abs_set(aumesh_sclr_decade, 3, wait=True)

    for ii in range(0,4):
        yield from bps.abs_set(pgm_energy, 770, wait=True)
        yield from E_ramp(dets, 770, 810, 0.1, deadband=6)

    for ii in range(0,4):
        yield from bps.abs_set(pgm_energy, 770, wait=True)
        yield from E_ramp(dets, 770, 810, 0.05, deadband=6)

#    yield from bps.abs_set(feedback, 0, wait=True)
#    yield from bps.abs_set(pgm_energy, 845, wait=True)
#    yield from bps.abs_set(epu1table, 6, wait=True)
#    yield from bps.abs_set(epu1offset, 0, wait=True)
#    yield from bps.sleep(10)
#    yield from bps.abs_set(feedback, 1, wait=True)
#    yield from bps.abs_set(pd_sclr_gain, 1, wait=True)
#    yield from bps.abs_set(pd_sclr_decade, 7, wait=True)
#    yield from bps.abs_set(aumesh_sclr_gain, 2, wait=True)
#    yield from bps.abs_set(aumesh_sclr_decade, 3, wait=True)

#    for ii in range(0,4):
#        yield from bps.abs_set(pgm_energy, 845, wait=True)
#        yield from E_ramp(dets, 845, 877, 0.1, deadband=8)

#    for ii in range(0,4):
#        yield from bps.abs_set(pgm_energy, 770, wait=True)
#        yield from E_ramp(dets, 845, 885, 0.1, deadband=8)

    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(pgm_energy, 870, wait=True)
    yield from bps.abs_set(epu1table, 6, wait=True)
    yield from bps.abs_set(epu1offset, 0, wait=True)
    yield from bps.sleep(10)
    yield from bps.abs_set(feedback, 1, wait=True)
    yield from bps.abs_set(pd_sclr_gain, 1, wait=True)
    yield from bps.abs_set(pd_sclr_decade, 7, wait=True)
    yield from bps.abs_set(aumesh_sclr_gain, 2, wait=True)
    yield from bps.abs_set(aumesh_sclr_decade, 3, wait=True)

    for ii in range(0,4):
        yield from bps.abs_set(pgm_energy, 870, wait=True)
        yield from E_ramp(dets, 870, 920, 0.1, deadband=8)

    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(pgm_energy, 925, wait=True)
    yield from bps.abs_set(epu1table, 6, wait=True)
    yield from bps.abs_set(epu1offset, 0, wait=True)
    yield from bps.sleep(10)
    yield from bps.abs_set(feedback, 1, wait=True)
    yield from bps.abs_set(pd_sclr_gain, 1, wait=True)
    yield from bps.abs_set(pd_sclr_decade, 7, wait=True)
    yield from bps.abs_set(aumesh_sclr_gain, 2, wait=True)
    yield from bps.abs_set(aumesh_sclr_decade, 3, wait=True)

    for ii in range(0,4):
        yield from bps.abs_set(pgm_energy, 925, wait=True)
        yield from E_ramp(dets, 925, 975, 0.1, deadband=8)

    for ii in range(0,4):
        yield from bps.abs_set(pgm_energy, 925, wait=True)
        yield from E_ramp(dets, 925, 960, 0.05, deadband=8)


    for ii in range(0,4):
        yield from bps.abs_set(pgm_energy, 925, wait=True)
        yield from E_ramp(dets, 925, 975, 0.05, deadband=8)

    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(pgm_energy, 1552, wait=True)
    yield from bps.abs_set(epu1table, 7, wait=True)
    yield from bps.abs_set(epu1offset, 8, wait=True)
    yield from bps.sleep(20)
    yield from bps.abs_set(feedback, 1, wait=True)
    yield from bps.abs_set(pd_sclr_gain, 0, wait=True)
    yield from bps.abs_set(pd_sclr_decade, 7, wait=True)
    yield from bps.abs_set(aumesh_sclr_gain, 0, wait=True)
    yield from bps.abs_set(aumesh_sclr_decade, 3, wait=True)

    for ii in range(0,4):
        yield from bps.abs_set(pgm_energy, 1552, wait=True)
        yield from E_ramp(dets, 1552, 1592, 0.05, deadband=1.2)

    yield from bps.abs_set(feedback, 0, wait=True)
    yield from bps.abs_set(pgm_energy, 1830, wait=True)
    yield from bps.abs_set(epu1table, 7, wait=True)
    yield from bps.abs_set(epu1offset, 10, wait=True)
    yield from bps.sleep(20)
    yield from bps.abs_set(feedback, 1, wait=True)
    yield from bps.abs_set(pd_sclr_gain, 0, wait=True)
    yield from bps.abs_set(pd_sclr_decade, 7, wait=True)
    yield from bps.abs_set(aumesh_sclr_gain, 0, wait=True)
    yield from bps.abs_set(aumesh_sclr_decade, 3, wait=True)

    for ii in range(0,4):
        yield from bps.abs_set(pgm_energy, 1830, wait=True)
        yield from E_ramp(dets, 1830, 1875, 0.1, deadband=4)   
    
    for ii in range(0,4):
        yield from bps.abs_set(pgm_energy, 1830, wait=True)
        yield from E_ramp(dets, 1830, 1875, 0.1, deadband=6)

    yield from bps.abs_set(diag4_y, 0, wait=True)
    yield from bps.abs_set(valve_mir3_close, 1, wait=True)


def O_K_Ctape():
    dets = [sclr, norm_ch4, ring_curr]
    for channel in ['channels.chan3','channels.chan4']:
        getattr(sclr, channel).kind = 'hinted'

    for ii in range(0,2):
        yield from bps.abs_set(pgm_energy, 520, wait=True)
        yield from E_ramp(dets, 520, 570, 0.1, deadband=8)

    for ii in range(0,2):
        yield from bps.abs_set(pgm_energy, 520, wait=True)
        yield from E_ramp(dets, 520, 570, 0.05, deadband=8)

    for ii in range(0,2):
        yield from bps.abs_set(pgm_energy, 520, wait=True)
        yield from E_ramp(dets, 520, 565, 0.1, deadband=8)

    for ii in range(0,2):
        yield from bps.abs_set(pgm_energy, 525, wait=True)
        yield from E_ramp(dets, 525, 570, 0.1, deadband=8)
 
