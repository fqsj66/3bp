#--------------------
# Simulation Running BUT VECTORISED!!!
#--------------------


#Imports

from imports import np, plt, time, csv, os, pd, mp
from functions_solarSystem import Sol_M_J_a_Gravity_V_Yarkovsky, m_Sol, T_J
from functions_mainBelt import asteroidPopulation_line_elliptical_V
from functions_evolve import evolve_V, evolve_V_P
from functions_gravity import ae_from_rv


#Constants

timestepNum = 0 #Save timestepNum s for each planet. Need to keep running count of how many revolutions Jupiter has done so that can tell how long the simulation is running for in in-simulation time
timestep = T_J / 1000
print("Timestep = {}s".format(timestep))
T = T_J * 1000
asteroidNum = 1000
eMax = 0.4

newSim = False
startingDirectory = "SimVectorisedWide"


#ACTUAL CODE
while True:

    #Deciding whether to start new simulation of not
    if newSim == False:

        files = os.listdir('Simulations\\{}'.format(startingDirectory))
        paths = [os.path.join('Simulations\\{}'.format(startingDirectory), basename) for basename in files]

        i_latest = 0
        for i in range(0, len(paths)): #Finding most recently modified file which is the current state of the simulation
            if float(os.path.getmtime(paths[i])) >= float(os.path.getmtime(paths[i_latest])):
                i_latest = i

        fileStart = pd.read_csv(paths[i_latest]) #Loading data from most recent output file
        print("READING FROM: {}".format(paths[i_latest]))
        #print(fileStart)
        
        N_M = (np.array(fileStart.x)[0])
        N_J = (np.array(fileStart.y)[0])
        N_start = np.array([N_M, N_J])

        xs = np.array(fileStart.x)[1:]
        ys = np.array(fileStart.y)[1:]
        zs = np.array(fileStart.z)[1:]
        vxs = np.array(fileStart.v_x)[1:]
        vys = np.array(fileStart.v_y)[1:]
        vzs = np.array(fileStart.v_z)[1:]

    else:

        #Set up sim file structure
        os.makedirs('Simulations\\{}'.format(startingDirectory))

        #Create initial conditions
        N_start = np.array([0, 0])
        xs, ys, zs, vxs, vys, vzs = asteroidPopulation_line_elliptical_V(asteroidNum, eMax)

        #Write initial conditions
        startFile = open('Simulations\\{}\\start.csv'.format(startingDirectory), 'w+', newline='')
        startWriter = csv.writer(startFile)
        startWriter.writerow(["x", "y", "z", "v_x", "v_y", "v_z"])
        startWriter.writerow([N_start[0], N_start[1], 0, 0, 0, 0])

        for i in range(0, len(xs)): #Not efficient but only happens once at the end of each run
            startWriter.writerow([xs[i], ys[i], zs[i], vxs[i], vys[i], vzs[i]])

        startFile.close()

        #Write parameters file
        paramsFile = open('Simulations\\{}\\params.csv'.format(startingDirectory), 'w+', newline='') #Creates csv file called the current time which is used to store (paused) results
        paramsWriter = csv.writer(paramsFile)
        paramsWriter.writerow(["timestep", "T", "asteroidNum", "eMax"])
        paramsWriter.writerow([timestep, T, asteroidNum, eMax])
        paramsFile.close()

        


    print("START: {}".format(time.asctime(time.localtime())))

    xs, ys, zs, vxs, vys, vzs = evolve_V(xs, ys, zs, vxs, vys, vzs, N_start, timestep, T, Sol_M_J_a_Gravity_V_Yarkovsky)

    print("END: {}".format(time.asctime(time.localtime())))


    #Saving file at the end of the sim

    print("SAVING...")

    resultsFile = open('Simulations\\{}\\{}.csv'.format(startingDirectory, time.time()), 'w+', newline='') #Creates csv file called the current time which is used to store (paused) results
    resultsWriter = csv.writer(resultsFile)
    resultsWriter.writerow(["x", "y", "z", "v_x", "v_y", "v_z"])
    #N_start[0] + int(np.round(T / timestep)) + 1
    resultsWriter.writerow([N_start[0] + int(np.round(T / timestep)) + 1, N_start[1] + int(np.round(T / timestep)) + 1, 0, 0, 0, 0])

    for i in range(0, len(xs)): #Not efficient but only happens once at the end of each run
        if np.abs(xs[i]) < 1E12 and np.abs(ys[i]) < 1E12: #Doesn't save particles that are outside solar system (> 10 AU)
            resultsWriter.writerow([xs[i], ys[i], zs[i], vxs[i], vys[i], vzs[i]])

    resultsFile.close()

    time.sleep(10)

    if newSim == True:
        newSim = False