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

def process(r, t, h):
    f = open('r{:5.3f}h{:5.3f}t{:5.3f}.io'.format(r, h, t), 'r').readlines()
    for i, line in enumerate(f):
        if 'the final estimated combined collision/absorption/track-length keff = ' in line:
            k = float(line.split()[8])
            d = float(line.split()[-2])
        elif 'no final keff results will be printed because all three keff estimator active data' in line:
            k = float(f[i+11].split()[2])
            d = float(f[i+11].split()[3])
    
    return k, d
    
def barchart(x, y):
    assert(len(x) == len(y) + 1)
    X = [x[0]] + [xx for xx in x[1:-1] for i in range(2)] + [x[-1]]
    Y = [yy for yy in y for i in range(2)]
    return np.array(X), np.array(Y)

    
if __name__ == "__main__":
    data = np.zeros((1000,6))
    count = 0
    for h in np.linspace(2.5, 25, 10):
        for t in np.linspace(2, 20, 10):
            for r in np.linspace(2, 20, 10):
                V_inside = np.pi * r ** 2 * 2 * h
                V_outside = np.pi * (r + t) ** 2 * (2 * h + 2 * t) - V_inside
                m = 0.25 * 10.97 * V_inside + 3.01 * V_outside
                k, d = process(r, t, h)
                data[count] = [k, d, r, t, h, m]
                count += 1
    
    np.savetxt('data', data)

