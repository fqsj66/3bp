#--------------------------------------------------------------------------------
#Final program for The Restricted Three Body Problem examining L2 Point in Earth-Moon system
#--------------------------------------------------------------------------------


print("""
=====================
Restricted 3BP for L2
=====================

Importing Packages...""")


#Imports


import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt
import csv
import imageio
import os
import time


#Constants


print("Setting Parameters...")


G = 6.6726E-11 #Gravitational Constant [m3kg-1s-2], project booklet
d_EM = 3844E5 #Earth to moon distance [m], project booklet
m_E = 5.9742E24 #Mass of Earth [kg], project booklet
m_M = 7.35E22 #Mass of Moon [kg], project booklet

r_E_circular = (d_EM * m_M) / (m_E + m_M) #Radius of Earth's orbit MAY NEED TO REWRITE IN TERMS OF MASS FRACTIONS TO MAKE MORE NUMERICALLY ROBUST
r_M_circular = (d_EM * m_E) / (m_E + m_M) #Radius of Moon's orbit

T_EM = np.sqrt(4 * np.pi ** 2 * d_EM ** 3 / (G * (m_M + m_E))) #Time period of orbit, worked out using K3L


#Functions


print("Interpreting functions...")


#Functions for the coordinates of Earth and Moon relative to centre of mass (and fixed stars)


def x_E_Circular(t):
    #Earth starts at y=0, x>0 for t=0
    angle = ((2 * np.pi * t) / T_EM)
    x = r_E_circular * np.cos(angle)
    y = r_E_circular * np.sin(angle)
    return np.array([x, y, 0]) #In x-y plane only, zero z coordinate added for function compatability

def x_M_Circular(t):
    #Moon starts at y=0, x<0 for t=0
    angle = ((2 * np.pi * t) / T_EM)
    x = -1 * r_M_circular * np.cos(angle)
    y = -1 * r_M_circular * np.sin(angle)
    return np.array([x, y, 0])


#Functions for Gravity Calculations


def d(state1, state2): #Calculates distance between two bodies' state vectors
    return np.hypot(np.hypot(state2[0][0] - state1[0][0], state2[0][1] - state1[0][1]), state2[0][2] - state1[0][2])

def a_Gravity_Component(mass, state, stateParticular): #Gives acceleration contribution due to a body with mass and state, acting on stateParticular
    distanceBetweenBodies = d(state, stateParticular)
    distanceReciprocalCubed = 1 / (distanceBetweenBodies * distanceBetweenBodies * distanceBetweenBodies)
    return -1 * G * mass * (stateParticular[0] - state[0]) * distanceReciprocalCubed #Outputs an array with the differing components of acceleration

def E_M_a_Gravity(stateParticular, t):
    gravityM = a_Gravity_Component(m_M, np.array([x_M_Circular(t), [0, 0, 0]]), stateParticular)
    gravityE = a_Gravity_Component(m_E, np.array([x_E_Circular(t), [0, 0, 0]]), stateParticular)
    return gravityM + gravityE


#Functions for Movement of Massless Particles


def step_Taylor(state, t, dt, f_a): #t gives the time at the start of the step, it is assumed f_a does not vary in time throughout the step
    f_a_values = f_a(state, t)
    return state + dt * np.array([state[1], f_a_values]) + (dt ** 2 / 2) * np.array([f_a_values, [0, 0, 0]])

def step_RK4(state, t, dt, f_a): #parameters as above
    a0 = f_a(state, t)

    x1 = state[0] + (dt / 2) * state[1]
    v1 = state[1] + (dt / 2) * a0
    a1 = f_a(np.array([x1, v1]), t)

    x2 = state[0] + (dt / 2) * v1
    v2 = state[1] + (dt / 2) * a1
    a2 = f_a(np.array([x2, v2]), t)

    x3 = state[0] + dt * v2
    v3 = state[1] + dt * a2
    a3 = f_a(np.array([x3, v3]), t)

    xNew = state[0] + (dt / 6) * (state[1] + 2 * v1 + 2 * v2 + v3)
    vNew = state[1] + (dt / 6) * (a0 + 2 * a1 + 2 * a2 + a3)

    return np.array([(xNew), (vNew)])

def evolve(state, t0, dt, t1, f_a, numSaves, useMethod, useFileName): #Evolves path of rocket, saving results in csv file
    
    N = int(np.round((t1 - t0) / (dt * numSaves))) + 1 #Number of groups of numSaves timesteps needed, added one in case rounds down to zero

    directoryRocket = "{}/rocket.csv".format(useFileName) #Setting up file for saving positions
    fileRocket = open(directoryRocket, 'w+', newline='')
    writerRocket = csv.writer(fileRocket)
    writerRocket.writerow(["x", "y", "z"])

    if useMethod == "T": #Taylor steps

        for i in range(0, N):
            for j in range(0, numSaves):
                state = step_Taylor(state, (t0 + numSaves * i + j), dt, f_a)
            writerRocket.writerow(state[0])

    else: #RK4 steps

        for i in range(0, N):
            for j in range(0, numSaves):
                state = step_RK4(state, (t0 + numSaves * i + j), dt, f_a)
            writerRocket.writerow(state[0])
    
    fileRocket.close()


#Functions for Simulating Orbit in L2 Point

def evolve_L2(dt, t1, useMethod, d_initial, useFileName): #d_initial is initial distance of rocket from the moon
    
    x_initial = - d_initial - r_M_circular
    v_initial = (x_initial * 2 * np.pi) / (T_EM)
    state = np.array([[x_initial, 0, 0], [0, v_initial, 0]])

    print("START: {}".format(time.asctime(time.localtime())))
    evolve(state, 0, dt, t1, E_M_a_Gravity, 50, useMethod, useFileName)
    print("FINISH: {}".format(time.asctime(time.localtime())))


#Core Code


d_approx = (3844E5 * (7.35E22 / (3 * 5.9742E24)) ** (1 / 3))
d_start = d_approx - 1E5
d_end = d_approx + 1E5

numTrials = 1
dt = 1
t1 = T_EM
useMethod = "rk4"
useFileNameMaster = "SEARCH-TEST"

os.makedirs("{}".format(useFileNameMaster))

ds = np.linspace(d_start, d_end, num=numTrials)

for d_initial in ds:
    os.makedirs("{}/{}".format(useFileNameMaster, d_initial))
    evolve_L2(dt, t1, useMethod, d_initial, "{}/{}".format(useFileNameMaster, d_initial))

