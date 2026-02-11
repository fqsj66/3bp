#-------------------------------------------------------------
# FUNCTIONS FOR THE CALCULATION OF GRAVITATIONAL ACCELERATION
#-------------------------------------------------------------


#Imports

from imports import np


#Constants NEED TO STATE UNITS

G = 6.6726E-11 #Gravitational Constant [m3kg-1s-2], https://www.britannica.com/science/gravitational-constant FOR NOW


#Function for distance between bodies

def d(state1, state2): #Takes state arrays as input
    #x_1, y_1, z_1 = state1[0][0], state1[0][1], state1[0][2]
    #x_2, y_2, z_2 = state2[0][0], state2[0][1], state2[0][2]
    #return np.hypot(np.hypot(x_2 - x_1, y_2 - y_1), z_2 - z_1)
    stateDiff = state2 - state1
    return np.hypot(np.hypot(stateDiff[0][0], stateDiff[0][1]), stateDiff[0][2])


#Function for gravitational acceleration due to one body

def a_Gravity_Component(mass, state, stateParticular): #Gives acceleration contribution due to a body with mass and state, acting on stateParticular
    distanceBetweenBodies = d(state, stateParticular)  #Below used to be -1 * G * mass * (stateParticular[0] - state[0]) * (d(state, stateParticular) ** (-3))
    distanceReciprocalCubed = 1 / (distanceBetweenBodies * distanceBetweenBodies * distanceBetweenBodies)
    return -1 * G * mass * (stateParticular[0] - state[0]) * distanceReciprocalCubed #Outputs an array with the differing components of acceleration
    

#Function for gravitational acceleration due to many bodies

def a_Gravity(masses, states, stateParticular):#Takes list of masses and states (3D array of 2D state arrays) and the x and the state of the body which acceleration is being calculated for
    aGravityTotal = np.zeros(3)
    for i in range(0, len(masses)):
        aGravityTotal += a_Gravity_Component(masses[i], states[i], stateParticular) #Watch out that aGravityTotal doesn't become much larger than each component
    return aGravityTotal


#Function for gravitational velocity impact (none)

def v_Gravity(masses, states, stateParticular): #"Dummy" function for step & evolution functions
    return stateParticular[1] #Simply returns the velocity vector of the state


#Functions for converting between positions & velocities and a & e

def rv_from_ae(a, e): #Gives initial state vector at periapse given semi-major axis and eccentricity
    return np.array([[a(1-e), 0, 0], [0, np.sqrt((1 + e) / (a * (1-e))), 0]])

def ae_from_rv(state, m): #m should be total mass of two bodies, but assume that mass of sun >> asteroid mass so should just be sun's mass (for calculating mu)
    vSqr = np.sum(state[1] ** 2)
    v = np.sqrt(vSqr)
    r = np.sqrt(np.sum(state[0] ** 2))
    a = (vSqr / (G * m) - 2 / r) ** -1
    sinTheta = np.sqrt(np.sum(np.cross(state[0], state[1]) ** 2)) / (r * v)
    e = (1 - (sinTheta ** 2 * r * (2 * a - r)) / (a ** 2)) ** 0.5
    return a, e