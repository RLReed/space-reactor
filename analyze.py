import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font',**{'family':'serif'})
from matplotlib import rcParams
rcParams['xtick.direction'] = 'out'
rcParams['ytick.direction'] = 'out'
rcParams['xtick.labelsize'] = 18
rcParams['ytick.labelsize'] = 18
rcParams['lines.linewidth'] = 1.85
rcParams['axes.labelsize'] = 20
rcParams.update({'figure.autolayout': True})

def process(r, t, h, n, b):
    f = open('{}-control/rod-{}/r{:5.3f}h{:5.3f}t{:5.3f}.io'.format(n, 'in' if b else 'out', r, h, t), 'r').readlines()
    for i, line in enumerate(f):
        if 'the final estimated combined collision/absorption/track-length keff = ' in line:
            k = float(line.split()[8])
            d = float(line.split()[-2])
        elif 'no final keff results will be printed because all three keff estimator active data' in line:
            k = float(f[i+11].split()[2])
            d = float(f[i+11].split()[3])
        elif 'no final keff results will be printed because only ' in line:
            k = float(f[i+9].split()[1])
            d = float(f[i+9].split()[2])

    return k, d

def barchart(x, y):
    assert(len(x) == len(y) + 1)
    X = [x[0]] + [xx for xx in x[1:-1] for i in range(2)] + [x[-1]]
    Y = [yy for yy in y for i in range(2)]
    return np.array(X), np.array(Y)


if __name__ == "__main__":
    for nControl in [2, 4, 8, 12]:
        for rods_in in [True, False]:
            print nControl, rods_in
            data = np.zeros((1000, 6))
            count = 0
            for h in np.linspace(2.5, 25, 10):
                for t in np.linspace(2, 20, 10):
                    for r in np.linspace(2, 20, 10):
                        outer_r = r + t
                        center = (outer_r - r) * 0.5
                        control_r = (outer_r - r) * 0.35
                        max_r = np.pi * center / nControl * 0.99
                        control_r = min(max_r, control_r)


                        V_inside = np.pi * r ** 2 * 2 * h
                        V_outside = np.pi * (r + t) ** 2 * (2 * h + 2 * t) - V_inside
                        V_rods = nControl * control_r ** 2 * h
                        m = 0.25 * 10.97 * V_inside + 3.01 * (V_outside - V_rods) + V_rods * 2.52
                        k, d = process(r, t, h, nControl, rods_in)
                        data[count] = [k, d, r, t, h, m]
                        count += 1
            print k
            np.savetxt('data-{}-{}'.format(nControl, 'in' if rods_in else 'out'), data)

