#----------------------------------------------------
# SIMULATION FOR THE ROCKET IN THE EARTH-MOON SYSTEM
#----------------------------------------------------


#Imports

from imports import np
from imports import plt
from imports import pd
from functions_evolve import evolve
from functions_earthMoon import E_M_a_Gravity


#Inputs

print("""EARTH-MOON SYSTEM ROCKET SIMULATION

INPUTS (all SI units):

Initial Rocket Coordinates:""")

state = np.zeros((2, 3))
state[0][0] = float(input("x   : "))
state[0][1] = float(input("y   : "))
state[0][2] = float(input("z   : "))
state[1][0] = float(input("v_x : "))
state[1][1] = float(input("v_y : "))
state[1][2] = float(input("v_z : "))

print("""
Simulation Parameters:""")

t = float(input("Start time :"))
dt = float(input("Time step  :"))
T = float(input("End time   :"))
useMethod = input("Step method (E/T/RK4) :")

print("""
Other:""")

useFile = input("Output file name (.csv):")


#Running Simulation

print("""
RUNNING SIMULATION...""")

evolve(state, t, dt, T, 0, E_M_a_Gravity, useMethod, useFile)

print("COMPLETE")


#Plotting

output = pd.read_csv(useFile)
xs = np.array(output.x)
ys = np.array(output.y)

plt.plot(xs, ys, color='red')


from functions_earthMoon import x_E_Circular, x_M_Circular

x_E = np.array([0])
y_E = np.array([0])

x_M = np.array([0])
y_M = np.array([0])

for i in range(0, len(xs)):
    x_E_i, y_E_i, z_E_i = x_E_Circular(i * dt * 50)
    x_M_i, y_M_i, z_M_i = x_M_Circular(i * dt * 50)

    x_E = np.append(x_E, [x_E_i])
    y_E = np.append(y_E, [y_E_i])
    x_M = np.append(x_M, [x_M_i])
    y_M = np.append(y_M, [y_M_i])

plt.plot(x_M[1:], y_M[1:], color='blue')
plt.plot(x_E[1:], y_E[1:], color='green')

plt.show()