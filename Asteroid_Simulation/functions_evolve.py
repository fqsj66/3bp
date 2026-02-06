#----------------------------------------------------------
# FUNCTIONS FOR EVOLVING POSITION AND VELOCITY NUMERICALLY
#----------------------------------------------------------


#Imports

from imports import np
from imports import csv
from imports import scipy
#from functions_earthMoon import E_M_a_Gravity #Needed for RK45


#Functions for a step forward in time with various algorithms

def step_Euler(state, t, dt, f_v, f_a): #f_v and f_a may need to be altered using inbetween functions in the core program to have valid arguments
    stateChange = np.array([state[1], f_a(state, t)]) #Calculates the deviations 
    stateNew = state + stateChange * dt
    return stateNew

def step_Taylor(state, t, dt, f_v, f_a): #f_v is redundant, t gives the time at the start of the step, it is assumed f_a does not vary in time throughout the step
    f_a_values = f_a(state, t)
    return state + dt * np.array([state[1], f_a_values]) + (dt ** 2 / 2) * np.array([f_a_values, [0, 0, 0]])

def step_RK4(state, N, dt, f_v, f_a): #f_v is  redundant, N is the timestep number

    a0 = f_a(state, N, dt)

    x1 = state[0] + (dt / 2) * state[1]
    v1 = state[1] + (dt / 2) * a0
    a1 = f_a(np.array([x1, v1]), N, dt)

    x2 = state[0] + (dt / 2) * v1
    v2 = state[1] + (dt / 2) * a1
    a2 = f_a(np.array([x2, v2]), N, dt)

    x3 = state[0] + dt * v2
    v3 = state[1] + dt * a2
    a3 = f_a(np.array([x3, v3]), N, dt)

    xNew = state[0] + (dt / 6) * (state[1] + 2 * v1 + 2 * v2 + v3)
    vNew = state[1] + (dt / 6) * (a0 + 2 * a1 + 2 * a2 + a3)

    return np.array([(xNew), (vNew)])

#def step_RK45_dydx(t, state4RK45): #THIS WORKS ONLY FOR EARTH MOON SYSTEM
#    stateInsideThisF = np.array([[state4RK45[0], state4RK45[1], state4RK45[2]], [state4RK45[3], state4RK45[4], state4RK45[5]]])
#    return np.array([stateInsideThisF[1][0], stateInsideThisF[1][1], stateInsideThisF[1][2], E_M_a_Gravity(stateInsideThisF, t)[0], E_M_a_Gravity(stateInsideThisF, t)[1], E_M_a_Gravity(stateInsideThisF, t)[2]])

def step_RK45(state, t, dt, f_v, f_a):
    state4RK45 = np.array([state[0][0], state[0][1], state[0][2], state[1][0], state[1][1], state[1][2]])
    RK4ScipySolver = scipy.integrate.RK45(step_RK45_dydx, t, state4RK45, 3E6, first_step=dt, max_step=dt)
    RK4ScipySolver.step()
    return np.array([[RK4ScipySolver.y[0], RK4ScipySolver.y[1], RK4ScipySolver.y[2]], [RK4ScipySolver.y[3], RK4ScipySolver.y[4], RK4ScipySolver.y[5]]])


#Function for multiple steps forward

def evolve(state, t, dt, T, f_v, f_a, useMethod, useFile): #Evolve motion starting at state and time t, with timestep dt and end time T.
    
    N = int(np.round((T - t) / (dt))) + 1 #Number of timesteps needed
    print("Evolving Asteroid with N = {}".format(N))

    if useMethod == "T": #Taylor steps
        
        for j in range(0, N):
            state = step_Taylor(state, N, dt, f_v, f_a)

    else: #RK4 steps

        for j in range(0, N):
            state = step_RK4(state, N, dt, f_v, f_a)
            #print(state)
    
    #f.close()

    return state
