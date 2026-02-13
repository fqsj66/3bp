#-------------------------------------------------
# Initial positions of asteroids in the Main Belt
#-------------------------------------------------


#Imports
from imports import np, rnd, plt
from functions_solarSystem import m_Sol
from functions_gravity import rv_from_ae

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

def asteroidPopulation_line_elliptical(Num, eMax):
    population = np.zeros((Num, 2, 3))
    eccentricity = np.zeros(Num)
    semimajoraxis = np.zeros(Num)
    for i in range(0, Num):
        eccentricity[i] = rnd.uniform(0, eMax)
        semimajoraxis[i] = ((endR - startR) * i / Num) + startR
        population[i] = rv_from_ae(((endR - startR) * i / Num) + startR, eccentricity[i], m_Sol)
    plt.scatter(semimajoraxis / AU, eccentricity)
    plt.show()
    print("""
          Starting orbitals:""")
    print(semimajoraxis)
    print(eccentricity)
    print("""
          """)
    return population