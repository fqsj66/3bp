#--------------------
# Simulation Running
#--------------------


#Imports

from imports import np, plt, time
from functions_solarSystem import Sol_M_J_a_Gravity, x_J_Circular, x_M_Circular, m_Sol, T_J
from functions_mainBelt import asteroidPopulation_line_elliptical, AU
from functions_evolve import evolve
from functions_gravity import ae_from_rv


#Constants

timestepNum = 0 #Save timestepNum s for each planet. Need to keep running count of how many revolutions Jupiter has done so that can tell how long the simulation is running for in in-simulation time
timestep = T_J / 1000
print("Timestep = {}s".format(timestep))
T = T_J * 100
asteroidNum = 50
eMax = 0.4

newSim = True
startingFile = "Simulations/1/example.csv"


#ACTUAL CODE

#Deciding whether to start new simulation of not
if newSim == False:
    #CONTINUE ON FROM HERE, LOOKING AT HOW TO LOAD FROM A CSV FILE, AND EVENTUALLY WRITE TO ONE AT THE END OF COURSE
else:
    population = asteroidPopulation_line_elliptical(asteroidNum, eMax)
    endpoints = np.zeros((asteroidNum, 2, 3))
    end_x = np.zeros(asteroidNum)
    end_y = np.zeros(asteroidNum)
    start_x = np.zeros(asteroidNum)
    start_y = np.zeros(asteroidNum)

print("START: {}".format(time.asctime(time.localtime())))

for i in range(0, asteroidNum):
    endpoints[i] = evolve(population[i], 0, timestep, T, 0, Sol_M_J_a_Gravity, "RK4", "")
    end_x[i] = endpoints[i][0][0]
    end_y[i] = endpoints[i][0][1]
    start_x[i] = population[i][0][0]
    start_y[i] = population[i][0][1]

print("END: {}".format(time.asctime(time.localtime())))






#OUTPUTS


#print(start_x)
#print(start_y)

#print(end_x)
#print(end_y)

#print(endpoints)

fig = plt.figure(figsize=(7, 7))
radii = np.sqrt(end_x ** 2 + end_y ** 2)
counts, bins = np.histogram(radii / AU)
plt.stairs(counts, bins)
#plt.xlim(0, 5)
plt.show()

fig = plt.figure(figsize=(7, 7))
plt.scatter(end_x / AU, end_y / AU, color="black")
plt.scatter(start_x / AU, start_y / AU, color="grey")
plt.scatter(x_J_Circular(1, T)[0]/ AU, x_J_Circular(1, T)[1]/ AU, color="orange")
plt.scatter(x_M_Circular(1, T)[0]/ AU, x_M_Circular(1, T)[1]/ AU, color="red")
plt.scatter([0], [0], color="yellow")
#plt.xlim(-8, 8)
#plt.ylim(-8, 8)
plt.show()

fig = plt.figure(figsize=(7, 7))
semimajoraxes = np.zeros(asteroidNum)
eccentricities = np.zeros(asteroidNum)

for i in range(0, asteroidNum):
    semimajoraxes[i], eccentricities[i] = ae_from_rv(endpoints[i], m_Sol)

print("""
      Ending Orbitals:""")
print(semimajoraxes)
print(eccentricities)
print("""
      """)

plt.scatter(semimajoraxes / AU, eccentricities)
plt.show()