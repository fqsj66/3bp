#----------------------------------------------------
# SIMULATION FOR THE ROCKET IN THE EARTH-MOON SYSTEM
#----------------------------------------------------


#Imports

from functions_evolve import evolve
from functions_earthMoon import E_M_a_Gravity


#Inputs

print("""EARTH-MOON SYSTEM ROCKET SIMULATION

INPUTS (all SI units):

Initial Rocket Coordinates:""")

state = np.zeros(2, 3)
state[0][0] = input("x   : ")
state[0][1] = input("y   : ")
state[0][2] = input("z   : ")
state[1][0] = input("v_x : ")
state[1][1] = input("v_y : ")
state[1][2] = input("v_z : ")

print("""
Simulation Parameters:""")

t = input("Start time :")
dt = input("Time step  :")
T = input("End time   :")
useMethod = input("Step method (E/T/RK4) :")

print("""
Other:""")

useFile - input("Output file name :")

print("""
RUNNING SIMULATION...""")

evolve(state, t, dt, T, 0, E_M_a_Gravity, useMethod, useFile)

print("COMPLETE")