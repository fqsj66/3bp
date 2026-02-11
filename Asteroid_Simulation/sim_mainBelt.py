#--------------------
# Simulation Running
#--------------------


#Imports

from imports import np, plt
from functions_solarSystem import Sol_M_J_a_Gravity, x_J_Circular, x_M_Circular
from functions_mainBelt import asteroidPopulation_line, AU
from functions_evolve import evolve


#Constants
 
timestepNum = 0 #Save timestepNum s for each planet. Need to keep running count of how many revolutions Jupiter has done so that can tell how long the simulation is running for in in-simulation time
timestep = 1000000
T = 0.3E11
asteroidNum = 1


#Code

population = asteroidPopulation_line(asteroidNum)
endpoints = np.zeros((asteroidNum, 2, 3))
end_x = np.zeros(asteroidNum)
end_y = np.zeros(asteroidNum)
start_x = np.zeros(asteroidNum)
start_y = np.zeros(asteroidNum)

for i in range(0, asteroidNum):
    endpoints[i] = evolve(population[i], 0, timestep, T, 0, Sol_M_J_a_Gravity, "RK4", "")
    end_x[i] = endpoints[i][0][0]
    end_y[i] = endpoints[i][0][1]
    start_x[i] = population[i][0][0]
    start_y[i] = population[i][0][1]

print(start_x)
print(start_y)

print(end_x)
print(end_y)

print(endpoints)

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