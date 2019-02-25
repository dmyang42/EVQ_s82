import sys
from math import sqrt

def filter_target(g, g_err):
    # return 0 if bad observation
    if g <= 0 or g >= 90:
        return 0
    if g_err > 0.2:
        return 0
    return 1

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

ID = []

target = sys.argv[1]
band = int(sys.argv[2])
band = 3 * (band - 1)
# 1 for u

filename = target + '_list'
with open(filename) as f:
    lines = f.readlines()
    for line in lines:
        line = line.split()
        ID.append(line[1])

path = 'QSO_S82/'

deltas = []
for i in ID:
    t, g, g_err = [], [], []
    filename = path + i	
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
            _t = float(line[band])
            _g = float(line[band + 1])
            _g_err = float(line[band + 2])
            if filter_target(_g, _g_err):    
                t.append(_t)
                g.append(_g)
                g_err.append(_g_err)

    i = 0
    while i < len(t):
        j = i
        while j < len(t) - 1:
            delta = []
            delta_t = t[j + 1] - t[i]
            # print(delta_t)
            delta_g = g[j + 1] - g[i]
            if delta_t >= 100.0:
                try:
                    radicant = 1 - (g_err[j + 1] ** 2 + g_err[i] ** 2) / (delta_g ** 2)
                except ZeroDivisionError:
                    radicant = 0
                    pass
                else:
                    pass
                if radicant > 0:
                    delta_g = delta_g * sqrt(radicant)
                    delta.append(delta_t)
                    delta.append(delta_g)
                    deltas.append(delta)
                else:
                    delta.append(delta_t)
                    delta.append(0)
                    deltas.append(delta)
            # print(delta_t, delta_g)
            j = j + 1
        i = i + 1
deltas.sort()

for i in range(len(deltas)):
    print(deltas[i][0], deltas[i][1])
