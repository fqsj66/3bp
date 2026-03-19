#-------------------------------------------------
# Initial positions of asteroids in the Main Belt
#-------------------------------------------------


#Imports
from imports import np, rnd, plt
from functions_solarSystem import m_Sol
from functions_gravity import rv_from_ae, rv_from_aei

#Constants

G = 6.6726E-11 #Gravitational Constant [m3kg-1s-2], project booklet
AU = 1.496E11
startR = 2.1 * AU
endR = 2.9 * AU
#startR = 230E9 #These not full belt, hopefully just enough for two prominent kirkwood gaps
#endR = 230E9 + AU

#rnd.seed(10) #For testing, and comparing like-with-like starting positions

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
        #population[i][0][2] = 1 #NEED TO ADD SMALL DEVIATIONS LATER
    plt.scatter(semimajoraxis / AU, eccentricity)
    plt.show()
    print("""
          Starting orbitals:""")
    print(semimajoraxis)
    print(eccentricity)
    print("""
          """)
    return population

def asteroidPopulation_line_elliptical_V(Num, eMax): #Same as above but with vectorised compatibility
    
    population = np.zeros((Num, 2, 3))
    eccentricity = np.zeros(Num)
    semimajoraxis = np.zeros(Num)
    xs = np.zeros(Num)
    ys = np.zeros(Num)
    zs = np.zeros(Num)
    vxs = np.zeros(Num)
    vys = np.zeros(Num)
    vzs = np.zeros(Num)

    for i in range(0, Num): #This is not efficient but only runs once at the very start of each simulatiom
        eccentricity[i] = rnd.uniform(0, eMax)
        semimajoraxis[i] = ((endR - startR) * i / Num) + startR
        population[i] = rv_from_ae(((endR - startR) * i / Num) + startR, eccentricity[i], m_Sol)
        
        xs[i] = population[i][0][0]
        ys[i] = population[i][0][1]
        zs[i] = population[i][0][2]
        vxs[i] = population[i][1][0]
        vys[i] = population[i][1][1]
        vzs[i] = population[i][1][2]
    #plt.scatter(semimajoraxis / AU, eccentricity)
    #plt.show()
    #print("""
    #      Starting orbitals:""")
    #print(semimajoraxis)
    #print(eccentricity)
    #print("""
    #      """)
    
    #print(population)

    #print(xs)
    #print(ys)
    #print(zs)
    #print(vxs)
    #print(vys)
    #print(vzs)


    return xs, ys, zs, vxs, vys, vzs


def asteroidPopulation_resonance(Num): #Same as above but with non-randomised eccentricities
    
    population = np.zeros((Num, 2, 3))
    eccentricity = np.array([0.05, 0.15, 0.30])#np.zeros(Num)
    semimajoraxis = np.zeros(Num)
    xs = np.zeros(Num)
    ys = np.zeros(Num)
    zs = np.zeros(Num)
    vxs = np.zeros(Num)
    vys = np.zeros(Num)
    vzs = np.zeros(Num)

    for i in range(0, Num): #This is not efficient but only runs once at the very start of each simulatiom
        #eccentricity[i] = eAll
        semimajoraxis[i] = 2.502 * AU
        #population[i] = rv_from_ae(((endR - startR) * i / Num) + startR, eccentricity[i], m_Sol)
        population[i] = rv_from_ae(2.502 * AU, eccentricity[i], m_Sol)
        
        xs[i] = population[i][0][0]
        ys[i] = population[i][0][1]
        zs[i] = population[i][0][2]
        vxs[i] = population[i][1][0]
        vys[i] = population[i][1][1]
        vzs[i] = population[i][1][2]

        print("2.502")
        print(eccentricity[i])
        print(population[i])

    return xs, ys, zs, vxs, vys, vzs


# PROPER BEST ONE:
def asteroidPopulation_aei_V(Num, eMax, iMax, aStart, aEnd): #Same prosess as above, but with full functionality of a, e, and i. start and end radii of main belt are in AU
    
    aStart = aStart * AU
    aEnd = aEnd * AU
    iMax = iMax * (2 * np.pi / 360)

    population = np.zeros((Num, 2, 3))
    eccentricity = np.zeros(Num)
    #semimajoraxis = np.zeros(Num)
    inclination = np.zeros(Num)
    xs = np.zeros(Num)
    ys = np.zeros(Num)
    zs = np.zeros(Num)
    vxs = np.zeros(Num)
    vys = np.zeros(Num)
    vzs = np.zeros(Num)

    #Edit for wider range
    aCurrent = 3 * AU
    i = 0
    semimajoraxis2 = []
    while aCurrent <= (3.3 * AU):
        semimajoraxis2.append(aCurrent)
        i += 1
        aCurrent += 0.001 * AU
    semimajoraxis = np.array(semimajoraxis2[:-1])
    print(semimajoraxis / AU)

    for i in range(0, Num): #This is not efficient but only runs once at the very start of each simulatiom
        eccentricity[i] = rnd.uniform(0, eMax)
        inclination[i] = rnd.uniform(0, iMax)
        #semimajoraxis[i] = ((aEnd - aStart) * i / Num) + aStart
        population[i] = rv_from_aei(semimajoraxis[i], eccentricity[i], inclination[i], m_Sol)
        
        xs[i] = population[i][0][0]
        ys[i] = population[i][0][1]
        zs[i] = population[i][0][2]
        vxs[i] = population[i][1][0]
        vys[i] = population[i][1][1]
        vzs[i] = population[i][1][2]
    
    #print(eccentricity)

    return xs, ys, zs, vxs, vys, vzs