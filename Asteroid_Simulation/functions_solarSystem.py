#-----------------------------------------------
# Positions of planetary bodies at a given time
#-----------------------------------------------

# Description:
# The NASA SSD API should be queried to get the positions of objects at all times throughout one orbit
# These stored in program as an array for the "true" positions of the planets unaffected by the asteroids' gravity
# Functions specifying which "timestepNum" is needed will be used to return to the simulation the positions on planets
# "timestep" values allow for integer numbers of the lowest timestep (queried from NASA SSD) to be used


# Imports
from imports import np
from functions_gravity import a_Gravity


# Constants

G = 6.6726E-11 #Gravitational Constant [m3kg-1s-2], project booklet

#Semi-major axes
a_M = 227.956E9 #Mars [m], https://www.smartconversion.com/factsheet/solar-system-semimajor-axis-radius-of-planets
a_J = 778.57E9 #Jupiter [m], https://radiojove.gsfc.nasa.gov/education/jupiter/basics/jfacts.htm

#Masses
m_Sol = 1989100E24 #Sun [kg], https://radiojove.gsfc.nasa.gov/education/sun/basics/material/sunfacts.htm
m_M = 6.4171E23 #Mars [kg], https://en.wikipedia.org/wiki/Mars
m_J = 1898.6E24 #Jupiter [kg], https://radiojove.gsfc.nasa.gov/education/jupiter/basics/jfacts.htm

#Orbital Periods
T_M = 2 * np.pi * ((a_M ** 3) / (G * m_Sol)) ** (0.5)
T_J = 2 * np.pi * ((a_J ** 3) / (G * m_Sol)) ** (0.5)


# Functions

#Positions of bodies

def x_E(timestepNum, timestep): #Less Important
    return ()

def x_M(timestepNum, timestep): #MAIN PROGRAM NEEDS TO KNOW HOW ANY STEPS FOR EACH PLANET AND WHEN IT GETS TO MAXIMUM, LOOP BACK TO 1
    return ()

def x_J(timestepNum, timestep):
    return ()

def x_S(timestepNum, timestep): #Less Important
    return ()

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

def x_Sol(timestepNum, timestep):
    return np.array([0, 0, 0])

#Gravity functions

def Sol_M_J_a_Gravity(stateParticular, N, dt): #Acceleration due to gravity of asteroid at stateParticular due to Sun and Jupiter system
    #N is an array where the first element is the timestep number for Mars and the second is for Jupiter
    masses = np.array([m_Sol, m_M, m_J])
    states = np.array([[[0, 0, 0], [0, 0, 0]], [tuple(x_M_Circular(N[0], dt)), [0, 0, 0]], [tuple(x_J_Circular(N[1], dt)), [0, 0, 0]]]) #Set velocities to zero because these are redundant in the calculation, force of gravity independent of velocities
    return a_Gravity(masses, states, stateParticular)

def Sol_J_a_Gravity(stateParticular, N, dt): #Acceleration due to gravity of asteroid at stateParticular due to Sun and Jupiter system
    masses = np.array([m_Sol, m_J])
    states = np.array([[[0, 0, 0], [0, 0, 0]], [tuple(x_J_Circular(N, dt)), [0, 0, 0]]]) #Set velocities to zero because these are redundant in the calculation, force of gravity independent of velocities
    return a_Gravity(masses, states, stateParticular)

def Sol_a_Gravity(stateParticular, N, dt): #Acceleration due to gravity of asteroid due to only the Sun (for testing purposes)
    masses = np.array([m_Sol])
    states = np.array([[[0, 0, 0], [0, 0, 0]]]) #Set velocities to zero because these are redundant in the calculation, force of gravity independent of velocities
    return a_Gravity(masses, states, stateParticular)