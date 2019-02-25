import sys
import matplotlib.pyplot as plt

def filter_target(g, g_err):
    # return 0 if bad observation
    if g <= 0 or g >= 90:
        return 0
    if g_err > 0.2:
        return 0
    return 1

ID = []

target = sys.argv[1]
band = int(sys.argv[2])
band = 3 * (band - 1)
i = int(sys.argv[3])

filename = target + '_list'
with open(filename) as f:
    lines = f.readlines()
    for line in lines:
        line = line.split()
        ID.append(line[1])

path = 'QSO_S82/'

t, g, g_err = [], [], []
filename = path + ID[i]
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
plt.errorbar(t, g, yerr=g_err)

plt.savefig('./light_curve/lc_' + str(ID[i]) + '.png')