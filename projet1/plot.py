import numpy as np
import matplotlib.pyplot as plt

# parse csv from "position_sample.csv" into np.array with header removed
data = np.genfromtxt('position_sample.csv', delimiter=';', skip_header=1).T
rt=data[0]
rx=data[1]
ry=data[2]



p0 = 0.00264477
p1 = 87.8377
p2 = -30.7315
p3 = 0.0120231
p4 = 48.53
p5 = -72.277

x = []
y = []

for t in rt:
    x.append(p0*np.sin(p1*t+p2))
    y.append(p3*np.sin(p4*t+p5))



plt.scatter(x,y, color="red")
plt.scatter(rx,ry, color="blue")
plt.show()