import numpy as np
import matplotlib.pyplot as plt

# parse csv from "position_sample.csv" into np.array with header removed
data = np.genfromtxt('position_sample.csv', delimiter=';', skip_header=1).T
rt=data[0]
rx=data[1]
ry=data[2]



p0 = 13.1888
p1 = 21.1013
p2 = 27.1315
p3 = -22.8966
p4 = -41.0979
p5 = 84.9714

x = []
y = []

for t in rt:
    x.append(p0*np.sin(p1*t+p2))
    y.append(p3*np.sin(p4*t+p5))



plt.scatter(x,y, color="red")
plt.scatter(rx,ry, color="blue")
plt.savefig("plot.png")