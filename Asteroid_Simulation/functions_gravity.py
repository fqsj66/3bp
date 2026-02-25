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

def d_V(xs1, ys1, zs1, x2, y2, z2): #Same as above but vectorised. First 3 arguments are arrays. Last 3 are numbers for planet
    return np.sqrt((x2 - xs1) ** 2 + (y2 - ys1) ** 2 + (z2 - zs1) ** 2)


#Function for gravitational acceleration due to one body

def a_Gravity_Component(mass, state, stateParticular): #Gives acceleration contribution due to a body with mass and state, acting on stateParticular
    distanceBetweenBodies = d(state, stateParticular)  #Below used to be -1 * G * mass * (stateParticular[0] - state[0]) * (d(state, stateParticular) ** (-3))
    distanceReciprocalCubed = 1 / (distanceBetweenBodies * distanceBetweenBodies * distanceBetweenBodies)
    return -1 * G * mass * (stateParticular[0] - state[0]) * distanceReciprocalCubed #Outputs an array with the differing components of acceleration

def a_Gravity_Component_V(mass, xs, ys, zs, x2, y2, z2): #Same as above but vectorised
    distancesBetweenBodies = d_V(xs, ys, zs, x2, y2, z2)
    distancesReciprocalCubed = 1 / (distancesBetweenBodies * distancesBetweenBodies * distancesBetweenBodies)
    ax = -1 * G * mass * (xs - x2) * distancesReciprocalCubed
    ay = -1 * G * mass * (ys - y2) * distancesReciprocalCubed
    az = -1 * G * mass * (zs - z2) * distancesReciprocalCubed
    return ax, ay, az

#Function for gravitational acceleration due to many bodies

def a_Gravity(masses, states, stateParticular):#Takes list of masses and states (3D array of 2D state arrays) and the x and the state of the body which acceleration is being calculated for
    aGravityTotal = np.zeros(3)
    for i in range(0, len(masses)):
        #print("Particle at {}".format(stateParticular))
        #print("{} gravity Component = {}".format(i, a_Gravity_Component(masses[i], states[i], stateParticular)))
        aGravityTotal += a_Gravity_Component(masses[i], states[i], stateParticular) #Watch out that aGravityTotal doesn't become much larger than each component
    
    return aGravityTotal

def a_Gravity_V(masses, xs, ys, zs, xs2, ys2, zs2): #Same as above but vectorised. arrays for all the arguments
    ax = 0
    ay = 0
    az = 0
    for i in range(0, len(masses)): #Only 3 loops for main simulations so computationally justifiable
        axNew, ayNew, azNew = a_Gravity_Component_V(masses[i], xs, ys, zs, xs2[i], ys2[i], zs2[i])
        ax += axNew
        ay += axNew
        az += axNew
    return ax, ay, az


#Function for gravitational velocity impact (none)

def v_Gravity(masses, states, stateParticular): #"Dummy" function for step & evolution functions
    return stateParticular[1] #Simply returns the velocity vector of the state


#Functions for converting between positions & velocities and a & e

def rv_from_ae(a, e, m): #Gives initial state vector at periapse given semi-major axis, eccentricity and mass sum (same approx. as below)
    return np.array([[a * (1-e), 0, 0], [0, np.sqrt(G * m * (1 + e) / (a * (1-e))), 0]])

def ae_from_rv(state, m): #m should be total mass of two bodies, but assume that mass of sun >> asteroid mass so should just be sun's mass (for calculating mu)
    vSqr = np.sum(state[1] ** 2)
    v = np.sqrt(vSqr)
    r = np.sqrt(np.sum(state[0] ** 2))
    a = np.abs((vSqr / (G * m) - 2 / r) ** -1)
    #sinTheta = np.sqrt(np.sum(np.cross(state[0], state[1]) ** 2)) / (r * v)
    #e = (1 - (sinTheta ** 2 * r * (2 * a - r)) / (a ** 2)) ** 0.5
    e = np.sqrt(1 + 2 / ((G * m ) ** 2) * np.sum(np.cross(state[0], state[1]) ** 2) * (vSqr / 2 - G * m / r))

    return a, e

def aei_from_rv(state, m): #Same as the above function but includes inclination
    print("MAKING INCLINATIONS:")
    a, e = ae_from_rv(state, m)
    print(state[0][2])
    print((state[0]))
    print((state[0]) ** 2)
    print(np.sum(state[0] ** 2))
    print(np.sqrt(np.sum(state[0] ** 2)))
    print(np.arccos(state[0][2] / np.sqrt(np.sum(state[0] ** 2))))
    i = np.pi / 2 -  np.arccos(state[0][2] / np.sqrt(np.sum(state[0] ** 2))) #dot product angle approach
    print(i)
    return a, e, i
