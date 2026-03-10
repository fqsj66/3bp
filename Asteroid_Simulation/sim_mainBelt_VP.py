#---------------------------------------
# COMPLETE SIMULATION IN ONE EXECUTABLE
#      Vectorised and Parallelised
#---------------------------------------



#---------------------------------------
#                Imports
#---------------------------------------

import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt
import csv
import os
import time
import random as rnd
import multiprocessing as mp


#---------------------------------------
#               Constants
#---------------------------------------

#Physics constants
G = 6.6726E-11 #Gravitational Constant [m3kg-1s-2], project booklet
AU = 1.496E11

#Semi-major axes
a_M = 227.956E9 #Mars [m], https://www.smartconversion.com/factsheet/solar-system-semimajor-axis-radius-of-planets
a_J = 778.57E9 #Jupiter [m], https://radiojove.gsfc.nasa.gov/education/jupiter/basics/jfacts.htm

#Masses
m_Sol = 1989100E24 #Sun [kg], https://radiojove.gsfc.nasa.gov/education/sun/basics/material/sunfacts.htm
m_M = 6.4171E23 #Mars [kg], https://en.wikipedia.org/wiki/Mars
m_J = 1898.6E24 #Jupiter [kg], https://radiojove.gsfc.nasa.gov/education/jupiter/basics/jfacts.htm

#Orbital Periods
T_M = 2 * np.pi * ((a_M ** 3) / (G * m_Sol)) ** (0.5) #Using K3L
T_J = 2 * np.pi * ((a_J ** 3) / (G * m_Sol)) ** (0.5)

#Asteroid Belt Parameters
startR = 2.1 * AU #Start orbital radius of asteroids
endR = 2.9 * AU #End orbital radius of asteroids
eMax = 0.4 #Maximum eccentricity of asteroids
asteroidNum = 1000 #Number of asteroids (obvs.)

#Simulation Parameters
timestepNum = 0 #Save timestepNum s for each planet. Need to keep running count of how many revolutions Jupiter has done so that can tell how long the simulation is running for in in-simulation time
timestep = T_J / 1000 #Duration of each timestep
T = T_J * 1000 #In-universe simulation duration
startingDirectory = "SimVectorisedWideMulti" #File dedicated to simulation
newSim = True #True if this is the first time simulation with these parameters is being run


#---------------------------------------
#          Functions: Gravity
#---------------------------------------

def d_V(xs1, ys1, zs1, x2, y2, z2): #First 3 arguments are arrays. Last 3 are numbers for planet
    return np.sqrt((x2 - xs1) ** 2 + (y2 - ys1) ** 2 + (z2 - zs1) ** 2)

def a_Gravity_Component_V(mass, xs, ys, zs, x2, y2, z2):
    distancesBetweenBodies = d_V(xs, ys, zs, x2, y2, z2)
    distancesReciprocalCubed = 1 / (distancesBetweenBodies * distancesBetweenBodies * distancesBetweenBodies)
    ax = -1 * G * mass * (xs - x2) * distancesReciprocalCubed
    ay = -1 * G * mass * (ys - y2) * distancesReciprocalCubed
    az = -1 * G * mass * (zs - z2) * distancesReciprocalCubed
    return ax, ay, az

def a_Gravity_V(masses, xs, ys, zs, xs2, ys2, zs2): #Arrays for all the arguments
    ax = 0
    ay = 0
    az = 0
    for i in range(0, len(masses)): #Only 3 loops for main simulations so computationally justifiable
        axNew, ayNew, azNew = a_Gravity_Component_V(masses[i], xs, ys, zs, xs2[i], ys2[i], zs2[i])
        ax += axNew
        ay += ayNew
        az += azNew
    return ax, ay, az

def ae_from_rv(state, m): #m should be total mass of two bodies, but assume that mass of sun >> asteroid mass so should just be sun's mass (for calculating mu)
    vSqr = np.sum(state[1] ** 2)
    v = np.sqrt(vSqr)
    r = np.sqrt(np.sum(state[0] ** 2))
    a = np.abs((vSqr / (G * m) - 2 / r) ** -1)
    e = np.sqrt(1 + 2 / ((G * m ) ** 2) * np.sum(np.cross(state[0], state[1]) ** 2) * (vSqr / 2 - G * m / r))
    return a, e

def rv_from_ae(a, e, m): #Gives initial state vector at periapse given semi-major axis, eccentricity and mass sum (same approx. as below)
    return np.array([[a * (1-e), 0, 0], [0, np.sqrt(G * m * (1 + e) / (a * (1-e))), 0]])


#---------------------------------------
#         Functions: Asteroids
#---------------------------------------

def asteroidPopulation_line_elliptical_V(Num, eMax):
    population = np.zeros((Num, 2, 3))
    eccentricity = np.zeros(Num)
    semimajoraxis = np.zeros(Num)
    xs = np.zeros(Num)
    ys = np.zeros(Num)
    zs = np.zeros(Num)
    vxs = np.zeros(Num)
    vys = np.zeros(Num)
    vzs = np.zeros(Num)
    for i in range(0, Num): #This is not efficient but only runs once at the very start of each simulatiom
        eccentricity[i] = rnd.uniform(0, eMax)
        semimajoraxis[i] = ((endR - startR) * i / Num) + startR
        population[i] = rv_from_ae(((endR - startR) * i / Num) + startR, eccentricity[i], m_Sol)
        xs[i] = population[i][0][0]
        ys[i] = population[i][0][1]
        zs[i] = population[i][0][2]
        vxs[i] = population[i][1][0]
        vys[i] = population[i][1][1]
        vzs[i] = population[i][1][2]
    return xs, ys, zs, vxs, vys, vzs


#---------------------------------------
#        Functions: Solar System
#---------------------------------------

def x_M_Circular(timestepNum, timestep):
    t = timestepNum * timestep
    angle = ((2 * np.pi * t) / T_M)
    x = a_M * np.cos(angle)
    y = a_M * np.sin(angle)
    return np.array([x, y, 0])

def x_J_Circular(timestepNum, timestep):
    t = timestepNum * timestep
    angle = ((2 * np.pi * t) / T_J)
    x = a_J * np.cos(angle)
    y = a_J * np.sin(angle)
    return np.array([x, y, 0])

def Sol_M_J_a_Gravity_V(xs, ys, zs, N, dt): #N is an array where the first element is the timestep number for Mars and the second is for Jupiter
    masses = np.array([m_Sol, m_M, m_J])
    M_coords = x_M_Circular(N[0], dt)
    J_coords = x_J_Circular(N[0], dt)
    xs2 = np.array([0, M_coords[0], J_coords[0]])
    ys2 = np.array([0, M_coords[1], J_coords[1]])
    zs2 = np.array([0, 0, 0])
    return a_Gravity_V(masses, xs, ys, zs, xs2, ys2, zs2)


#---------------------------------------
#           Functions: Evolve
#---------------------------------------

def step_RK4_V(xs0, ys0, zs0, vxs0, vys0, vzs0, N, dt, f_a):
    ax0, ay0, az0 = f_a(xs0, ys0, zs0, N, dt)
    xs1 = xs0 + (dt / 2) * vxs0
    ys1 = ys0 + (dt / 2) * vys0
    zs1 = zs0 + (dt / 2) * vzs0
    vxs1 = vxs0 + (dt / 2) * ax0
    vys1 = vys0 + (dt / 2) * ay0
    vzs1 = vzs0 + (dt / 2) * az0
    ax1, ay1, az1 = f_a(xs1, ys1, zs1, N, dt)
    xs2 = xs0 + (dt / 2) * vxs1
    ys2 = ys0 + (dt / 2) * vys1
    zs2 = zs0 + (dt / 2) * vzs1
    vxs2 = vxs0 + (dt / 2) * ax1
    vys2 = vys0 + (dt / 2) * ay1
    vzs2 = vzs0 + (dt / 2) * az1
    ax2, ay2, az2 = f_a(xs2, ys2, zs2, N, dt)
    xs3 = xs0 + dt * vxs2
    ys3 = ys0 + dt * vys2
    zs3 = zs0 + dt * vzs2
    vxs3 = vxs0 + dt * ax2
    vys3 = vys0 + dt * ay2
    vzs3 = vzs0 + dt * az2
    ax3, ay3, az3 = f_a(xs3, ys3, zs3, N, dt)
    xsNew = xs0 + (dt / 6) * (vxs0 + 2 * vxs1 + 2 * vxs2 + vxs3)
    ysNew = ys0 + (dt / 6) * (vys0 + 2 * vys1 + 2 * vys2 + vys3)
    zsNew = zs0 + (dt / 6) * (vzs0 + 2 * vzs1 + 2 * vzs2 + vzs3)
    vxsNew = vxs0 + (dt / 6) * (ax0 + 2 * ax1 + 2 * ax2 + ax3)
    vysNew = vys0 + (dt / 6) * (ay0 + 2 * ay1 + 2 * ay2 + ay3)
    vzsNew = vzs0 + (dt / 6) * (az0 + 2 * az1 + 2 * az2 + az3)
    return xsNew, ysNew, zsNew, vxsNew, vysNew, vzsNew

def evolve_V_P(xs, ys, zs, vxs, vys, vzs, N_start, dt, T, f_a):
    N_end = int(np.round(T / dt)) + 1 #Number of timesteps needed
    print("Evolving Asteroids with N = {}".format(N_end))
    for j in range(0, N_end):
        xs, ys, zs, vxs, vys, vzs = step_RK4_V(xs, ys, zs, vxs, vys, vzs, N_start + j, dt, f_a)
    return xs, ys, zs, vxs, vys, vzs

def evolve_V(xs, ys, zs, vxs, vys, vzs, N_start, dt, T, f_a): #Vectorised version of evolve for RK4_V, self contained
    N_end = int(np.round(T / dt)) + 1 #Number of timesteps needed
    print("Evolving Asteroids with N = {}".format(N_end))
    for j in range(0, N_end):
        xs, ys, zs, vxs, vys, vzs = step_RK4_V(xs, ys, zs, vxs, vys, vzs, N_start + j, dt, f_a)
    return xs, ys, zs, vxs, vys, vzs

def worker(xs, ys, zs, vxs, vys, vzs, N_start, dt, T, f_a, q): #Worker for multiprocessing
    xs, ys, zs, vxs, vys, vzs = evolve_V_P(xs, ys, zs, vxs, vys, vzs, N_start, dt, T, f_a)
    q.put(np.array([xs, ys, zs, vxs, vys, vzs]))

#---------------------------------------
#               SIMULATION
#---------------------------------------

while __name__ == "__main__":

    #Deciding whether to start new simulation of not
    if newSim == False:

        files = os.listdir('Simulations\{}'.format(startingDirectory))
        paths = [os.path.join('Simulations\{}'.format(startingDirectory), basename) for basename in files]

        i_latest = 0
        for i in range(0, len(paths)): #Finding most recently modified file which is the current state of the simulation
            if float(os.path.getmtime(paths[i])) >= float(os.path.getmtime(paths[i_latest])):
                i_latest = i

        fileStart = pd.read_csv(paths[i_latest]) #Loading data from most recent output file
        
        N_M = (np.array(fileStart.x)[0])
        N_J = (np.array(fileStart.y)[0])
        N_start = np.array([N_M, N_J])

        xs = np.array(fileStart.x)[1:]
        ys = np.array(fileStart.y)[1:]
        zs = np.array(fileStart.z)[1:]
        vxs = np.array(fileStart.v_x)[1:]
        vys = np.array(fileStart.v_y)[1:]
        vzs = np.array(fileStart.v_z)[1:]

    else:

        #Set up sim file structure
        os.makedirs('Simulations\{}'.format(startingDirectory))
        paramsFile = open('Simulations\{}\params.csv'.format(startingDirectory), 'w+', newline='') #Creates csv file called the current time which is used to store (paused) results
        paramsWriter = csv.writer(paramsFile)
        paramsWriter.writerow(["timestep", "T", "asteroidNum", "eMax"])
        paramsWriter.writerow([timestep, T, asteroidNum, eMax])
        paramsFile.close()

        N_start = np.array([0, 0])
        xs, ys, zs, vxs, vys, vzs = asteroidPopulation_line_elliptical_V(asteroidNum, eMax)


    print("START: {}".format(time.asctime(time.localtime())))

    #RUNNING THE SIMULATION
    #mp.set_start_method('spawn')
    if __name__ == "__main__": #Ensures multiprocessing begins from main program and is worthwhile
        print("STARTING PROCESSES")
        q = mp.Queue()
        print("creating objects")
        p1 = mp.Process(target=worker, args=(xs[:500], ys[:500], zs[:500], vxs[:500], vys[:500], vzs[:500], N_start, timestep, T, Sol_M_J_a_Gravity_V, q))
        p2 = mp.Process(target=worker, args=(xs[500:], ys[500:], zs[500:], vxs[500:], vys[500:], vzs[500:], N_start, timestep, T, Sol_M_J_a_Gravity_V, q))
        print("created objects")
        p1.start()
        p2.start()
        print("started objects")
        p1.join()
        p2.join()
        print("finished objects")
        result1 = q.get()
        result2 = q.get()
        xs = np.append(result1[0], result2[0])
        ys = np.append(result1[1], result2[1])
        zs = np.append(result1[2], result2[2])
        vxs = np.append(result1[3], result2[3])
        vys = np.append(result1[4], result2[4])
        vzs = np.append(result1[5], result2[5])
    else:
        print("Error with Parallelisation")
    #xs, ys, zs, vxs, vys, vzs = evolve_V(xs, ys, zs, vxs, vys, vzs, N_start, timestep, T, Sol_M_J_a_Gravity_V)

    print("END: {}".format(time.asctime(time.localtime())))


    #Saving file at the end of the sim

    print("SAVING...")

    resultsFile = open('Simulations\{}\{}.csv'.format(startingDirectory, time.time()), 'w+', newline='') #Creates csv file called the current time which is used to store (paused) results
    resultsWriter = csv.writer(resultsFile)
    resultsWriter.writerow(["x", "y", "z", "v_x", "v_y", "v_z"])
    N_start[0] + int(np.round(T / timestep)) + 1
    resultsWriter.writerow([N_start[0] + int(np.round(T / timestep)) + 1, N_start[1] + int(np.round(T / timestep)) + 1, 0, 0, 0, 0])

    for i in range(0, len(xs)): #Not efficient but only happens once at the end of each run
        resultsWriter.writerow([xs[i], ys[i], zs[i], vxs[i], vys[i], vzs[i]])

    resultsFile.close()

    time.sleep(200)

    if newSim == True:
        newSim = False