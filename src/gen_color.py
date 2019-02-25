import sys

def filter_target(g, g_err, r, r_err):
    # return 0 if bad observation
    if g <= 0 or g >= 90 or r <= 0 or r >= 90:
        return 0
    if g_err > 0.2 or r_err > 0.2:
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

filename = target + '_list'
with open(filename) as f:
    lines = f.readlines()
    for line in lines:
        line = line.split()
        ID.append(line[1])

path = 'QSO_S82/'

deltas = []
for i in ID:
    t, g, r, g_err, r_err = [], [], [], [], []
    filename = path + i	
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
            _t = float(line[3])
            _g = float(line[4])
            _r = float(line[7])
            _g_err = float(line[5])
            _r_err = float(line[8])
            if filter_target(_g, _g_err, _r, _r_err):    
                t.append(_t)
                g.append(_g)
                r.append(_r)
                g_err.append(_g_err)
                r_err.append(_r_err)

    i = 0
    while i < len(t):
        j = i
        while j < len(t) - 1:
            delta = []
            delta_t = t[j + 1] - t[i]
            # print(delta_t)
            delta_g = g[j + 1] - g[i]
            delta_r = r[j + 1] - r[i]
            delta_g_err = g_err[j + 1] + g_err[i]
            delta_r_err = r_err[j + 1] + r_err[i]
            if delta_t >= 30.0: ##epoch threshold
                delta.append(delta_t)
                delta.append(delta_g)
                delta.append(delta_r)
                delta.append(delta_g_err)
                delta.append(delta_r_err)
                deltas.append(delta)
            # print(delta_t, delta_g)
            j = j + 1
        i = i + 1
deltas.sort()

for i in range(len(deltas)):
    if(deltas[i][0]>3400):
        pass
    print(deltas[i][0], deltas[i][1], deltas[i][2], deltas[i][3], deltas[i][4])