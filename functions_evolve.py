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
    #stateNew = np.empty((2,3))
    #stateNew[0][0] = state[0][0] + f_v(state) * dt #x
    #stateNew[0][1] = state[0][1] + f_v(state) * dt #y NEED TO SOMEHOW TELL f_v WHICH DIMENSION?


#Function for multiple steps forward