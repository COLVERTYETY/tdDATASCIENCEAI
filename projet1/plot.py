import numpy as np
import matplotlib.pyplot as plt

# parse csv from "position_sample.csv" into np.array with header removed
data = np.genfromtxt('position_sample.csv', delimiter=';', skip_header=1).T
rt=data[0]
rx=data[1]
ry=data[2]



p0 = 13.19073
p1 = 21.09898
p2 = -85.95925
p3 = -22.90835
p4 = -41.09652
p5 = 59.83373

x = []
y = []

for t in rt:
    x.append(p0*np.sin(p1*t+p2))
    y.append(p3*np.sin(p4*t+p5))



plt.scatter(x,y, color="red")
plt.scatter(rx,ry, color="blue")
plt.savefig("plot.png")