#--------------
# CORE PROGRAM
#--------------

#Notes:
#Status of bodies, where applicable, are stored as a 2D array with rows in different dimensions and rows as x and v


#Test plotting Earth and Moon


from imports import np
#from imports import pd
#from imports import plt

#from functions_earthMoon import x_E_circular, x_M_circular

#x_E = np.array([0])
#y_E = np.array([0])

#x_M = np.array([0])
#y_M = np.array([0])

#for i in range(0, 40):
#    x_E_i, y_E_i = x_E_Circular(i * 10000)
#    x_M_i, y_M_i = x_M_Circular(i * 10000)

#    x_E = np.append(x_E, [x_E_i])
#    y_E = np.append(y_E, [y_E_i])
#    x_M = np.append(x_M, [x_M_i])
#    y_M = np.append(y_M, [y_M_i])

#plt.plot(x_M[1:], y_M[1:])
#plt.plot(x_E[1:], y_E[1:], color='red')
#plt.show()












#a = np.arange(6.0).reshape((3, 2))
#b = np.arange(6.0).reshape((3, 2))

#print(np.arange(6.0).reshape((3, 2)))
#print(np.arange(6.0).reshape((3, 2)))

#print("1")

#print(np.subtract(a, b))

#print("1")

#print(np.transpose(a))

#print(a[0])

#print(np.transpose(a)[0])


#hello = np.empty((2,3))
#print(hello)
#test1 = np.array([0, 1, 2])
#test2 = np.array([3, 4, 5])
#print(test1)
#print(test2)
#hello[0] = test1
#hello[1] = test2
#print(hello)

#hiya = np.array([[0, 1, 2], [3, 4, 5]])

#print(hello + hiya * 2)






#test = np.array([0, 1, 2])
#print(tuple(test))
#test2 = np.array([tuple(test), tuple(test)])
#print(test2)




#output = pd.read_csv("test.csv")
#print(output.x[0])

#testtest = 20

#print(str("t={}".format(testtest)))




from functions_evolve import step_RK4

x = np.arange(-10, 11)

def f_a(state, t):
    return [1, 0, 0]
def f_v(state, t):
    return state[1]

stateParticular = np.array([[-300000000, 0, 0], [0, 0, 0]])

t=0
dt=1

#print(step_RK4(stateParticular, t, dt, f_v, f_a))

#import os
#os.makedirs("images7/")


#Creating gif

from imports import pd
from imports import imageio

output = pd.read_csv("l2_3/rocket.csv")
xs = np.array(output.x)

frames = []
for frameNum in range(0, int(len(xs) / 2)):
    image = imageio.v2.imread(f'./l2_3/frames/{frameNum}.png')
    frames.append(image)
imageio.mimsave('./animation.gif', frames, fps = 20)