#Producing plots based on csv files


#Imports

from imports import np, plt, time, os, pd, scipy
from functions_solarSystem import Sol_M_J_a_Gravity, x_J_Circular, x_M_Circular, m_Sol, T_J
from functions_mainBelt import AU
from functions_gravity import aei_from_rv


#Loading data from file

startingDirectory = "analysis" #Simply reads the csv file in analysis

files = os.listdir('Simulations\{}'.format(startingDirectory))
paths = [os.path.join('Simulations\{}'.format(startingDirectory), basename) for basename in files]

i_latest = 0
i_earliest = 1
#for i in range(0, len(paths)): #Finding most recently modified file which is the current state of the simulation
#    print("At [{}], Path: {} has time: {}".format(i, paths[i], os.path.getmtime(paths[i])))
#    if float(os.path.getmtime(paths[i])) > float(os.path.getmtime(paths[i_latest])):
#        print("Converting i_latest to {}".format(i))
#        i_latest = i
#    if (float(os.path.getmtime(paths[i])) < float(os.path.getmtime(paths[i_latest]))) and paths[i] != "Simulations\{}\params.csv".format(startingDirectory):
#        print("Converting i_earliest to {}".format(i))
#        i_earliest = i

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

fileObs = pd.read_csv("Observations\\NASA.csv")
semimajoraxesObs = fileObs.a
eccentricitiesObs = fileObs.e
inclinationsObs = fileObs.i

#Calculating orbital parameters

semimajoraxes = []#np.zeros(len(fileStart) - 1)
eccentricities = []#np.zeros(len(fileStart) - 1)
inclinations = []#np.zeros(len(fileStart) - 1)

semimajoraxes0 = np.zeros(len(fileFirstPass) - 1)
eccentricities0 = np.zeros(len(fileFirstPass) - 1)
inclinations0 = np.zeros(len(fileFirstPass) - 1)

for i in range(0, len(fileStart) - 1):
    semimajoraxesi, eccentricitiesi, inclinationsi = aei_from_rv(population[i], m_Sol)
    
    if True: #(semimajoraxesi / AU) > 2.4 and (semimajoraxesi / AU) < 2.6:
        semimajoraxes.append(semimajoraxesi)
        eccentricities.append(eccentricitiesi)
        inclinations.append(inclinationsi)

for j in range(0, len(fileFirstPass) - 1):
    semimajoraxes0[j], eccentricities0[j], inclinations0[j] = aei_from_rv(population0[j], m_Sol)

#diffa = (semimajoraxes - semimajoraxes0) #Change in each particles semimajor axis
#diffe = (eccentricities - eccentricities0) #np.abs


#Making Plots

semimajoraxes = np.array(semimajoraxes)
eccentricities = np.array(eccentricities)
inclinations = np.array(inclinations)

#print(semimajoraxes)
fig0 = plt.figure(figsize=(7, 7))
counts, bins = np.histogram(semimajoraxes / AU, bins = np.arange(0, 3.3, 0.019))
counts0, bins0 = np.histogram(semimajoraxes0 / AU, bins = 100)
countsObs, binsObs = np.histogram(semimajoraxesObs, bins = np.arange(0, 3.3, 0.019))

area = 0
positions = []
for i in range(0, len(bins) - 1):
    area += counts[i] * (bins[i+1] - bins[i])
    positions.append(bins[i] + ((bins[i+1] - bins[i]) / 2))

area0 = 0
for i in range(0, len(bins0) - 1):
    area0 += counts0[i] * (bins0[i+1] - bins0[i])

areaObs = 0
for i in range(0, len(binsObs) - 1):
    areaObs += countsObs[i] * (binsObs[i+1] - binsObs[i])

#plt.stairs(counts0 / (area0 * len(bins0)), bins0)
plt.stairs(countsObs / (areaObs * len(binsObs)), binsObs, color = "blue")
plt.stairs(counts / (area * len(bins)), bins, color = "black", linestyle = "dashed")
plt.errorbar(positions, counts / (area * len(bins)), [np.sqrt(counts) / (area * len(bins)), np.sqrt(counts) / (area * len(bins))], color = "black", fmt = '-', capsize = 3, elinewidth = 1, markersize = 1, linestyle='')

#print(bins)
#print(counts)
plt.scatter(bins[131], counts[131] / (area * len(bins)), color = "red")#, markersize = 10) #JUST TO SHOW WHERE THE POINT IS
plt.plot([2.502, 2.502], [0, np.max(countsObs / (areaObs * len(binsObs)))], color = "red", linestyle = "dashed")
plt.plot([2.825, 2.825], [0, np.max(countsObs / (areaObs * len(binsObs)))], color = "red", linestyle = "dashed")
plt.plot([2.958, 2.958], [0, np.max(countsObs / (areaObs * len(binsObs)))], color = "red", linestyle = "dashed")
plt.plot([2.065, 2.065], [0, np.max(countsObs / (areaObs * len(binsObs)))], color = "red", linestyle = "dashed")
plt.plot([3.279, 3.279], [0, np.max(countsObs / (areaObs * len(binsObs)))], color = "red", linestyle = "dashed")

#plt.scatter([227.956E9 / AU], [np.max(counts) / (np.sum(counts) * 2)], color = "red")
plt.xlabel("Semimajor Axis [AU]")
plt.ylabel("Asteroid Density")
plt.xlim(1.5, 3.4)
#plt.show()

from scipy.stats import ks_2samp #KS testing
ksResult = ks_2samp(countsObs, counts)
print(ksResult)

fig1 = plt.figure(figsize=(7, 7))
#plt.scatter(semimajoraxes0 / AU, eccentricities0, color = "blue", label = "Initial")
#plt.scatter(semimajoraxes / AU, eccentricities, color = "black", label = "Simulation")
plt.errorbar(semimajoraxes / AU, eccentricities, xerr = 0, yerr = 0, color = "black", fmt = '.', capsize = 0, elinewidth = 0, markersize = 5, linestyle='', label = "Simulation")
#plt.scatter(semimajoraxesObs, eccentricitiesObs, marker = ',', color = "blue", label = "Observation")#, markersize = 1)
plt.errorbar(semimajoraxesObs, eccentricitiesObs, xerr = 0, yerr = 0, color = "blue", fmt = '.', capsize = 0, elinewidth = 0, markersize = 0.2, linestyle='', label = "Observation")
plt.plot([2.502, 2.502], [0, np.max(eccentricitiesObs)], color = "red", linestyle = "dashed")
plt.plot([2.825, 2.825], [0, np.max(eccentricitiesObs)], color = "red", linestyle = "dashed")
plt.plot([2.958, 2.958], [0, np.max(eccentricitiesObs)], color = "red", linestyle = "dashed")
plt.plot([2.065, 2.065], [0, np.max(eccentricitiesObs)], color = "red", linestyle = "dashed")
plt.plot([3.279, 3.279], [0, np.max(eccentricitiesObs)], color = "red", linestyle = "dashed")
plt.xlabel("Semimajor Axis [AU]")
plt.ylabel("Eccentricities")
#plt.xlim(2, 3)
#plt.ylim(0, 0.5)
#plt.legend()

fig2 = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter(xs, ys, zs)
ax.scatter([0], [0], [0], color = "yellow")
ax.scatter([227.956E9 / AU], [0], [0], color = "red")
ax.scatter([778.57E9 / AU], [0], [0], color = "orange")
ax.axes.set_xlim(-4, 4)
ax.axes.set_ylim(-4, 4)
ax.axes.set_zlim(-4, 4)
#ax.set_title("Actual Positions")

fig3 = plt.figure(figsize=(7, 7))
#plt.scatter(semimajoraxes / AU, np.abs(inclinations * (360 / (np.pi * 2))), color = "black", label = "Simulation", marker = "o")
plt.errorbar(semimajoraxes / AU, np.abs(inclinations * (360 / (np.pi * 2))), xerr = 0, yerr = 0, color = "black", fmt = '.', capsize = 0, elinewidth = 0, markersize = 5, linestyle='', label = "Simulation")

#plt.scatter(semimajoraxesObs, inclinationsObs, color = "blue", label = "Observation", marker = ".", markersize = "0.01")
plt.errorbar(semimajoraxesObs, inclinationsObs, xerr = 0, yerr = 0, color = "blue", fmt = '.', capsize = 0, elinewidth = 0, markersize = 0.1, linestyle='')

#plt.scatter(semimajoraxes / AU, inclinations * (360 / (np.pi * 2)), color = "red", label = "Final")
plt.xlabel("Semimajor Axis [AU]")
plt.ylabel("Inclinations [deg]")
#plt.xlim(2.1, 2.9)

fig6 = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter(semimajoraxesObs, eccentricitiesObs, inclinationsObs)
#ax.scatter(semimajoraxes, eccentricities, inclinations)
ax.set_xlabel("Semimajor Axis [AU]")
ax.set_ylabel("Eccentricities")
ax.set_zlabel("Inclinations [deg]")

#fig4 = plt.figure(figsize=(7, 7))
#plt.scatter(semimajoraxes0 / AU, diffa / AU)
#plt.plot([2.502, 2.502], [0, 0.013], color = "red")
#plt.xlabel("Semimajor Axis [AU]", fontsize = 15)
#plt.ylabel("Change in Semimajor Axis [AU]", fontsize = 15)

#fig5 = plt.figure(figsize=(7, 7))
#plt.scatter(semimajoraxes0 / AU, diffe / AU)
#plt.plot([2.502, 2.502], [0, 3.5E-13], color = "red")
#plt.xlabel("Semimajor Axis [AU]", fontsize = 15)
#plt.ylabel("Change in Eccentricity", fontsize = 15)



plt.show()