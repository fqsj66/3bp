#----------------------------------------------------------------
# FUNCTIONS FOR THE POSITIONS OF BODIES IN THE EARTH-MOON SYSTEM
#----------------------------------------------------------------


#Imports

from imports import np


#Constants NEED TO STATE UNITS ALL SI FOR NOW

G = 6.67430E-11 #Gravitational Constant [m3kg-1s-2], https://www.britannica.com/science/gravitational-constant FOR NOW
d_EM = 3844E5 #Earth to moon distance [m], https://spaceplace.nasa.gov/moon-distance/en/ FOR NOW
m_E = 5.97E24 #Mass of Earth [kg], https://www.britannica.com/science/How-Big-Is-Earth FOR NOW
m_M = 7.3E22 #Mass of Moon [kg], https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/moon/ FOR NOW

r_E_circular = (d_EM * m_M) / (m_E + m_M) #Radius of Earth's orbit MAY NEED TO EXPAND BRACKET TO POWER -1
r_M_circular = (d_EM * m_E) / (m_E + m_M) #Radius of Moon's orbit

T_EM = np.sqrt(4 * np.pi ** 2 * d_EM ** 3 / (G * (m_M + m_E))) #Time period of orbit, worked out using K3L, may have to expand sqrt UNSURE IF THIS IS CORRECT


#Functions for the coordinates of Earth and Moon relative to centre of mass (and fixed stars)

def x_E_circular(t):
    #Earth starts at y=0, x>0 for t=0
    angle = ((2 * np.pi * t) / T_EM)
    x = r_E_circular * np.cos(angle)
    y = r_E_circular * np.sin(angle)
    return np.array([x, y])

def x_M_circular(t):
    #Moon starts at y=0, x<0 for t=0
    angle = ((2 * np.pi * t) / T_EM)
    x = -1 * r_M_circular * np.cos(angle)
    y = -1 * r_M_circular * np.sin(angle)
    return np.array([x, y])
