import sys
import numpy as np
from scipy.stats import ks_2samp

def open_file(filename):
	name, ID, z, L, M = [], [], [], [], []
	with open(filename) as f:
		lines = f.readlines()
		for line in lines:
			line = line.split()
			name.append(line[0])
			ID.append(line[1])
			z.append(float(line[2]))
			L.append(float(line[3]))
			M.append(float(line[4]))
	return name, ID, z, L, M

def ks_tests(z, z_tar, L, L_tar, M, M_tar):
	return ks_2samp(z, z_tar).pvalue, ks_2samp(L, L_tar).pvalue, ks_2samp(M, M_tar).pvalue

def print_info(z_oth, z_tar, L_oth, L_tar, M_oth, M_tar, f):
	print(len(z_oth), file=f)
	r1, r2, r3 = ks_tests(z_oth, z_tar, L_oth, L_tar, M_oth, M_tar)
	print(r1, r2, r3, sep='\n', file=f)

def sample_filter(iter_times, flg, name_oth, ID_oth, z_oth, z_tar, L_oth, L_tar, M_oth, M_tar, f):
	pz, pL, pM = ks_tests(z_oth, z_tar, L_oth, L_tar, M_oth, M_tar)
	for j in range(iter_times):
		i = np.random.randint(0, len(z_oth)-1)
		name1, name2 = name_oth[0:i], name_oth[i+1:]
		name = name1 + name2
		ID1, ID2 = ID_oth[0:i], ID_oth[i+1:]
		ID = ID1 + ID2
		z1, z2 = z_oth[0:i], z_oth[i+1:]
		z = z1 + z2
		L1, L2 = L_oth[0:i], L_oth[i+1:]
		L = L1 + L2
		M1, M2 = M_oth[0:i], M_oth[i+1:]
		M = M1 + M2
		pz_t, pL_t, pM_t = ks_tests(z, z_tar, L, L_tar, M, M_tar)
		if  (pz_t > pz or flg != 1)\
		and (pL_t > pL or flg != 2)\
		and (pM_t > pM or flg != 3):
			name_oth, ID_oth = name, ID
			z_oth, L_oth, M_oth = z, L, M
			pz, pL, pM = pz_t, pL_t, pM_t
	print_info(z_oth, z_tar, L_oth, L_tar, M_oth, M_tar, f)
	return name_oth, ID_oth, z_oth, L_oth, M_oth

p = float(sys.argv[1])

log = open('gen.log', 'w')
dat = open('s82_ftr', 'w')

name_oth, ID_oth, z_oth, L_oth, M_oth = open_file('s82_oth')

name_tar, ID_tar, z_tar, L_tar, M_tar = open_file('s82_tar')

for i in range(8000):
	if ks_2samp(z_oth, z_tar).pvalue < p:
		name_oth, ID_oth, z_oth, L_oth, M_oth = sample_filter(3, 1, name_oth, ID_oth, z_oth, z_tar, L_oth, L_tar, M_oth, M_tar, log)
	if ks_2samp(L_oth, L_tar).pvalue < p:
		name_oth, ID_oth, z_oth, L_oth, M_oth = sample_filter(3, 2, name_oth, ID_oth, z_oth, z_tar, L_oth, L_tar, M_oth, M_tar, log)
	if ks_2samp(M_oth, M_tar).pvalue < p:
		name_oth, ID_oth, z_oth, L_oth, M_oth = sample_filter(3, 3, name_oth, ID_oth, z_oth, z_tar, L_oth, L_tar, M_oth, M_tar, log)

for i in range(len(z_oth)):
	print(name_oth[i], ID_oth[i], z_oth[i], L_oth[i], M_oth[i], file=dat)
	# print(name_oth[i], ID_oth[i], file=dat)

log.close()
dat.close()
