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

data = np.loadtxt('uo2/data').T
K = data[0]
D = data[1]
R = data[2]
T = data[3]
H = data[4] * 2
M = data[5]

hmin, hmax = 5, 50
tmin, tmax = 2, 20
rmin, rmax = 2, 20

rgb = [((R[i]-rmin)/rmax, (H[i]-hmin)/hmax, (T[i]-tmin)/tmax) for i in range(len(K))]
red_patch = mpatches.Patch(color='red', label='Foam Radius')
green_patch = mpatches.Patch(color='green', label='Foam Height')
blue_patch = mpatches.Patch(color='blue', label='Reflector Thickness')

# Radius plot
plt.scatter(R, K, c=rgb)
plt.ylabel('k')
plt.xlabel('radius [cm]')
plt.xlim([0, rmax])
plt.legend(handles=[red_patch, green_patch, blue_patch])
plt.savefig('k-radius.pdf')
plt.clf()

# Thickness plot
plt.scatter(T, K, c=rgb)
plt.ylabel('k')
plt.xlim([0, tmax])
plt.xlabel('reflector thickness [cm]')
plt.legend(handles=[red_patch, green_patch, blue_patch])
plt.savefig('k-thick.pdf')
plt.clf()

# Height plot
plt.scatter(H, K, c=rgb)
plt.ylabel('k')
plt.xlim([0, hmax])
plt.xlabel('height [cm]')
plt.legend(handles=[red_patch, green_patch, blue_patch])
plt.savefig('k-height.pdf')
plt.clf()

# Mass plot
plt.scatter(M / 1000, K, c=rgb)
plt.ylabel('k')
plt.xlabel('mass [kg]')
plt.xlim([0.0, 6000])
plt.legend(handles=[red_patch, green_patch, blue_patch])
plt.savefig('k-mass.pdf')
plt.clf()

i = np.argmin(M[K > 1.0])
print data[:,K > 1.0][:,i]
