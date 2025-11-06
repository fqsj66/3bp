#----------------------------------------------------------------
# FUNCTIONS FOR THE POSITIONS OF BODIES IN THE EARTH-MOON SYSTEM
#----------------------------------------------------------------


#Imports

from imports import np
from functions_gravity import a_Gravity


#Constants NEED TO STATE UNITS ALL SI FOR NOW

G = 6.67430E-11 #Gravitational Constant [m3kg-1s-2], https://www.britannica.com/science/gravitational-constant FOR NOW
d_EM = 3844E5 #Earth to moon distance [m], https://spaceplace.nasa.gov/moon-distance/en/ FOR NOW
m_E = 5.97E24 #Mass of Earth [kg], https://www.britannica.com/science/How-Big-Is-Earth FOR NOW
m_M = 7.3E22 #Mass of Moon [kg], https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/moon/ FOR NOW

r_E_circular = (d_EM * m_M) / (m_E + m_M) #Radius of Earth's orbit MAY NEED TO EXPAND BRACKET TO POWER -1
r_M_circular = (d_EM * m_E) / (m_E + m_M) #Radius of Moon's orbit

T_EM = np.sqrt(4 * np.pi ** 2 * d_EM ** 3 / (G * (m_M + m_E))) #Time period of orbit, worked out using K3L, may have to expand sqrt UNSURE IF THIS IS CORRECT


#Functions for the coordinates of Earth and Moon relative to centre of mass (and fixed stars)

def x_E_Circular(t):
    #Earth starts at y=0, x>0 for t=0
    angle = ((2 * np.pi * t) / T_EM)
    x = r_E_circular * np.cos(angle)
    y = r_E_circular * np.sin(angle)
    return np.array([x, y, 0]) #In x-y plane only, zero z coordinate added for function compatability

def x_M_Circular(t):
    #Moon starts at y=0, x<0 for t=0
    angle = ((2 * np.pi * t) / T_EM)
    x = -1 * r_M_circular * np.cos(angle)
    y = -1 * r_M_circular * np.sin(angle)
    return np.array([x, y, 0])


#Function for calling functions_gravity subroutine a_Gravity at a certain time, calculating the states of the moon and sun to pass into this.

def E_M_a_Gravity(stateParticular, t): #Acceleration due to gravity of rocket at stateParticular at time t due to Earth and Moon system
    masses = np.array([m_E, m_M])
    states = np.array([[tuple(x_E_Circular(t)), [0, 0, 0]], [tuple(x_M_Circular(t)), [0, 0, 0]]]) #Set velocities to zero because these are redundant in the calculation, force of gravity independent of velocities
    return a_Gravity(masses, states, stateParticular)