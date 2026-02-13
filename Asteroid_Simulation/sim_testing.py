#--------------------
# Simulation Running
#--------------------


#Imports

from imports import np, plt
from functions_solarSystem import Sol_a_Gravity, m_Sol
from functions_mainBelt import asteroidPopulation_line_elliptical, AU
from functions_evolve import evolve
from functions_gravity import ae_from_rv


#Constants
 
timestepNum = 0 #Save timestepNum s for each planet. Need to keep running count of how many revolutions Jupiter has done so that can tell how long the simulation is running for in in-simulation time
timestep = 10000
T = 27000000
asteroidNum = 100


#Code

population = asteroidPopulation_line_elliptical(asteroidNum, 0.3)
endpoints = np.zeros((asteroidNum, 2, 3))
end_x = np.zeros(asteroidNum)
end_y = np.zeros(asteroidNum)
start_x = np.zeros(asteroidNum)
start_y = np.zeros(asteroidNum)

for i in range(0, asteroidNum):
    endpoints[i] = evolve(population[i], 0, timestep, T, 0, Sol_a_Gravity, "RK4", "")
    end_x[i] = endpoints[i][0][0]
    end_y[i] = endpoints[i][0][1]
    start_x[i] = population[i][0][0]
    start_y[i] = population[i][0][1]

#print(start_x)
#print(start_y)

#print(end_x)
#print(end_y)

#print(endpoints)

semimajoraxes = np.zeros(asteroidNum)
eccentricities = np.zeros(asteroidNum)

for i in range(0, asteroidNum):
    semimajoraxes[i], eccentricities[i] = ae_from_rv(endpoints[i], m_Sol)

plt.scatter(semimajoraxes / AU, eccentricities)
plt.show()

print("Ending Orbitals")
print(semimajoraxes)
print(eccentricities)

fig = plt.figure(figsize=(7, 7))
radii = np.sqrt(end_x ** 2 + end_y ** 2)
counts, bins = np.histogram(radii / AU)
plt.stairs(counts, bins)
#plt.xlim(0, 5)
plt.show()

fig = plt.figure(figsize=(7, 7))
plt.scatter(end_x / AU, end_y / AU, color="black")
plt.scatter(start_x / AU, start_y / AU, color="grey")
plt.scatter([0], [0], color="yellow")
#plt.xlim(-8, 8)
plt.ylim(-8, 8)
plt.show()