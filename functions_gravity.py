#-------------------------------------------------------------
# FUNCTIONS FOR THE CALCULATION OF GRAVITATIONAL ACCELERATION
#-------------------------------------------------------------


#Imports

from imports import np


#Constants NEED TO STATE UNITS

G = 6.67430E-11 #Gravitational Constant [m3kg-1s-2], https://www.britannica.com/science/gravitational-constant FOR NOW


#Function for distance between bodies

def d(state1, state2): #Takes state arrays as input
    x_1, y_1, z_1 = state1[0][0], state1[0][1], state1[0][2]
    x_2, y_2, z_2 = state2[0][0], state2[0][1], state2[0][2]
    return np.sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2 + (z_2 - z_1) ** 2) #Number output


#Function for gravitational acceleration due to one body

def aGravityComponent(mass, state, stateParticular): #Gives acceleration contribution due to a body with mass and state, acting on stateParticular
    return -1 * G * mass * (stateParticular[0] - state[0]) * d(state, stateParticular) ** (-3) #Outputs an array with the differing components of acceleration


#Function for gravitational acceleration due to many bodies

def aGravity(masses, states, stateParticular):#Takes list of masses and states (3D array of 2D state arrays) and the x and the state of the body which acceleration is being calculated for
    aGravityTotal = np.empty(3)
    for i in range(0, len(masses) + 1):
        aGravityTotal += aGravityComponent(masses[i], states[i], stateParticular) #Watch out that aGravityTotal doesn't become much larger than each component
    return aGravityTotal


#Function for gravitational velocity impact (none)

def vGravity(masses, states, statePaticular) #"Dummy" function for step & evolution functions
    return stateParticular[1] #Simply returns the velocity vector of the state