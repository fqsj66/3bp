#----------------------------------------------------------
# FUNCTIONS FOR EVOLVING POSITION AND VELOCITY NUMERICALLY
#----------------------------------------------------------


#Imports

from imports import np
from imports import csv
from imports import scipy
from functions_earthMoon import E_M_a_Gravity #Needed for RK45


#Functions for a step forward in time with various algorithms

def step_Euler(state, t, dt, f_v, f_a): #f_v and f_a may need to be altered using inbetween functions in the core program to have valid arguments
    stateChange = np.array([state[1], f_a(state, t)]) #Calculates the deviations 
    stateNew = state + stateChange * dt
    return stateNew

def step_Taylor(state, t, dt, f_v, f_a): #f_v is redundant, t gives the time at the start of the step, it is assumed f_a does not vary in time throughout the step
    f_a_values = f_a(state, t)
    return state + dt * np.array([state[1], f_a_values]) + (dt ** 2 / 2) * np.array([f_a_values, [0, 0, 0]])

def step_RK4(state, t, dt, f_v, f_a): #f_v is  redundant, t ... (as above)
    #x1 = state[0] + (dt / 2) * state[1]
    #v1 = state[1] + (dt / 2) * f_a(state, t) #While f_a in general changes with time continuously, we assume it is constant over the step in t
    #x2 = state[0] + (dt / 2) * v1
    #v2 = state[1] + (dt / 2) * f_a(np.array([x1, v1]), t)
    #x3 = state[0] + dt * v2
    #v3 = state[1] + dt * f_a(np.array([x2, v2]), t)

    #May choose to store a123 as variables so they don't have to be re-evaluated here:
    #stateNew = np.empty((2, 3))
    #stateNew[0] = state[0] + (dt / 6) * (state[1] + 2 * v1 + 2 * v2 + v3)
    #stateNew[1] = state[1] + (dt / 6) * (f_a(state, t) + 2 * f_a(np.array([x1, v1]), t) + 2 * f_a(np.array([x2, v2]), t) + f_a(np.array([x3, v3]), t))
    #return stateNew

    #REWRITTEN ALGORITHM:

    #x0 = state[0]
    #v0 = state[1]
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

def step_RK45_dydx(t, state4RK45): #THIS WORKS ONLY FOR EARTH MOON SYSTEM
    stateInsideThisF = np.array([[state4RK45[0], state4RK45[1], state4RK45[2]], [state4RK45[3], state4RK45[4], state4RK45[5]]])
    return np.array([stateInsideThisF[1][0], stateInsideThisF[1][1], stateInsideThisF[1][2], E_M_a_Gravity(stateInsideThisF, t)[0], E_M_a_Gravity(stateInsideThisF, t)[1], E_M_a_Gravity(stateInsideThisF, t)[2]])

def step_RK45(state, t, dt, f_v, f_a):
    state4RK45 = np.array([state[0][0], state[0][1], state[0][2], state[1][0], state[1][1], state[1][2]])
    RK4ScipySolver = scipy.integrate.RK45(step_RK45_dydx, t, state4RK45, 3E6, first_step=dt, max_step=dt)
    RK4ScipySolver.step()
    return np.array([[RK4ScipySolver.y[0], RK4ScipySolver.y[1], RK4ScipySolver.y[2]], [RK4ScipySolver.y[3], RK4ScipySolver.y[4], RK4ScipySolver.y[5]]])


#Function for multiple steps forward

def evolve(state, t, dt, T, f_v, f_a, useMethod, useFile): #Evolve motion starting at state and time t, with timestep dt and end time T.
    
    directory = "{}/rocket.csv".format(useFile)
    N = int(np.round((T - t) / (dt * 20))) + 1 #Number of groups of 20 timesteps needed, added one in case rounds down to zero

    f = open(directory, 'w+', newline='')
    writer = csv.writer(f)
    writer.writerow(["x", "y", "z"])

    if useMethod == "E": #Euler steps

        for i in range(0, N):
            for j in range(0, 20): #Does 50 steps before saving current state again
                state = step_Euler(state, (t + 20 * i + j), dt, f_v, f_a) #Time calculated from number of individual steps
            writer.writerow(state[0]) #Saves positions only.................................................................DOES THIS KEEP THE FULL PRECISION OF THE NUMBERS?

    elif useMethod == "T": #Taylor steps

        for i in range(0, N):
            for j in range(0, 20):
                state = step_Taylor(state, (t + 20 * i + j), dt, f_v, f_a)
            writer.writerow(state[0])

    elif useMethod == "45": #Scipy RK45 steps
        print("RK45")
        for i in range(0, N):
            for j in range(0, 20):
                state = step_RK45(state, (t + 20 * i + j), dt, f_v, f_a)
            writer.writerow(state[0])

    else: #RK4 steps

        for i in range(0, N):
            for j in range(0, 20):
                state = step_RK4(state, (t + 20 * i + j), dt, f_v, f_a)
            writer.writerow(state[0])
    
    f.close()
