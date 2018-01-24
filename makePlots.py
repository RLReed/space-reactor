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
import matplotlib.patches as mpatches

def makePlot(nControl):
    dataIn = np.loadtxt('data-{}-in'.format(nControl)).T
    dataOut = np.loadtxt('data-{}-out'.format(nControl)).T

    K = dataIn[0]
    D = dataIn[1]
    R = dataIn[2]
    T = dataIn[3]
    H = dataIn[4] * 2
    M = dataIn[5]

    K_out = dataOut[0]
    D_out = dataOut[1]

    hmin, hmax = 5, 50
    tmin, tmax = 2, 20
    rmin, rmax = 2, 20

    mask = (K < 1.0) * (1.0 < K_out)

    rgb = [((R[i]-rmin)/rmax, (H[i]-hmin)/hmax, (T[i]-tmin)/tmax) for i in range(len(K)) if mask[i]]
    red_patch = mpatches.Patch(color='red', label='Foam Radius')
    green_patch = mpatches.Patch(color='green', label='Foam Height')
    blue_patch = mpatches.Patch(color='blue', label='Reflector Thickness')

    # Radius plot
    plt.scatter(R[mask], K[mask], c=rgb)
    plt.ylabel('k')
    plt.xlabel('radius [cm]')
    plt.xlim([0, rmax])
    plt.legend(handles=[red_patch, green_patch, blue_patch])
    plt.savefig('k-radius-{}.pdf'.format(nControl))
    plt.clf()

    # Thickness plot
    plt.scatter(T[mask], K[mask], c=rgb)
    plt.ylabel('k')
    plt.xlim([0, tmax])
    plt.xlabel('reflector thickness [cm]')
    plt.legend(handles=[red_patch, green_patch, blue_patch])
    plt.savefig('k-thick-{}.pdf'.format(nControl))
    plt.clf()

    # Height plot
    plt.scatter(H[mask], K[mask], c=rgb)
    plt.ylabel('k')
    plt.xlim([0, hmax])
    plt.xlabel('height [cm]')
    plt.legend(handles=[red_patch, green_patch, blue_patch])
    plt.savefig('k-height-{}.pdf'.format(nControl))
    plt.clf()

    # Mass plot
    plt.scatter(M[mask] / 1000, K[mask], c=rgb)
    plt.ylabel('k')
    plt.xlabel('mass [kg]')
    plt.xlim([0.0, 6000])
    plt.legend(handles=[red_patch, green_patch, blue_patch])
    plt.savefig('k-mass-{}.pdf'.format(nControl))
    plt.clf()

    i = np.argmin(M[K_out > 1.0])
    print 'k={}, d={}, r={}, t={}, h={}, m={}'.format(*dataIn[:,K_out > 1.0][:,i])
    print 'k_out={}'.format(K_out[K_out > 1.0][i])

for nControl in [12, 4, 8, 12]:
    makePlot(nControl)
