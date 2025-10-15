#----------------------------------------------------------
# FUNCTIONS FOR EVOLVING POSITION AND VELOCITY NUMERICALLY
#----------------------------------------------------------


#Imports

from imports import np


#Functions for a step forward in time with various algorithms

def step_Euler(state, dt, f_v, f_a): #f_v and f_a may need to be altered using inbetween functions in the core program to have valid arguments
    stateChange = np.array([f_v(state), f_a(state)]) #Calculates the deviations 
    stateNew = state + stateChange * dt
    return stateNew

def step_Taylor(state, dt, f_v, f_a):
    f_a_values = f_a(state)
    return state + dt * np.array([state[1], f_a_values]) + (dt ** 2 / 2) * nparray([f_a_values, [0, 0, 0]])


#Function for multiple steps forward