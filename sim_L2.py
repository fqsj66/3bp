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
from functions_earthMoon import E_M_a_Gravity, r_M_circular, T_EM, x_E_Circular, x_M_Circular
from functions_gravity import d


#Function for running the simulation of a rocket for initial state

def L2Run(state, dt, T, useMethod, d_initial, useFileName):
    
    t = 0

    os.makedirs("{}".format(useFileName)) #Create a folder to house all the data


    #Running Simulation

    print("START: {}".format(time.asctime(time.localtime())))

    evolve(state, t, dt, T, 0, E_M_a_Gravity, useMethod, useFileName)

    print("COMPLETE: {}".format(time.asctime(time.localtime())))


    #Plotting orbits

    output = pd.read_csv("{}/rocket.csv".format(useFileName))
    xs = np.array(output.x)
    ys = np.array(output.y)

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

    plt.savefig(f'./{useFileName}/orbits.png',
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


    #Calculating mean and standard deviation

    dMean = np.sum(ds[1:]) / len(ds[1:])
    dSd = np.sqrt(  (1 / (len(ds[1:]) - 1))  *  (np.sum(ds[1:] ** 2))  )

    return (dSd / dMean)

    #return np.array([ds[1], ds[-1]]) #returns start and end values of rocket-moon distance


#Main Method

print("""
--------------------------------
EARTH-MOON SYSTEM L2 SIMULATION
--------------------------------

SETUP:
""")

state = np.zeros((2, 3))
#state[0][0] = -445803407.2 #starting point from project booklet
state[0][1] = 0
state[0][2] = 0
state[1][0] = 0
#state[1][1] = state[0][0] * 2 * np.pi / (T_EM) #Circular velocity required for this radius
state[1][2] = 0

#startingDR = int(input("Starting Point   :")) * -1
#finishingDR = int(input("Finishing Point  :")) * -1
#trialsDR = int(input("Num of Runs      :"))
#dt = int(input("Timestep Size    :"))S
#useMethod = input("Evolution Method :")

startingDR = -400000000
finishingDR = -500000000
trialsDR = 20
dt = 20
T = T_EM
useMethod = "rk4"
useFileNameMaster = "SEARCH/"

trials = np.linspace(startingDR, finishingDR, num=trialsDR)

dataPrecision = np.array([0])

os.makedirs("{}".format(useFileNameMaster))#File to house data files

for trial in trials:
    state[0][0] = trial
    state[1][1] = state[0][0] * 2 * np.pi / (T_EM)
    dataPrecision = np.append(dataPrecision, L2Run(state, dt, T, useMethod, trial, "{}{}".format(useFileNameMaster, trial)))

plt.plot(trials, dataPrecision[1:])
plt.show()



