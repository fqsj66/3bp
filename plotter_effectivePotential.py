import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# ---------------------------------------------
# Physical constants (SI units)
# ---------------------------------------------
G = 6.6726E-11                # gravitational constant
M_earth = 5.9742E24           # kg
M_moon  = 7.35E22             # kg
d = 3844E5                    # Earth–Moon distance (m)

# Rotating frame angular velocity (circular orbit)
omega = np.sqrt(G * (M_earth + M_moon) / d**3)

# ---------------------------------------------
# Coordinate grid
# ---------------------------------------------
# Define a coordinate system where Earth is at x=0, Moon at x=d
xmin, xmax = -500000000, 500000000
ymin, ymax = -500000000, 500000000

N = 1000   # grid resolution

x = np.linspace(xmin, xmax, N)
y = np.linspace(ymin, ymax, N)
X, Y = np.meshgrid(x, y)

# Distances to Earth and Moon
r_earth = np.sqrt((X - 0)**2 + Y**2)
r_moon  = np.sqrt((X - d)**2 + Y**2)

# ---------------------------------------------
# Effective potential (Roche potential)
# Φ = -GM1/r1 - GM2/r2 - ½ ω² r²  (in rotating frame)
# ---------------------------------------------
Phi = -G*M_earth/r_earth - G*M_moon/r_moon \
      - 0.5 * omega**2 * ( (X - (M_moon/(M_earth+M_moon))*d )**2 + Y**2 )

# Mask singularities (near Earth & Moon)
#Phi = np.where(r_earth < 1, np.nan, Phi)
#Phi = np.where(r_moon  < 1, np.nan, Phi)

# ---------------------------------------------
# Plotting
# ---------------------------------------------
plt.figure(figsize=(15, 12))

vmin = np.nanpercentile(Phi, 1)
vmax = np.nanpercentile(Phi, 99)
levels = np.linspace(vmin, vmax, 150)

contour = plt.contourf(X / 1E8, Y / 1E8, Phi, levels=levels, cmap='plasma')
plt.colorbar(contour, label='Effective potential [$10^{6}$J/kg]')


line_levels = np.linspace(vmin, vmax, 60)   # adjust number for desired spacing
contour_lines = plt.contour(
    X / 1E8, Y / 1E8, Phi,
    levels=line_levels,
    colors='black',
    linewidths=0.6,
    #linestyle='solid'
    alpha=0.7
)
#plt.clabel(contour_lines, inline=True, fontsize=6, fmt="%.2e")

# Plot Earth and Moon
plt.plot(0, 0, 'o', color='black', markersize=31)
plt.plot(0, 0, 'x', color='green', markersize=10)
plt.plot(d / 1E8, 0, 'x', color='blue', markersize=10)

plt.plot(0.848 * d / 1E8, 0, '+', color='red', markersize=10)
plt.plot(1.167 * d / 1E8, 0, '+', color='red', markersize=10)
plt.plot(-0.994 * d / 1E8, 0, '+', color='red', markersize=10)
plt.plot(0.5 * d / 1E8, 0.866 * d / 1E8, '+', color='red', markersize=10)
plt.plot(0.5 * d / 1E8, -0.866 * d / 1E8, '+', color='red', markersize=10)

matplotlib.rc('xtick', labelsize=30)
matplotlib.rc('ytick', labelsize=20)

plt.xlabel("$x$ position [$10^{8}m$]", fontsize=10)
plt.ylabel("$y$ position [$10^{8}m$]", fontsize=10)
#plt.legend()
plt.tight_layout()
plt.show()