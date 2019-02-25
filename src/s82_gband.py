import sys
import random
import numpy as np
from astropy.io import fits

np.set_printoptions(threshold=np.inf)

def parse_s82(filename):
    # read out s82 ID of each source and their ra / dec
    ID, ra, dec = [], [], []
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
            try:
                ID.append(int(line[0]))
                ra.append(float(line[1]))
                dec.append(float(line[2]))
            except:
                pass
    return ID, ra, dec

def filter_target(g, g_err):
    # return 0 if bad observation
    if g <= 0 or g >= 90:
        return 0
    if g_err > 0.2:
        return 0
    return 1

def seletc_EVQ(path, ID):
    # select light variation > 1 in g band
    # ! -- reconstruct -- !
    # seperate specific method from selection function    
    targets = []

    for i in ID:
        g, r = [], []
        filename = path + str(i)	
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                line = line.split()
                _g = float(line[4])
                _g_err = float(line[5])
                _r = float(line[7])
                _r_err = float(line[8])
                if filter_target(_g, _g_err) and filter_target(_r, _r_err):
                    g.append(_g)
                    r.append(_r)
        if g:
            if max(g) - min(g) > 0.8:
                if r[g.index(max(g))] - r[g.index(min(g))] > 0.6:
                    targets.append(i)
    return targets

def parse_fits(fits_file):
    # read out dr7 fits file
    # find sources in s82 and record information
    # for now: sdss_name, ra, dec, redshift, plate, fiber, mjd,
    # loglbol, loglbol_err, logbh, loghbh_err are included
    # ! -- reconstruct -- !
    dat = fits.open(fits_file)

    dr7s = []
    sdss_name = dat[1].data['SDSS_NAME']
    ra = dat[1].data['RA']
    dec = dat[1].data['DEC']
    z = dat[1].data['REDSHIFT']
    plate = dat[1].data['PLATE']
    fiber = dat[1].data['FIBER']
    MJD = dat[1].data['MJD']
    L = dat[1].data['LOGLBOL']
    L_err = dat[1].data['LOGLBOL_ERR']
    M = dat[1].data['LOGBH']
    M_err = dat[1].data['LOGBH_ERR']

    for i in range(len(dat[1].data)):
        dr7 = {}
        dr7['SDSS_NAME'] = sdss_name[i]
        dr7['RA'] = ra[i]
        dr7['DEC'] = dec[i]
        dr7['REDSHIFT'] = z[i]
        dr7['PLATE'] = plate[i]
        dr7['FIBER'] = fiber[i]
        dr7['MJD'] = MJD[i]
        dr7['LOGLBOL'] = L[i]
        dr7['LOGLBOL_ERR'] = L_err[i]
        dr7['LOGBH'] = M[i]
        dr7['LOGBH_ERR'] = M_err[i]
        dr7s.append(dr7)
    return dr7s

def gen_tar(ID, ra, dec, targets):
    id_tar, ra_tar, dec_tar = [], [], []
    for i in range(len(ID)):
        if ID[i] in targets:
            id_tar.append(ID[i])
            ra_tar.append(ra[i])
            dec_tar.append(dec[i])
    return id_tar, ra_tar, dec_tar

def gen_oth(ID, ra, dec, targets):
    id_oth, ra_oth, dec_oth = [], [], []
    for i in range(len(ID)):
        if ID[i] not in targets:
            id_oth.append(ID[i])
            ra_oth.append(ra[i])
            dec_oth.append(dec[i])
    return id_oth, ra_oth, dec_oth

def gen_rnd(ID, ra, dec):
    id_rnd, ra_rnd, dec_rnd = [], [], []
    rnd = list(np.random.randint(0, len(ID)-1, size=700))
    for i in range(700):
        id_rnd.append(ID[rnd[i]])
        ra_rnd.append(ra[rnd[i]])
        dec_rnd.append(dec[rnd[i]])
    return id_rnd, ra_rnd, dec_rnd

def s82_dic(ID, ra, dec):
    targets = []
    for i in range(len(ID)):
        target = {}
        target['ID'] = ID[i]
        target['RA'] = ra[i]
        target['DEC'] = dec[i]
        targets.append(target)
    return targets

def s82_output(s82s, dr7s):
    for s82 in s82s:
        for dr7 in dr7s:
            if abs(s82['RA'] - dr7['RA']) < 0.0001 and abs(s82['DEC'] - dr7['DEC']) < 0.0001:
                if dr7['LOGLBOL'] > 0 and dr7['LOGBH'] > 0:
                    print(dr7['SDSS_NAME'], s82['ID'], 
                    dr7['REDSHIFT'], dr7['LOGLBOL'], dr7['LOGBH'])
                    # print(dr7['SDSS_NAME'], s82['ID'])
                    # print(dr7['MJD'])
                break

s82_file = 'data/DB_QSO_S82.dat' # stripe 82 brief info
s82_folder = 'data/QSO_S82/' # observation of each source in stripe 82
dr7_file = 'data/dr7_bh_Nov19_2013.fits' # dr7 fits file

ID, ra, dec = parse_s82(s82_file)
dr7s = parse_fits(dr7_file)
# dr7 = { 'SDSS_NAME': ***, 'RA': ***, 'DEC': ***, ...}
# sdss_name, ra, dec, redshift, plate, fiber, mjd,
# loglbol, loglbol_err, logbh, loghbh_err are included in dr7
# dr7s is a list of dr7 item

targets = seletc_EVQ(s82_folder, ID)

atr = sys.argv[1]
if atr == 'all':
    s82_all = s82_dic(ID, ra, dec)
    s82_output(s82_all, dr7s)
elif atr == 'tar':
    id_tar, ra_tar, dec_tar = gen_tar(ID, ra, dec, targets)
    s82_tar = s82_dic(id_tar, ra_tar, dec_tar)
    s82_output(s82_tar, dr7s)
elif atr == 'oth':
    id_oth, ra_oth, dec_oth = gen_oth(ID, ra, dec, targets)
    s82_oth = s82_dic(id_oth, ra_oth, dec_oth)
    s82_output(s82_oth, dr7s)
elif atr == 'rnd':
    id_rnd, ra_rnd, dec_rnd = gen_rnd(ID, ra, dec)
    s82_rnd = s82_dic(id_rnd, ra_rnd, dec_rnd)
    s82_output(s82_rnd, dr7s)
else:
    print('no such attribute', file=sys.stderr)
