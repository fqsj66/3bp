#--------------------
# Simulation Running
#--------------------


#Imports

from imports import np, plt
from functions_solarSystem import Sol_a_Gravity
from functions_mainBelt import asteroidPopulation_disc, AU
from functions_evolve import evolve


#Constants
 
timestepNum = 0 #Save timestepNum s for each planet. Need to keep running count of how many revolutions Jupiter has done so that can tell how long the simulation is running for in in-simulation time
timestep = 1000000


#Code

asteroidNum = 15
population = asteroidPopulation_disc(asteroidNum)
endpoints = np.zeros((asteroidNum, 2, 3))
end_x = np.zeros(asteroidNum)
end_y = np.zeros(asteroidNum)
start_x = np.zeros(asteroidNum)
start_y = np.zeros(asteroidNum)

for i in range(0, asteroidNum):
    endpoints[i] = evolve(population[i], 0, timestep, 1000000000 * 100, 0, Sol_a_Gravity, "RK4", "")
    end_x[i] = endpoints[i][0][0]
    end_y[i] = endpoints[i][0][1]
    start_x[i] = population[i][0][0]
    start_y[i] = population[i][0][1]

print(start_x)
print(start_y)

print(end_x)
print(end_y)

fig = plt.figure(figsize=(6, 6))
plt.scatter(end_x / AU, end_y / AU, color="black")
plt.scatter(start_x / AU, start_y / AU, color="red")
plt.show()