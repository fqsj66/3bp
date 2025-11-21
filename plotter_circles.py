#Fast plot gogogo

from imports import np
from imports import plt
from functions_earthMoon import x_M_Circular, x_E_Circular, T_EM

x_E = np.array([0])
y_E = np.array([0])

x_M = np.array([0])
y_M = np.array([0])

x_R = np.array([0])
y_R = np.array([0])

for t in range(0, int(2628500 / 20)):
    x_E_i, y_E_i, z_E_i = x_E_Circular(t * 20)
    x_M_i, y_M_i, z_M_i = x_M_Circular(t * 20)

    x_E = np.append(x_E, [x_E_i])
    y_E = np.append(y_E, [y_E_i])
    x_M = np.append(x_M, [x_M_i])
    y_M = np.append(y_M, [y_M_i])

    x_R = np.append(x_R, (445803407.2 * np.sin((2 * np.pi * t * 20) / T_EM)))
    y_R = np.append(y_R, (445803407.2 * np.cos((2 * np.pi * t * 20) / T_EM)))

fig = plt.figure(figsize=(6, 6))

plt.plot(x_E[1:], y_E[1:], color="green")
plt.plot(x_M[1:], y_M[1:], color="blue")
plt.plot(x_R[1:], y_R[1:], color="red")

plt.xlim(-500000000, 500000000)
plt.ylim(-500000000, 500000000)
plt.show()