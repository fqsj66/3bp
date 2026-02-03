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


# Constants

G = 6.6726E-11 #Gravitational Constant [m3kg-1s-2], project booklet

#Semi-major axes
a_M = 227.956E9 #Mars [m], https://www.smartconversion.com/factsheet/solar-system-semimajor-axis-radius-of-planets
a_J = 778.57E9 #Jupiter [m], https://radiojove.gsfc.nasa.gov/education/jupiter/basics/jfacts.htm

#Masses
m_Su = 1989100E24 #Sun [kg], https://radiojove.gsfc.nasa.gov/education/sun/basics/material/sunfacts.htm

#Orbital Periods
T_M = 2 * np.pi * ((a_M) / (G * m_Su)) ** (0.5)
T_J = 2 * np.pi * ((a_J) / (G * m_Su)) ** (0.5)


# Functions

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