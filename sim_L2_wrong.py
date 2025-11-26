#----------------------------------------------------------
# SIMULATION FOR THE ROCKET AT L2 IN THE EARTH-MOON SYSTEM
#----------------------------------------------------------


#Imports

from imports import imageio
from imports import np
from imports import plt
from imports import pd
from imports import os
from imports import time
from functions_evolve import evolve
from functions_earthMoon import E_M_a_Gravity, r_M_circular, T_EM
from functions_gravity import d



def L2Run(state, t, dt, T, useMethod, d_initial, useFileName):
    

    os.makedirs("{}".format(useFileName)) #Create a folder to house all the data


    #Running Simulation
    print("""
    -------------------
    RUNNING SIMULATION:
    -------------------
    """)

    print("START: {}".format(time.localtime()))

    evolve(state, t, dt, T, 0, E_M_a_Gravity, useMethod, useFileName)

    print("COMPLETE: {}".format(time.localtime()))


    #Plotting


    print("""
    ----------------
    GENERATING PLOT:
    ----------------
    """)

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

    fig = plt.figure(figsize=(6, 6))
    plt.plot(x_M[1:], y_M[1:], color='blue')
    plt.plot(x_E[1:], y_E[1:], color='green')
    plt.plot(xs, ys, color='red')
    plt.xlim(-500000000, 500000000)
    plt.ylim(-500000000, 500000000)
    plt.title("{}".format(d_initial))

    plt.savefig(f'./{useFileName}/all.png', 
                        transparent = False,  
                        facecolor = 'white'
                    )

    plt.close()


    #Plotting moon to rocket distance

    ds = np.array([0])
    ts = np.array([0])

    for step in range(0, len(xs)):
        ds = np.append(ds, d( [ [xs[step], ys[step], 0] , [0, 0, 0] ] , [ [x_M_Circular(step * dt * 20)[0] , x_M_Circular(step * dt * 20)[1], 0] , [0, 0, 0]]) )
        ts = np.append(ts, [step * dt * 20])
    fig = plt.figure(figsize=(6, 6))

    plt.plot(ts[1:], ds[1:]/ (d_initial))
    #plt.plot([0, ts[-1]], [(-1 * (state[0][0] + r_M_circular)), (-1 * (state[0][0] + r_M_circular))], color="black")
    #plt.plot([0, ts[-1]], [0, 0], color="black")
    plt.savefig(f'./{useFileName}/d.png',
                        transparent = False,
                        facecolor = 'white'
                    )

    plt.close()
    
    return np.array([ds[1], ds[-1]]) #returns start and end values of rocket-moon distance

















#Inputs

print("""
--------------------------------
EARTH-MOON SYSTEM L2 SIMULATION
--------------------------------

------
SETUP:
------

Initial Rocket Coordinates [SI]:""")

state = np.zeros((2, 3))
state[0][0] = -445803407.2 #starting point from project booklet
state[0][1] = 0
state[0][2] = 0
state[1][0] = 0
state[1][1] = state[0][0] * 2 * np.pi / (T_EM) #Circular velocity required for this radius
print(state[0][0])
print(state[1][1])
print(r_M_circular)

state[1][2] = 0

print("""
Simulation Parameters [SI]:""")

t = 0 #Start time
dt = float(input("Time step  :"))
T = T_EM #Time period of orbit
useMethod = input("Step method (E/T/RK4) :")

print("""
Simulation Name:""")

nameOfFile = input("Output file name :")

print("""
Number of Simulations:""")

simNum = input("Sim Num :")

perDiff = 0.01 # Percentage difference for changing initial placement of satellite
xIncreased = False
xDecreased = False

for n in range(0, int(simNum)): #Loops for the search
    d_initial =  -1 * state[0][0] - r_M_circular
    d_startEnd = np.zeros(2)
    d_startEnd = L2Run(state, t, 10, 5000, useMethod, d_initial, ("{}_{}_{}".format(nameOfFile, n, str(state[0][0]))))#runs for 1 second timesteps to 200 seconds to see if staellite falls closer to moon or further away
    
    if d_startEnd[0] > d_startEnd[1]:# Changing the L2 numerical value
        xIncreased = True
        state[0][0] = state[0][0] * (1 + perDiff)
    else:
        xDecreased = True
        state[0][0] = state[0][0] * (1 - perDiff)
    state[1][1] = state[0][0] * 2 * np.pi / (T_EM)#

    if (xIncreased == True) and (xDecreased == False):# Halves the percentage difference L2 numerical value is altered by if starts to overshoot target
        xIncreased = False
        xDecreased = False
        #perDiff = perDiff / 2 #changing perecentage difference
    #time.sleep(3)

d_startEnd = L2Run(state, t, dt, T, useMethod, d_initial, ("{}_{}_{}".format(nameOfFile, simNum, str(state[0][0]))))# Final simulation of full orbit
