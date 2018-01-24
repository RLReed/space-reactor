import sys
import os
import numpy as np

def makeCells(den, nControl, rods_in):
    s = 'c ******************************************************************************\n'
    s += 'c   CELL CARDS\n'
    s += 'c ******************************************************************************\n'
    s += '1 1 -{:6.4f} -11                                           IMP:P,N=1  $ fuel\n'.format(den)

    # Get the surface numbers for the rods
    drums = ['{}'.format(120 + i) + ('\n                ' if i % 10 == 9 else '') for i in range(nControl)]
    drums = ' '.join(drums)
    # 16, 22
    s += '2 3 -3.01 11 -12 {} IMP:P,N=1  $ reflector\n'.format(drums)
    s += '4 0  12                                                   IMP:P,N=0  $ graveyard\n'

    # Set control material
    mat_in = 4
    den_in = -2.52
    # Set reflector material
    mat_out = 3
    den_out = -3.01

    if not rods_in:
        # Switch mats
        mat_in, mat_out = mat_out, mat_in
        den_in, den_out = den_out, den_in


    # Make the control rods
    for i in range(nControl):
        # Control half
        s += '{} {} {:6.5f} -{} -{}  IMP:P,N=1 $ control\n'.format(20 + i, mat_in, den_in, 120 + i, 150 + i)
        # Reflector half
        s += '{} {} {:6.5f} -{} {}  IMP:P,N=1 $ control\n'.format(50 + i, mat_out, den_out, 120 + i, 150 + i)

    s += '\n'
    return s

def makeSurfs(inner_bot, inner_top, inner_r, outer_bot, outer_top, outer_r, nControl):
    s = 'c ******************************************************************************\n'
    s += 'c   SURFACE CARDS\n'
    s += 'c ******************************************************************************\n'
    s += '11 RCC 0 0 -{:5.3f}  0 0 {:5.3f} {:5.3f}  $ Inner (fuel) cylinder\n'.format(inner_bot, inner_top, inner_r)
    s += '12 RCC 0 0 -{:5.3f} 0 0 {:5.3f} {:5.3f}  $ Reflector\n'.format(outer_bot, outer_top, outer_r)

    # Fill 70% of the reflector space with a control rod drum
    center = (outer_r - inner_r) * 0.5
    control_r = (outer_r - inner_r) * 0.35
    max_r = np.pi * center / nControl * 0.99
    control_r = min(max_r, control_r)

    theta = np.linspace(0, 2 * np.pi, nControl + 1)[:-1]
    for i, t in enumerate(theta):
        # Define the rod cylinder
        x = (inner_r + center) * np.cos(t)
        y = (inner_r + center) * np.sin(t)
        s += '{:3d} RCC {:5.3f} {:5.3f} -{:5.3f} 0 0 {:5.3f} {:5.3f} $ Drum Cylinder\n'.format(120 + i, x, y, inner_bot, inner_top, control_r)

        # Define the rod plane
        A = x
        B = y
        C = 0
        D = x ** 2 + y ** 2
        s += '{:3d} P {:5.3f} {:5.3f} {:5.3f} {:5.3f} $ Drum Plane\n'.format(150 + i, A, B, C, D)
    s += '\n'
    return s

def makeData(fuel, h_bot, h_top, r, nRad):
    s = 'c ******************************************************************************\n'
    s += 'c   DATA CARDS\n'
    s += 'c ******************************************************************************\n'
    s += 'c\n'
    s += 'c *** Materials\n'
    s += fuel
    s += 'c tungsten carbide - density 15.6\n'
    s += 'm2         6000.82c -0.061256681\n'
    s += '          74182.82c -0.246200810\n'
    s += '          74183.82c -0.133585507\n'
    s += '          74184.82c -0.288355615\n'
    s += '          74186.82c -0.270601387\n'
    s += 'c berillium oxide reflector\n'
    s += 'm3         4009.82c .5 $ BeO'
    s += '           8016.82c .5 $ BeO\n'
    s += 'mt3 beo.62t $ BeO at 600 K\n'
    s += 'c Boron Carbide, Control - density 2.52\n'
    s += 'm4         5010.82c 2.1443e-02\n'
    s += '           5011.82c 8.6310e-02\n'
    s += '           6000.82c 2.7355e-02\n'
    s += 'c\n'
    s += 'c *** Problem Specification\n'
    s += 'mode  n\n'
    s += 'kcode 100000 1.000000 10 50\n'
    s += 'ksrc 0.0 1.5 0.0\n'
    s += 'F4:N 1\n'
    s += 'E4 1.00000000e-05   5.00000000e-03   1.00000000e-02   1.50000000e-02\n'
    s += '       2.00000000e-02   2.50000000e-02   3.00000000e-02   3.50000000e-02\n'
    s += '       4.20000000e-02   5.00000000e-02   5.80000000e-02   6.70000000e-02\n'
    s += '       8.00000000e-02   1.00000000e-01   1.40000000e-01   1.80000000e-01\n'
    s += '       2.20000000e-01   2.50000000e-01   2.80000000e-01   3.00000000e-01\n'
    s += '       3.20000000e-01   3.50000000e-01   4.00000000e-01   5.00000000e-01\n'
    s += '       6.25000000e-01   7.80000000e-01   8.50000000e-01   9.10000000e-01\n'
    s += '       9.50000000e-01   9.72000000e-01   9.96000000e-01   1.02000000e+00\n'
    s += '       1.04500000e+00   1.07100000e+00   1.09700000e+00   1.12300000e+00\n'
    s += '       1.15000000e+00   1.30000000e+00   1.50000000e+00   2.10000000e+00\n'
    s += '       2.60000000e+00   3.30000000e+00   4.00000000e+00   9.87700000e+00\n'
    s += '       1.59680000e+01   2.77000000e+01   4.80520000e+01   7.55014000e+01\n'
    s += '       1.48729000e+02   3.67263000e+02   9.06899000e+02   1.42510000e+03\n'
    s += '       2.23945000e+03   3.51910000e+03   5.53000000e+03   9.11800000e+03\n'
    s += '       1.50300000e+04   2.47800000e+04   4.08500000e+04   6.73400000e+04\n'
    s += '       1.11000000e+05   1.83000000e+05   3.02500000e+05   5.00000000e+05\n'
    s += '       8.21000000e+05   1.35300000e+06   2.23100000e+06   3.67900000e+06\n'
    s += '       6.06550000e+06   1.00000000e+07\n'
    s += 'FMESH14:n GEOM=CYL ORIGIN=0.,0.,-{} IMESH={} JMESH={} KMESH=1\n'.format(h_bot, h_top, r)
    s += '          IINTS={} JINTS=35 KINTS=1 OUT=CF AXS=0 0 1 VEC=1 0 0\n'.format(nRad)
    s += '          EMESH=1.00000000e-05, 5.00000000e-03, 1.00000000e-02,  1.50000000e-02,\n'
    s += '           2.00000000e-02,   2.50000000e-02,   3.00000000e-02,   3.50000000e-02,\n'
    s += '           4.20000000e-02,   5.00000000e-02,   5.80000000e-02,   6.70000000e-02,\n'
    s += '           8.00000000e-02,   1.00000000e-01,   1.40000000e-01,   1.80000000e-01,\n'
    s += '           2.20000000e-01,   2.50000000e-01,   2.80000000e-01,   3.00000000e-01,\n'
    s += '           3.20000000e-01,   3.50000000e-01,   4.00000000e-01,   5.00000000e-01,\n'
    s += '           6.25000000e-01,   7.80000000e-01,   8.50000000e-01,   9.10000000e-01,\n'
    s += '           9.50000000e-01,   9.72000000e-01,   9.96000000e-01,   1.02000000e+00,\n'
    s += '           1.04500000e+00,   1.07100000e+00,   1.09700000e+00,   1.12300000e+00,\n'
    s += '           1.15000000e+00,   1.30000000e+00,   1.50000000e+00,   2.10000000e+00,\n'
    s += '           2.60000000e+00,   3.30000000e+00,   4.00000000e+00,   9.87700000e+00,\n'
    s += '           1.59680000e+01,   2.77000000e+01,   4.80520000e+01,   7.55014000e+01,\n'
    s += '           1.48729000e+02,   3.67263000e+02,   9.06899000e+02,   1.42510000e+03,\n'
    s += '           2.23945000e+03,   3.51910000e+03,   5.53000000e+03,   9.11800000e+03,\n'
    s += '           1.50300000e+04,   2.47800000e+04,   4.08500000e+04,   6.73400000e+04,\n'
    s += '           1.11000000e+05,   1.83000000e+05,   3.02500000e+05,   5.00000000e+05,\n'
    s += '           8.21000000e+05,   1.35300000e+06,   2.23100000e+06,   3.67900000e+06,\n'
    s += '           6.06550000e+06,   1.00000000e+07\n'
    return s

def getFuel(nFuel):
    if nFuel == 1:
        fuel = 'c uranium dioxide - density 10.97\n'
        fuel += 'm1         8016.84c -0.119749645\n'
        fuel += '          92235.84c -0.817852652\n'
        fuel += '          92238.84c -0.062344659\n'
        fuel += '           1001.82c -0.000053044\n'
        dens = 10.97
    elif nFuel == 2:
        fuel = 'c uranium carbide - density 13.63\n'
        fuel += 'm1         6000.84c -0.0485396624\n'
        fuel += '          92235.84c -0.8840286010\n'
        fuel += '          92238.84c -0.0673892313\n'
        fuel += '           1001.82c -0.0000425054\n'
        dens = 13.6
    elif nFuel == 3:
        fuel = 'c uranium carbide - density 13.63\n'
        fuel += 'm1         92235.85c 0.0008888\n'
        fuel += '           92238.85c 0.0000275\n'
        fuel += '           40000.80c 0.0292010\n'
        fuel += '           41093.80c 0.0097337\n'
        fuel += '           6000.80c 0.0398509\n'
        fuel += 'mt2 grph.08t $2000 K graph, fuel @ 3000\n'
        dens = 14.155260188
    return fuel, dens

def makeMCNP(r, t, h, nControl, rods_in):
    nFuel = 2
    fuel, dens = getFuel(nFuel)

    s = 'TrigaModel\n'
    s += makeCells(0.25 * dens, nControl, rods_in)
    s += makeSurfs(h, 2 * h, r, h + t, 2 * h + 2 * t, r + t, nControl)
    s += makeData(fuel, h, 2 * h, int(r), int(r))

    path = '{}-control/rod-{}/'.format(nControl, 'in' if rods_in else 'out')
    if not os.path.exists(path):
        os.makedirs(path)
    name = path + 'r{:5.3f}h{:5.3f}t{:5.3f}.i'.format(r, h, t)
    with open(name, 'w') as f:
        f.write(s)
    os.system('mcnp6 name={} tasks 28'.format(name))

if __name__ == "__main__":
    nControl = 2
    rods_in = False
    for h in np.linspace(15, 25, 11):
        for t in np.linspace(2, 18, 11):
            for r in np.linspace(8, 28, 11):
                makeMCNP(r=r, t=t, h=h, nControl=nControl, rods_in=rods_in)



