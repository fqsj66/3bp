#----------------------------------------------------------
# FUNCTIONS FOR EVOLVING POSITION AND VELOCITY NUMERICALLY
#----------------------------------------------------------


#Imports

from imports import np


#Functions for a step forward in time with various algorithms

def step_Euler(state, t, dt, f_v, f_a): #f_v and f_a may need to be altered using inbetween functions in the core program to have valid arguments
    stateChange = np.array([f_v(state, t), f_a(state, t)]) #Calculates the deviations 
    stateNew = state + stateChange * dt
    return stateNew

def step_Taylor(state, t, dt, f_v, f_a): #f_v is redundant, t gives the time at the start of the step so that f_a may vary in time
    f_a_values = f_a(state, t)
    return state + dt * np.array([state[1], f_a_values]) + (dt ** 2 / 2) * nparray([f_a_values, [0, 0, 0]])

def step_RK4(state, t, dt, f_v, f_a): #f_v is  redundant, t ... (as above)
    x1 = state[0] + (dt / 2) * state[1]
    v1 = state[1] + (dt / 2) * f_a(state, (t + dt / 2)) #Need to check that these times are correct. Do they even need to change? Should i just put t?
    x2 = state[0] + (dt / 2) * x.1
    v2 = state[1] + (dt / 2) * f_a(np.array([x1, v1]), t) #Just putting t for now
    x3 = state[0] + dt * v2
    v3 = state[1] + dt * f_a(np.array([x2, v2]), t)

    #May choose to store a123 as variables so they don't have to be re-evaluated here:
    stateNew = np.empty((2, 3))
    stateNew[0] = state[0] + dt / 6 * (state[1] + 2 * v1 + 2 * v2 + v3)
    stateNew[1] = state[1] + dt / 6 * (f_a(state, t) + 2 * f_a(np.array([x1, v1]), t) + 2 * f_a(np.array([x2, v2]), t) + f_a(np.array([x3, v3]), t)) #Need to check t's here too
    return stateNew


#Function for multiple steps forward

def evolve(state, dt, f_v, f_a, useMethod, useFile):
    return "filler"
