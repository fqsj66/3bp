#----------------------------------------------------------
# FUNCTIONS FOR EVOLVING POSITION AND VELOCITY NUMERICALLY
#----------------------------------------------------------


#Imports

from imports import np
from imports import csv


#Functions for a step forward in time with various algorithms

def step_Euler(state, t, dt, f_v, f_a): #f_v and f_a may need to be altered using inbetween functions in the core program to have valid arguments
    stateChange = np.array([f_v(state, t), f_a(state, t)]) #Calculates the deviations 
    stateNew = state + stateChange * dt
    return stateNew

def step_Taylor(state, t, dt, f_v, f_a): #f_v is redundant, t gives the time at the start of the step, it is assumed f_a does not vary in time throughout the step
    f_a_values = f_a(state, t)
    return state + dt * np.array([state[1], f_a_values]) + (dt ** 2 / 2) * nparray([f_a_values, [0, 0, 0]])

def step_RK4(state, t, dt, f_v, f_a): #f_v is  redundant, t ... (as above)
    x1 = state[0] + (dt / 2) * state[1]
    v1 = state[1] + (dt / 2) * f_a(state, t) #While f_a in general changes with time continuously, we assume it is constant over the step in t
    x2 = state[0] + (dt / 2) * v1
    v2 = state[1] + (dt / 2) * f_a(np.array([x1, v1]), t)
    x3 = state[0] + dt * v2
    v3 = state[1] + dt * f_a(np.array([x2, v2]), t)

    #May choose to store a123 as variables so they don't have to be re-evaluated here:
    stateNew = np.empty((2, 3))
    stateNew[0] = state[0] + (dt / 6) * (state[1] + 2 * v1 + 2 * v2 + v3)
    stateNew[1] = state[1] + (dt / 6) * (f_a(state, t) + 2 * f_a(np.array([x1, v1]), t) + 2 * f_a(np.array([x2, v2]), t) + f_a(np.array([x3, v3]), t))
    return stateNew


#Function for multiple steps forward

def evolve(state, t, dt, T, f_v, f_a, useMethod, useFile): #Evolve motion starting at state and time t, with timestep dt and end time T.
    N = np.round((T - t) / (dt * 50)) + 1 #Number of groups of 50 timesteps needed, added one in case rounds down to zero

    f = open(useFile, 'w+', newline='')
    writer = csv.writer(f)

    if useMethod == "E": #Euler steps

        for i in range(0, N):
            for j in range(0, 50): #Does 50 steps before saving current state again
                state = step_Euler(state, (t + 50 * i + j), dt, f_v, f_a) #Time calculated from number of individual steps
            writer.writerow(state[0]) #Saves positions only.................................................................DOES THIS KEEP THE FULL PRECISION OF THE NUMBERS?

    elif useMethod == "T": #Taylor steps

        for i in range(0, N):
            for j in range(0, 50):
                state = step_Taylor(state, (t + 50 * i + j), dt, f_v, f_a)
            writer.writerow(state[0])

    else: #RK4 steps

        for i in range(0, N):
            for j in range(0, 50):
                state = step_RK4(state, (t + 50 * i + j), dt, f_v, f_a)
            writer.writerow(state[0])
    
    f.close()
