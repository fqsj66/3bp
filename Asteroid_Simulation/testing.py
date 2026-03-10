from imports import np
from imports import mp

Num = 1000
aStart = 2 #Inner-most semimajor axis of starting asteroid population
aEnd = 3 #Outer-most equivalent
semimajoraxis = np.zeros(Num)
for i in range(0, Num):
    semimajoraxis[i] = ((aEnd - aStart) * i / Num) + aStart
print(semimajoraxis)

aCurrent = 3
i = 0
semimajoraxis2 = []
while aCurrent < 3.3:
    semimajoraxis2.append(aCurrent)
    i += 1
    aCurrent += 0.001
print(np.array(semimajoraxis2[:-1]))
print(len(semimajoraxis2[:-1])) #SO THIS MEANS THAT 


thingy = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
print(thingy[:10])
print("break")
print(thingy[10:])

def evolve(x, y, z, q):
    print(x)
    print(y)
    print(z)
    q.put("teststring")
    #return x, y, z

def f(q):
    q.put('X' * 1000000)

if __name__ == '__main__':
    q = mp.Queue()
    p = mp.Process(target=evolve, args=(["x1", "x2"],["y1", "y2"],["z1", "z2"],q))
    p.start()
    obj = q.get()
    p.join()
    print(obj)

#for i in range(0, 10):
#    print(i)

#one = np.array([1, 2, 3])
#two = np.array([4, 5, 6])

#three = np.sqrt(one ** 2 + two ** 2)
#print(three)