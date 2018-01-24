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

def process(name):
    f = open(name + '.io', 'r').readlines()
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
        elif 'cell  1' in line:
            phi = []
            for j in range(70):
                phi.append(f[i+2+j].split())
            phi = np.array(phi).astype(float).T
            e = np.concatenate((np.array([1e-8]), phi[0])) * 1e6
            phi = phi[1] * 3.12e16
            e, phi = barchart(e, phi)

    plt.loglog(e, phi)
    plt.xlabel('energy [eV]')
    plt.ylabel('$\phi$ [n cm$^{-2}$ s$^{-1}$]')
    plt.xlim([1e-3, 2e7])
    plt.savefig('{}_flux.png'.format(name))
    plt.clf()

    return k, d

def barchart(x, y):
    assert(len(x) == len(y) + 1)
    X = [x[0]] + [xx for xx in x[1:-1] for i in range(2)] + [x[-1]]
    Y = [yy for yy in y for i in range(2)]
    return np.array(X), np.array(Y)


if __name__ == "__main__":
    for name in ['best-{}-in'.format(N) for N in [2, 4, 8, 12]]:
        k, d = process(name)

