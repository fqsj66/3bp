#-------------------------------------------------
# Initial positions of asteroids in the Main Belt
#-------------------------------------------------


#Imports
from imports import np
from functions_solarSystem import m_Sol


#Constants

G = 6.6726E-11 #Gravitational Constant [m3kg-1s-2], project booklet
AU = 1.496E11
startR = 230E9 #These not full belt, hopefully just enough for two prominent kirkwood gaps
endR = 230E9 + AU


#Functions

def asteroidPopulation_line(Num):
    population = np.zeros((Num, 2, 3))
    for i in range(0, Num):
        x = startR + ((endR - startR) / Num) * i
        v_y = np.sqrt((G * m_Sol) / x)
        population[i] = np.array([[x, 0, 0], [0, v_y, 0]])
    return population