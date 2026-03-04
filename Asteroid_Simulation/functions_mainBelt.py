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
startR = 2.1 * AU
endR = 2.9 * AU
#startR = 230E9 #These not full belt, hopefully just enough for two prominent kirkwood gaps
#endR = 230E9 + AU

rnd.seed(10) #For testing

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