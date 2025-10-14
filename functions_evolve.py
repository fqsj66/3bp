#----------------------------------------------------------
# FUNCTIONS FOR EVOLVING POSITION AND VELOCITY NUMERICALLY
#----------------------------------------------------------


#Imports

from imports import np


#Functions for steps forward in time with various algorithms

def step_Euler(state, dt, f_v, f_a):
    stateNew = np.empty((3,2))
    stateNew[0][0] = state[0][0] + f_v(state[0][0], state[0][1])#Takes x and v as inputs?


#Function for multiple steps forward