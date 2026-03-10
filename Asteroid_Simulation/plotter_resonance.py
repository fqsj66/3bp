#Producing plots based on csv files


#Imports

from imports import np, plt, time, os, pd
from functions_solarSystem import Sol_M_J_a_Gravity, x_J_Circular, x_M_Circular, m_Sol, T_J
from functions_mainBelt import AU
from functions_gravity import aei_from_rv


#Loading data from file

startingDirectory = "SimVectorisedResonanceLonger" #or just "SimVectorisedResonance"

files = os.listdir('Simulations\{}'.format(startingDirectory))
paths = [os.path.join('Simulations\{}'.format(startingDirectory), basename) for basename in files]

a0 = []
a1 = []
a2 = []
e0 = []
e1 = []
e2 = []


for i in range(0, len(paths)): #Finding most recently modified file which is the current state of the simulation

    fileStart = pd.read_csv(paths[i])
    print("Reading from {}".format(paths[i]))
    N_M = (np.array(fileStart.x)[0])
    N_J = (np.array(fileStart.y)[0])
    N_start = np.array([N_M, N_J])
    population = np.zeros((len(fileStart) -1, 2, 3))
    populationTrans = np.transpose(population, (1, 2, 0))
    populationTrans[0][0] = np.array(fileStart.x)[1:]
    populationTrans[0][1] = np.array(fileStart.y)[1:]
    populationTrans[0][2] = np.array(fileStart.z)[1:]
    populationTrans[1][0] = np.array(fileStart.v_x)[1:]
    populationTrans[1][1] = np.array(fileStart.v_y)[1:]
    populationTrans[1][2] = np.array(fileStart.v_z)[1:]
    population = np.transpose(populationTrans, (2, 0, 1))

    xs = np.array(fileStart.x)[1:] / AU
    ys = np.array(fileStart.y)[1:] / AU
    zs = np.array(fileStart.z)[1:] / AU
    vxs = np.array(fileStart.v_x)[1:]
    vys = np.array(fileStart.v_y)[1:]
    vzs = np.array(fileStart.v_z)[1:]


    #Calculating orbital parameters

    semimajoraxes = []#np.zeros(len(fileStart) - 1)
    eccentricities = []#np.zeros(len(fileStart) - 1)
    inclinations = []#np.zeros(len(fileStart) - 1)

    for i in range(0, len(fileStart) - 1):
        semimajoraxesi, eccentricitiesi, inclinationsi = aei_from_rv(population[i], m_Sol)
        
        if True: #(semimajoraxesi / AU) > 2.4 and (semimajoraxesi / AU) < 2.6:
            semimajoraxes.append(semimajoraxesi)
            eccentricities.append(eccentricitiesi)
            inclinations.append(inclinationsi)

    a0.append(semimajoraxes[0])
    a1.append(semimajoraxes[1])
    a2.append(semimajoraxes[2])
    e0.append(eccentricities[0])
    e1.append(eccentricities[1])
    e2.append(eccentricities[2])

#diffa = (semimajoraxes - semimajoraxes0) #Change in each particles semimajor axis
#diffe = (eccentricities - eccentricities0) #np.abs


#Making Plots

a0 = np.array(a0)
a1 = np.array(a1)
a2 = np.array(a2)
e0 = np.array(e0)
e1 = np.array(e1)
e2 = np.array(e2)

fig1 = plt.figure(figsize=(7, 7))
#plt.scatter(semimajoraxes0 / AU, eccentricities0, color = "blue", label = "Initial")
plt.plot(a0 / AU, e0, color = "red", label = "0.05")
plt.plot(a1 / AU, e1, color = "blue", label = "0.15")
plt.plot(a2 / AU, e2, color = "green", label = "0.3")
plt.plot([2.502, 2.502], [0, 0.3], color = "red")
#plt.plot([2.825, 2.825], [0, 0.3], color = "red")
#plt.plot([2.958, 2.958], [0, 0.3], color = "red")
plt.xlabel("Semimajor Axis [AU]")
plt.ylabel("Eccentricities")
#plt.xlim(2, 3)
#plt.ylim(0, 0.5)
plt.legend()

fig2 = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter(xs, ys, zs)
ax.scatter([0], [0], [0], color = "yellow")
ax.scatter([227.956E9 / AU], [0], [0], color = "red")
ax.scatter([778.57E9 / AU], [0], [0], color = "orange")
#ax.set_title("Actual Positions")


plt.show()