import sys
import random
import numpy as np
import matplotlib.pyplot as plt
from math import log10

def binary_search(num, x):
    left, right = 0, len(num)
    while left < right:
        mid = int((left + right) / 2)
        if num[mid] > x:
            right = mid
        elif num[mid] < x:
            left = mid + 1
        elif num[mid] == x:
            return mid
    return mid

def avrg(g_temp):
    return sum(g_temp) / len(g_temp)

def struct_func(g_temp):
    # IQR as structure function
    g_temp.sort()
    lower = int(0.25 * len(g_temp))
    upper = int(0.75 * len(g_temp))
    IQR_lower = g_temp[lower]
    IQR_upper = g_temp[upper]
    
    sf = 0.74 * (IQR_upper - IQR_lower) 
    return sf

def bootstrap(mags, func):
    mags_rnd = []
    sfs = [] # structure function
    for j in range(1000):
        for i in range(1000):
            if len(mags) <= 1:
                print('shit!')
            rnd = random.randint(0, len(mags) - 1)
            mags_rnd.append(mags[rnd])
        sfs.append(func(mags_rnd))
    return sfs

def read_list(filename):
    t, g = [], []
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
            t.append(float(line[0]))
            g.append(float(line[1]))
    return t, g

def pivot_list(t, d, log_min, n):
    pivots = [] # n等分点
    pivots.append(0)
    for i in range(n - 1):
        pivot = 10 ** (log_min + d * (i + 1))
        pivot = binary_search(t, pivot)
        pivots.append(pivot)
    pivots.append(len(t) - 1)
    return pivots

def tau_list(pivots, d, log_min):
	taus, log_taus = [], []
	for i in range(len(pivots) - 1):
		tau = log_min + d * (2 * i + 1) / 2
		taus.append(10 ** tau)
		log_taus.append(tau)
	return taus, log_taus

def error_list(pivots, g):
    # 利用bootstrap计算每个bin的误差
    errors = []
    for i in range(len(pivots) - 1):
        #print(np.std(bootstrap(g[pivots[i]:pivots[i+1]]), ddof=1))
        error = np.std(bootstrap(g[pivots[i]:pivots[i+1]], struct_func), ddof=1)
        errors.append(error)
    return errors

def sf_list(pivots, g):
    # 计算每个bin的结构函数值 
    sfs = []
    for i in range(len(pivots) - 1):
        g_bin = g[pivots[i]:pivots[i + 1]]
        sf = struct_func(g_bin)
        sfs.append(sf)
    return sfs

def print_list(taus, d, sfs, errors):
    print(taus, d, sfs, errors, sep='\n')

def plot_line(taus, sfs, yerrs):
	plt.errorbar(taus, sfs, yerr=yerrs)

def plot_bin(log_tau, d, sfs):
	for i in range(len(log_tau)):
		y = sfs[i]
		x1 = 10 ** (log_tau[i] - d / 2)
		x2 = 10 ** (log_tau[i] + d / 2)	
		plt.hlines(y, x1, x2)

def bin(filename, n):
    # 输入一组源的list
    t, g = read_list(filename)

    log_min = log10(min(t))
    log_max = log10(max(t))
    d = (log_max - log_min) / n

    pivots = pivot_list(t, d, log_min, n) # 用于分bin
    taus, log_taus = tau_list(pivots, d, log_min) # 用于绘图
    errors = error_list(pivots, g)
    sfs = sf_list(pivots, g)
    # print_list(taus, d, sfs, errors)

    plot_line(taus, sfs, errors)
    plot_bin(log_taus, d, sfs)
    return log_min, log_max

def bin_2(filename, n, log_min, log_max):
    # 输入一组源的list
    t, g = read_list(filename)

    d = (log_max - log_min) / n

    pivots = pivot_list(t, d, log_min, n) # 用于分bin
    taus, log_taus = tau_list(pivots, d, log_min) # 用于绘图
    errors = error_list(pivots, g)
    sfs = sf_list(pivots, g)
    # print_list(taus, d, sfs, errors)

    plot_line(taus, sfs, errors)
    plot_bin(log_taus, d, sfs)

n = int(sys.argv[1]) # n等分log下时标
band_id = sys.argv[2]
EVQ_file = 'cache/delta_EVQ_' + band_id
match_file = 'cache/delta_match_' + band_id
# EVQ_file = 'delta_EVQ'
# match_file = 'delta_match'
# oth_file = 'delta_oth_' + band_id
# bin(oth_file, n)
log_min, log_max = bin(EVQ_file, n)
bin_2(match_file, n, log_min, log_max)

band = ['u', 'g', 'r', 'i', 'z']
title = 'SF in ' + band[int(band_id) - 1] + ' band'
plt.title(title)
plt.xscale('log')
plt.yscale('log')
plt.xlabel(r'$\tau$ [day]')
plt.ylabel('SF [mag]')
# plt.show()
png = 'figure/tau_sf_' + band[int(band_id) - 1] + '.png'
plt.savefig(png, dpi=2000)
