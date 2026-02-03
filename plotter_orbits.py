#Plotting orbits

from imports import imageio
from imports import np
from imports import plt
from imports import pd
from imports import os
from imports import csv
from functions_earthMoon import x_E_Circular, x_M_Circular
import matplotlib 

dt = 1

outputRK = pd.read_csv("FINAL-rk4 dt=1/-444248469.0/rocket.csv")
xsRK = np.array(outputRK.x)
ysRK = np.array(outputRK.y)

outputT = pd.read_csv("FINAL-T dt=1/-444248469.0/rocket.csv")
xsT = np.array(outputT.x)
ysT = np.array(outputT.y)

x_E = np.array([0])
y_E = np.array([0])

x_M = np.array([0])
y_M = np.array([0])

for i in range(0, len(xsRK)):

    x_E_i, y_E_i, z_E_i = x_E_Circular(i * dt * 20)
    x_M_i, y_M_i, z_M_i = x_M_Circular(i * dt * 20)

    x_E = np.append(x_E, [x_E_i])
    y_E = np.append(y_E, [y_E_i])
    x_M = np.append(x_M, [x_M_i])
    y_M = np.append(y_M, [y_M_i])



fig = plt.figure(figsize=(10, 10))
matplotlib.rc('xtick', labelsize=20)
matplotlib.rc('ytick', labelsize=20)
plt.plot(x_M[1:] / 1E8, y_M[1:] / 1E8, color='blue', linewidth=3)
plt.plot(x_E[1:] / 1E8, y_E[1:] / 1E8, color='green', linewidth=3)
plt.plot(xsT / 1E8, ysT / 1E8, color='orange', linewidth=3)
plt.plot(xsRK / 1E8, ysRK / 1E8, color='red', linewidth=3)
plt.xlim(-5.5, 5.5)
plt.ylim(-5.5, 5.5)
plt.xlabel("$x$ position [$10^{8}m$]", fontsize=22)
plt.ylabel("$y$ position [$10^{8}m$]", fontsize=22)

plt.savefig(f'./FINALorbits.png',
                    transparent = False,
                    facecolor = 'white'
                )

plt.close()