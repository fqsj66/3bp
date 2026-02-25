#--------------------
# Simulation Running
#--------------------


#Imports

from imports import np, plt, time, csv, os, pd
from functions_solarSystem import Sol_M_J_a_Gravity, x_J_Circular, x_M_Circular, m_Sol, T_J
from functions_mainBelt import asteroidPopulation_line_elliptical, AU
from functions_evolve import evolve2
from functions_gravity import ae_from_rv


#Constants

timestepNum = 0 #Save timestepNum s for each planet. Need to keep running count of how many revolutions Jupiter has done so that can tell how long the simulation is running for in in-simulation time
timestep = T_J / 1000
print("Timestep = {}s".format(timestep))
T = T_J / 50#T_J * 100
asteroidNum = 5#100
eMax = 0.3

newSim = True
startingDirectory = "SimTestingVectorisedNon"


#ACTUAL CODE
while True:

    #Deciding whether to start new simulation of not
    if newSim == False:

        files = os.listdir('Simulations\{}'.format(startingDirectory))
        paths = [os.path.join('Simulations\{}'.format(startingDirectory), basename) for basename in files]

        i_latest = 0
        for i in range(0, len(paths)): #Finding most recently modified file which is the current state of the simulation
            if float(os.path.getmtime(paths[i])) >= float(os.path.getmtime(paths[i_latest])):
                i_latest = i

        fileStart = pd.read_csv(paths[i_latest]) #Loading data from most recent output file
        N_M = (np.array(fileStart.x)[0])
        N_J = (np.array(fileStart.y)[0])
        N_start = np.array([N_M, N_J])
        print(len(fileStart))
        population = np.zeros((len(fileStart) -1, 2, 3))
        populationTrans = np.transpose(population, (1, 2, 0))
        print(populationTrans[0][0])
        print(np.array(fileStart.x)[1:])
        populationTrans[0][0] = np.array(fileStart.x)[1:]
        populationTrans[0][1] = np.array(fileStart.y)[1:]
        populationTrans[0][2] = np.array(fileStart.z)[1:]
        populationTrans[1][0] = np.array(fileStart.v_x)[1:]
        populationTrans[1][1] = np.array(fileStart.v_y)[1:]
        populationTrans[1][2] = np.array(fileStart.v_z)[1:]
        print(populationTrans[0][0])
        print(populationTrans[0][1])
        print(populationTrans[0][2])
        print(populationTrans[1][0])
        print(populationTrans[1][1])
        print(populationTrans[1][2])
        population = np.transpose(populationTrans, (2, 0, 1))

    else:
        #Set up sim file structure
        os.makedirs('Simulations\{}'.format(startingDirectory))
        N_start = np.array([0, 0])
        population = asteroidPopulation_line_elliptical(asteroidNum, eMax)
        print(population)

    #end_x = np.zeros(asteroidNum)
    #end_y = np.zeros(asteroidNum)
    #start_x = np.zeros(asteroidNum)
    #start_y = np.zeros(asteroidNum)

    print("START: {}".format(time.asctime(time.localtime())))

    endpoints = np.zeros((asteroidNum, 2, 3))
    for i in range(0, asteroidNum):
        endpoints[i] = evolve2(population[i], N_start, timestep, T, Sol_M_J_a_Gravity)
        #end_x[i] = endpoints[i][0][0]
        #end_y[i] = endpoints[i][0][1]
        #start_x[i] = population[i][0][0]
        #start_y[i] = population[i][0][1]

    print("END: {}".format(time.asctime(time.localtime())))


    #Saving file at the end of the sim

    print("SAVING...")

    resultsFile = open('Simulations\{}\{}.csv'.format(startingDirectory, time.time()), 'w+', newline='') #Creates csv file called the current time which is used to store (paused) results
    resultsWriter = csv.writer(resultsFile)
    resultsWriter.writerow(["x", "y", "z", "v_x", "v_y", "v_z"])
    N_start[0] + int(np.round(T / timestep)) + 1
    resultsWriter.writerow([N_start[0] + int(np.round(T / timestep)) + 1, N_start[1] + int(np.round(T / timestep)) + 1, 0, 0, 0, 0])

    for i in range(0, len(endpoints)):
        resultsWriter.writerow([endpoints[i][0][0], endpoints[i][0][1], endpoints[i][0][2], endpoints[i][1][0], endpoints[i][1][1], endpoints[i][1][2]])

    resultsFile.close()

    time.sleep(200)

    if newSim == True:
        newSim = False



#OUTPUTS


#print(start_x)
#print(start_y)

#print(end_x)
#print(end_y)

#print(endpoints)

#fig = plt.figure(figsize=(7, 7))
#radii = np.sqrt(end_x ** 2 + end_y ** 2)
#counts, bins = np.histogram(radii / AU)
#plt.stairs(counts, bins)
##plt.xlim(0, 5)
#plt.show()

#fig = plt.figure(figsize=(7, 7))
#plt.scatter(end_x / AU, end_y / AU, color="black")
#plt.scatter(start_x / AU, start_y / AU, color="grey")
#plt.scatter(x_J_Circular(1, T)[0]/ AU, x_J_Circular(1, T)[1]/ AU, color="orange")
#plt.scatter(x_M_Circular(1, T)[0]/ AU, x_M_Circular(1, T)[1]/ AU, color="red")
#plt.scatter([0], [0], color="yellow")
##plt.xlim(-8, 8)
##plt.ylim(-8, 8)
#plt.show()

#fig = plt.figure(figsize=(7, 7))
#semimajoraxes = np.zeros(asteroidNum)
#eccentricities = np.zeros(asteroidNum)

#for i in range(0, asteroidNum):
#    semimajoraxes[i], eccentricities[i] = ae_from_rv(endpoints[i], m_Sol)

#print("""
#      Ending Orbitals:""")
#print(semimajoraxes)
#print(eccentricities)
#print("""
#      """)

#plt.scatter(semimajoraxes / AU, eccentricities)
#plt.show()