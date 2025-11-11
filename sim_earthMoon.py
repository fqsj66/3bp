#----------------------------------------------------
# SIMULATION FOR THE ROCKET IN THE EARTH-MOON SYSTEM
#----------------------------------------------------


#Imports

from imports import imageio
from imports import np
from imports import plt
from imports import pd
from imports import os
from imports import time
from functions_evolve import evolve
from functions_earthMoon import E_M_a_Gravity


#Inputs

print("""
-----------------------------------
EARTH-MOON SYSTEM ROCKET SIMULATION
-----------------------------------

------
SETUP:
------

Initial Rocket Coordinates [SI]:""")

state = np.zeros((2, 3))
state[0][0] = float(input("x   : "))
state[0][1] = float(input("y   : "))
state[0][2] = float(input("z   : "))
state[1][0] = float(input("v_x : "))
state[1][1] = float(input("v_y : "))
state[1][2] = float(input("v_z : "))

print("""
Simulation Parameters [SI]:""")

t = float(input("Start time :"))
dt = float(input("Time step  :"))
T = float(input("End time   :"))
useMethod = input("Step method (E/T/RK4) :")

print("""
Simulation Name:""")

useFileName = input("Output file name :")
#useFile = "{}.csv".format(useFileName)

os.makedirs("{}".format(useFileName)) #Create a folder to house all the data
os.makedirs("{}/frames".format(useFileName))

#LATER SHOULD CREATE A TXT FILE TO HOUSE THE METADATA FOR THE RUN PARAMETERS


#Running Simulation

print("""
-------------------
RUNNING SIMULATION:
-------------------
""")

print("START: {}".format(time.localtime()))

evolve(state, t, dt, T, 0, E_M_a_Gravity, useMethod, useFileName)

print("COMPLETE: {}".format(time.localtime()))

print("""
----------------
GENERATING PLOT:
----------------
""")


#Plotting

output = pd.read_csv("{}/rocket.csv".format(useFileName))
xs = np.array(output.x)
ys = np.array(output.y)

from functions_earthMoon import x_E_Circular, x_M_Circular

x_E = np.array([0])
y_E = np.array([0])

x_M = np.array([0])
y_M = np.array([0])

for i in range(0, len(xs)):

    x_E_i, y_E_i, z_E_i = x_E_Circular(i * dt * 20)
    x_M_i, y_M_i, z_M_i = x_M_Circular(i * dt * 20)

    x_E = np.append(x_E, [x_E_i])
    y_E = np.append(y_E, [y_E_i])
    x_M = np.append(x_M, [x_M_i])
    y_M = np.append(y_M, [y_M_i])

plt.plot(x_M[1:], y_M[1:], color='blue')
plt.plot(x_E[1:], y_E[1:], color='green')
plt.plot(xs, ys, color='red')

plt.show()
plt.close()


print("""
--------------------
GENERATING ANIMATION
--------------------
""")


#Creating a gif

x_E = np.array([0])
y_E = np.array([0])

x_M = np.array([0])
y_M = np.array([0])

for frame in range(0, len(xs)):
    fig = plt.figure(figsize=(6, 6))

    x_E_i, y_E_i, z_E_i = x_E_Circular(frame * dt * 20)
    x_M_i, y_M_i, z_M_i = x_M_Circular(frame * dt * 20)

    x_E = np.append(x_E, [x_E_i])
    y_E = np.append(y_E, [y_E_i])
    x_M = np.append(x_M, [x_M_i])
    y_M = np.append(y_M, [y_M_i])

    plt.plot(xs[:(frame)], ys[:(frame)], color='red')
    plt.plot(x_M[1:], y_M[1:], color='blue')
    plt.plot(x_E[1:], y_E[1:], color='green')
    

    plt.xlim(-500000000, 500000000)
    plt.ylim(-500000000, 500000000)
    plt.title("t={}".format(frame * dt * 20))

    plt.savefig(f'./{useFileName}/frames/{frame}.png', 
                transparent = False,  
                facecolor = 'white'
               )

    plt.close()

frames = []
for frameNum in range(0, len(xs)):
    image = imageio.v2.imread(f'./{useFileName}/frames/{frameNum}.png')
    frames.append(image)
imageio.mimsave('./{}/animation.gif'.format(useFileName), frames, fps = 20)



#for frame in range(0, len(xs)):
#    fig = plt.figure(figsize=(6, 6))

#    x_E_i, y_E_i, z_E_i = x_E_Circular(i * dt * 20)
#    x_M_i, y_M_i, z_M_i = x_M_Circular(i * dt * 20)

#    x_E = np.append(x_E, [x_E_i])
#    y_E = np.append(y_E, [y_E_i])
#    x_M = np.append(x_M, [x_M_i])
#    y_M = np.append(y_M, [y_M_i])

print("""EXIT SIMULATION""")