#Producing plots based on csv files


#Imports

from imports import np, plt, time, os, pd
from functions_solarSystem import Sol_M_J_a_Gravity, x_J_Circular, x_M_Circular, m_Sol, T_J
from functions_mainBelt import AU
from functions_gravity import aei_from_rv


#Loading data from file

startingDirectory = "SimOneGap"

files = os.listdir('Simulations\{}'.format(startingDirectory))
paths = [os.path.join('Simulations\{}'.format(startingDirectory), basename) for basename in files]

i_latest = 0
i_earliest = 0
for i in range(0, len(paths)): #Finding most recently modified file which is the current state of the simulation
    print("At [{}], Path: {} has time: {}".format(i, paths[i], os.path.getmtime(paths[i])))
    if float(os.path.getmtime(paths[i])) > float(os.path.getmtime(paths[i_latest])):
        print("Converting i_latest to {}".format(i))
        i_latest = i
    if float(os.path.getmtime(paths[i])) < float(os.path.getmtime(paths[i_latest])):
        print("Converting i_earliest to {}".format(i))
        i_earliest = i

#fileStart = pd.read_csv("Simulations\\SimOvernight\\new.csv") #Loading data from most recent output file
fileStart = pd.read_csv(paths[i_latest])
print("Reading from {}".format(paths[i_latest]))
print("Reading from {}".format(paths[i_earliest]))
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

fileFirstPass = pd.read_csv(paths[i_earliest])
population0 = np.zeros((len(fileFirstPass) -1, 2, 3))
populationTrans0 = np.transpose(population0, (1, 2, 0))
populationTrans0[0][0] = np.array(fileFirstPass.x)[1:]
populationTrans0[0][1] = np.array(fileFirstPass.y)[1:]
populationTrans0[0][2] = np.array(fileFirstPass.z)[1:]
populationTrans0[1][0] = np.array(fileFirstPass.v_x)[1:]
populationTrans0[1][1] = np.array(fileFirstPass.v_y)[1:]
populationTrans0[1][2] = np.array(fileFirstPass.v_z)[1:]
population0 = np.transpose(populationTrans0, (2, 0, 1))


#Calculating orbital parameters

semimajoraxes = np.zeros(len(fileStart) - 1)
eccentricities = np.zeros(len(fileStart) - 1)
inclinations = np.zeros(len(fileStart) - 1)

semimajoraxes0 = np.zeros(len(fileFirstPass) - 1)
eccentricities0 = np.zeros(len(fileFirstPass) - 1)
inclinations0 = np.zeros(len(fileFirstPass) - 1)

for i in range(0, len(fileStart) - 1):
    semimajoraxes[i], eccentricities[i], inclinations[i] = aei_from_rv(population[i], m_Sol)

for j in range(0, len(fileFirstPass) - 1):
    semimajoraxes0[j], eccentricities0[j], inclinations0[j] = aei_from_rv(population0[j], m_Sol)

diffa = (semimajoraxes - semimajoraxes0) #Change in each particles semimajor axis
diffe = (eccentricities - eccentricities0) #np.abs


#Making Plots

fig0 = plt.figure(figsize=(7, 7))
counts, bins = np.histogram(semimajoraxes / AU)
plt.stairs(counts, bins)
plt.plot([2.502, 2.502], [0, 12], color = "red")
plt.xlabel("Semimajor Axis [AU]")
plt.ylabel("Asteroid Density")
#plt.xlim(0, 5)
plt.show()

fig1 = plt.figure(figsize=(7, 7))
plt.scatter(semimajoraxes / AU, eccentricities)
plt.plot([2.502, 2.502], [0, 0.3], color = "red")
#plt.plot([2.825, 2.825], [0, 0.3], color = "red")
#plt.plot([2.958, 2.958], [0, 0.3], color = "red")
plt.xlabel("Semimajor Axis [AU]")
plt.ylabel("Eccentricities")

fig2 = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter(xs, ys, zs)
ax.scatter([0], [0], [0], color = "yellow")
ax.scatter([227.956E9 / AU], [0], [0], color = "red")
ax.scatter([778.57E9 / AU], [0], [0], color = "orange")
#ax.set_title("Actual Positions")

fig3 = plt.figure(figsize=(7, 7))
plt.scatter(semimajoraxes / AU, inclinations)
plt.xlabel("Semimajor Axis [AU]")
plt.ylabel("Inclinations [rad]")

fig4 = plt.figure(figsize=(7, 7))
plt.scatter(semimajoraxes0 / AU, diffa / AU)
plt.plot([2.502, 2.502], [0, 0.013], color = "red")
plt.xlabel("Semimajor Axis [AU]", fontsize = 15)
plt.ylabel("Change in Semimajor Axis [AU]", fontsize = 15)

fig5 = plt.figure(figsize=(7, 7))
plt.scatter(semimajoraxes0 / AU, diffe / AU)
plt.plot([2.502, 2.502], [0, 3.5E-13], color = "red")
plt.xlabel("Semimajor Axis [AU]", fontsize = 15)
plt.ylabel("Change in Eccentricity", fontsize = 15)

plt.show()