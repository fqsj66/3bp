#--------------
# CORE PROGRAM
#--------------

#Notes:
#Status of bodies, where applicable, are stored as a 2D array with rows in different dimensions and rows as x and v


#Test plotting Earth and Moon


from imports import np
#from imports import plt

#from functions_earthMoon import x_E_circular, x_M_circular

#x_E = np.array([0])
#y_E = np.array([0])

#x_M = np.array([0])
#y_M = np.array([0])

#for i in range(0, 40):
#    x_E_i, y_E_i = x_E_circular(i * 10000)
#    x_M_i, y_M_i = x_M_circular(i * 10000)

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


hello = np.empty((2,3))
print(hello)
test1 = np.array([0, 1, 2])
test2 = np.array([3, 4, 5])
print(test1)
print(test2)
hello[0] = test1
hello[1] = test2
print(hello)

hiya = np.array([[0, 1, 2], [3, 4, 5]])

print(hello + hiya * 2)