#Imports

from imports import np


#Constants NEED TO STATE UNITS

G = #gravitational constant


#Function for distance between bodies

def d(first, second):#Takes numpy arrays of 3D coordinates
    x_1, y_1, z_1 = first
    x_2, y_2, z_2 = second
    return np.sqrt(mod(x_2 - x_1) ** 2 + mod(y_2 - y_1) ** 2 + mod(z_2 - z_1) ** 2)


#Function for acceleration due to gravity

def a(values):#should return a vector?
    mass, first, second = values
    return -1 * G * mass * (first - second) * d(first, second) ** (-3)