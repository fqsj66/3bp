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

    #print(a0)

    return np.array([(xNew), (vNew)])


def step_RK4_V(xs0, ys0, zs0, vxs0, vys0, vzs0, N, dt, f_a): #Same as above but vectoried

    ax0, ay0, az0 = f_a(xs0, ys0, zs0, N, dt) #Shouldn't need to put in velocities?

    #x1 = state[0] + (dt / 2) * state[1]
    xs1 = xs0 + (dt / 2) * vxs0
    ys1 = ys0 + (dt / 2) * vys0
    zs1 = zs0 + (dt / 2) * vzs0
    #v1 = state[1] + (dt / 2) * a0
    vxs1 = vxs0 + (dt / 2) * ax0
    vys1 = vys0 + (dt / 2) * ay0
    vzs1 = vzs0 + (dt / 2) * az0
    #a1 = f_a(np.array([x1, v1]), N, dt)
    ax1, ay1, az1 = f_a(xs1, ys1, zs1, N, dt)

    #x2 = state[0] + (dt / 2) * v1
    xs2 = xs0 + (dt / 2) * vxs1
    ys2 = ys0 + (dt / 2) * vys1
    zs2 = zs0 + (dt / 2) * vzs1
    #v2 = state[1] + (dt / 2) * a1
    vxs2 = vxs0 + (dt / 2) * ax1
    vys2 = vys0 + (dt / 2) * ay1
    vzs2 = vzs0 + (dt / 2) * az1
    #a2 = f_a(np.array([x2, v2]), N, dt)
    ax2, ay2, az2 = f_a(xs2, ys2, zs2, N, dt)

    #x3 = state[0] + dt * v2
    xs3 = xs0 + dt * vxs2
    ys3 = ys0 + dt * vys2
    zs3 = zs0 + dt * vzs2
    #v3 = state[1] + dt * a2
    vxs3 = vxs0 + dt * ax2
    vys3 = vys0 + dt * ay2
    vzs3 = vzs0 + dt * az2
    #a3 = f_a(np.array([x3, v3]), N, dt)
    ax3, ay3, az3 = f_a(xs3, ys3, zs3, N, dt)

    #xNew = state[0] + (dt / 6) * (state[1] + 2 * v1 + 2 * v2 + v3)
    xsNew = xs0 + (dt / 6) * (vxs0 + 2 * vxs1 + 2 * vxs2 + vxs3)
    ysNew = ys0 + (dt / 6) * (vys0 + 2 * vys1 + 2 * vys2 + vys3)
    zsNew = zs0 + (dt / 6) * (vzs0 + 2 * vzs1 + 2 * vzs2 + vzs3)
    #vNew = state[1] + (dt / 6) * (a0 + 2 * a1 + 2 * a2 + a3)
    vxsNew = vxs0 + (dt / 6) * (ax0 + 2 * ax1 + 2 * ax2 + ax3)
    vysNew = vys0 + (dt / 6) * (ay0 + 2 * ay1 + 2 * ay2 + ay3)
    vzsNew = vzs0 + (dt / 6) * (az0 + 2 * az1 + 2 * az2 + az3)

    return xsNew, ysNew, zsNew, vxsNew, vysNew, vzsNew

#def step_RK45_dydx(t, state4RK45): #THIS WORKS ONLY FOR EARTH MOON SYSTEM
#    stateInsideThisF = np.array([[state4RK45[0], state4RK45[1], state4RK45[2]], [state4RK45[3], state4RK45[4], state4RK45[5]]])
#    return np.array([stateInsideThisF[1][0], stateInsideThisF[1][1], stateInsideThisF[1][2], E_M_a_Gravity(stateInsideThisF, t)[0], E_M_a_Gravity(stateInsideThisF, t)[1], E_M_a_Gravity(stateInsideThisF, t)[2]])

#def step_RK45(state, t, dt, f_v, f_a):
#    state4RK45 = np.array([state[0][0], state[0][1], state[0][2], state[1][0], state[1][1], state[1][2]])
#    RK4ScipySolver = scipy.integrate.RK45(step_RK45_dydx, t, state4RK45, 3E6, first_step=dt, max_step=dt)
#    RK4ScipySolver.step()
#    return np.array([[RK4ScipySolver.y[0], RK4ScipySolver.y[1], RK4ScipySolver.y[2]], [RK4ScipySolver.y[3], RK4ScipySolver.y[4], RK4ScipySolver.y[5]]])


#Function for multiple steps forward

def evolve(state, t, dt, T, f_v, f_a, useMethod, useFile): #Evolve motion starting at state and time t, with timestep dt and end time T.
    
    N = int(np.round((T - t) / (dt))) + 1 #Number of timesteps needed
    print("Evolving Asteroid with N = {}".format(N))

    if useMethod == "T": #Taylor steps
        
        for j in range(0, N):
            state = step_Taylor(state, N, dt, f_v, f_a)

    else: #RK4 steps

        for j in range(0, N):
            state = step_RK4(state, np.array([N, N]), dt, f_v, f_a)#This little [N, N] array is so that Sol_M_J_a_Gravity can be edited for different M and J timesteps
            #print(state)
    
    #f.close()

    return state



def evolve_V(xs, ys, zs, vxs, vys, vzs, N_start, dt, T, f_a): #Vectorised version of evolve for RK4_V, self contained
    
    N_end = int(np.round(T / dt)) + 1 #Number of timesteps needed
    print("Evolving Asteroids with N = {}".format(N_end))
    for j in range(0, N_end):
        xs, ys, zs, vxs, vys, vzs = step_RK4_V(xs, ys, zs, vxs, vys, vzs, N_start + j, dt, f_a)

    return xs, ys, zs, vxs, vys, vzs








def evolve2(state, N_start, dt, T, f_a): #Evolve corresponding to sim_mainBelt2
    
    N_end = int(np.round(T / dt)) + 1 #Number of timesteps needed
    #print("Evolving Asteroid with N = {}".format(N_end))
    for j in range(0, N_end):
        state = step_RK42(state, N_start + j, dt, f_a)

    return state


def step_RK42(state, N, dt, f_a): #RK4 step corresponding to sim_mainBelt2

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

    #print(a0)

    return np.array([(xNew), (vNew)])