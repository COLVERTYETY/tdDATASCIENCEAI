import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

from pyparsing import alphas

data = np.genfromtxt("./position_sample.csv",delimiter=";").T
# print("unsorted",data)
idx = np.argsort(data[0])
rt = np.take(data[0], idx)
rx = np.take(data[1], idx)
ry = np.take(data[2], idx)
# plt.scatter(rx,ry, color="red")

Nindiv = 10000
Nepochs = 100

rng = np.random.default_rng()

# selection rng
l = 8    # lower is softer
bias = 0.3 # higher is more
odsexp = np.exp(-1*l*np.linspace(0,1,Nindiv))
plt.plot(odsexp)
plt.title("Selection bias")
plt.show()
plt.cla()
selectmask = odsexp>(np.random.rand(Nindiv)-bias)
print("rate:=",100*sum(selectmask)/Nindiv,"%")

plt.hist(np.where(selectmask)[0])
plt.title("Selection mask")
plt.show()
plt.cla()

# get indexes of selected individuals
selectidx = np.where(selectmask)[0]
# get indexes of non-selected individuals
nonselectidx = np.where(~selectmask)[0]
# seperate nonselected in two groups
children = nonselectidx[:int(len(nonselectidx)/2)]
newindividuals = nonselectidx[int(len(nonselectidx)/2):]
# assign each non-selected individual to a selected individual
ods = rng.exponential(20,size=len(selectidx))
ods/=ods.sum()
Xidx = rng.choice(selectidx, size=len(children), replace=True,p=ods)
Yidx = rng.choice(selectidx, size=len(children), replace=True,p=ods)
plt.hist(sorted(Xidx))
plt.title("Xidx")
plt.show()
plt.cla()

# create random population
p1 = np.broadcast_to((rng.random(Nindiv)*200 -100)[...,None],(Nindiv,len(rt)) )
p2 = np.broadcast_to((rng.random(Nindiv)*200 -100)[...,None],(Nindiv,len(rt)) )
p3 = np.broadcast_to((rng.random(Nindiv)*200 -100)[...,None],(Nindiv,len(rt)) )
p4 = np.broadcast_to((rng.random(Nindiv)*200 -100)[...,None],(Nindiv,len(rt)) )
p5 = np.broadcast_to((rng.random(Nindiv)*200 -100)[...,None],(Nindiv,len(rt)) )
p6 = np.broadcast_to((rng.random(Nindiv)*200 -100)[...,None],(Nindiv,len(rt)) )
loss = np.ones(Nindiv)*np.inf

#shape data to population
RT = np.tile(rt, (Nindiv,1))
RX = np.tile(rx, (Nindiv,1))
RY = np.tile(ry, (Nindiv,1))

# debug
maxloss = []
minloss = []
meanloss = []
selectloss=[]
losses=[]

for epoch in range(Nepochs):  
    start = time.time()  
    xs = p1*np.sin((p2*RT)+p3)
    ys = p4*np.sin((p5*RT)+p6)
    errorx = (xs-RX)**2   # square penalises more the outliers then small errors
    errory = (ys-RY)**2
    loss = np.sum(errorx, axis=1) + np.sum(errory, axis=1)
    # print("loss:=", loss.shape, loss.mean(axis=0))

    # sort by loss 
    indx = np.argsort(loss)
    loss = np.take(loss, indx)
    p1 = np.take(p1, indx,axis=0)
    p2 = np.take(p2, indx,axis=0)
    p3 = np.take(p3, indx,axis=0)
    p4 = np.take(p4, indx,axis=0)
    p5 = np.take(p5, indx,axis=0)
    p6 = np.take(p6, indx,axis=0)
    # debug
    maxloss.append(loss.max())
    minloss.append(loss.min())
    meanloss.append(loss.mean())
    selectloss.append(loss[selectidx].mean())
    losses.append(loss)
    # display the best one
    if epoch%100==0:
        print(f"{epoch}: {loss.mean(axis=0)} {loss[0]} {loss[31]}",end="")

    # mutate
    p1[selectmask]+=rng.normal(0.0,1)
    p2[selectmask]+=rng.normal(0.0,1)
    p3[selectmask]+=rng.normal(0.0,1)
    p4[selectmask]+=rng.normal(0.0,1)
    p5[selectmask]+=rng.normal(0.0,1)
    p6[selectmask]+=rng.normal(0.0,1)

    # ceate new individuals
    p1[newindividuals] = (rng.random(1)*200 -100)
    p2[newindividuals] = (rng.random(1)*200 -100)
    p3[newindividuals] = (rng.random(1)*200 -100)
    p4[newindividuals] = (rng.random(1)*200 -100)
    p5[newindividuals] = (rng.random(1)*200 -100)
    p6[newindividuals] = (rng.random(1)*200 -100)
    
    #cross over
    p1[children] = p1[Xidx]
    p2[children] = p2[Xidx]
    p3[children] = p3[Xidx]
    p4[children] = p4[Yidx]
    p5[children] = p5[Yidx]
    p6[children] = p6[Yidx]

    stop= time.time()
    if epoch%100==0:
        print(" time:=", stop-start)



losses=np.array(losses)
plt.imshow(np.log(losses))
plt.title("losses")
plt.show()
plt.cla()
plt.fill_between(range(Nepochs), minloss, maxloss, color="blue", alpha=0.1)
plt.plot(meanloss, color="blue")
plt.plot(selectloss, color="red", alpha=0.5)
plt.title("losses")
plt.show()
plt.cla()
for i, txt in enumerate(rt):
    plt.annotate(txt, (rx[i], ry[i]))
plt.scatter(rx,ry, color="red", label=rt)
x=[]
y=[]
for t in rt:
    a=p1[0]*np.sin((p2[0]*t)+p3[0])
    x.append(a)
    b=p4[0]*np.sin((p5[0]*t)+p6[0])
    y.append(b)
plt.scatter(x,y, color="blue")
plt.title("best fit")
plt.show()
