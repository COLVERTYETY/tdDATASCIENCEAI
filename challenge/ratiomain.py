import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time


plt.ion()

data = np.genfromtxt("./position_sample.csv",delimiter=";").T
# print("unsorted",data)
idx = np.argsort(data[0])
rt = np.take(data[0], idx)
rx = np.take(data[1], idx)
ry = np.take(data[2], idx)
# plt.scatter(rx,ry, color="red")

Nindiv = 5000
Nepochs = 1001
ratio1 = 0.3    # mutate only
ratio2 = 0.1   # clones
ratio3 = 0.5    # children
clonecutoff = 10

if ratio1+ratio2+ratio3>=1:
    raise Exception("ratio greater than 1")

cut1 = int(Nindiv*ratio1)
passidx = np.arange(0, cut1)
cut2 = int(Nindiv*ratio2)+cut1
cloneidx = np.arange(cut1,cut2)
cut3 = int(Nindiv*ratio3)+cut2
childrenidx = np.arange(cut2,cut3)
newidx = np.arange(cut3, Nindiv)

rng = np.random.default_rng()


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
    errorx = abs(RX-xs)/abs(RX)#(xs-RX)**2  # square penalises more the outliers then small errors
    errory = abs(RY-ys)/abs(RY)#(ys-RY)**2
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
    # selectloss.append(loss[selectidx].mean())
    losses.append(loss)
    # display the best one
    if epoch%100==0:
        print(f"{epoch}: {loss[0]} {np.mean(loss[:100])}",end="")

    #select parents for clones
    parentclones = rng.choice(np.arange(0,clonecutoff), size=len(cloneidx), replace=True)
    p1[cloneidx] = p1[parentclones]+np.broadcast_to(rng.normal(0.0,1.5,size=len(parentclones))[...,None], (len(parentclones),len(rt)) )
    p2[cloneidx] = p2[parentclones]+np.broadcast_to(rng.normal(0.0,1.5,size=len(parentclones))[...,None], (len(parentclones),len(rt)) )
    p3[cloneidx] = p3[parentclones]+np.broadcast_to(rng.normal(0.0,1.5,size=len(parentclones))[...,None], (len(parentclones),len(rt)) )
    p4[cloneidx] = p4[parentclones]+np.broadcast_to(rng.normal(0.0,1.5,size=len(parentclones))[...,None], (len(parentclones),len(rt)) )
    p5[cloneidx] = p5[parentclones]+np.broadcast_to(rng.normal(0.0,1.5,size=len(parentclones))[...,None], (len(parentclones),len(rt)) )
    p6[cloneidx] = p6[parentclones]+np.broadcast_to(rng.normal(0.0,1.5,size=len(parentclones))[...,None], (len(parentclones),len(rt)) )

    # select parents for children different for x and y
    parentschildren = rng.choice(passidx, size = len(childrenidx),replace=True)
    p1[childrenidx] = p1[parentschildren]
    p2[childrenidx] = p2[parentschildren]
    p3[childrenidx] = p3[parentschildren]
    parentschildren = rng.choice(passidx, size = len(childrenidx),replace=True)
    p4[childrenidx] = p4[parentschildren]
    p5[childrenidx] = p5[parentschildren]
    p6[childrenidx] = p6[parentschildren]

    # create the new individuals
    p1[newidx] = np.broadcast_to((rng.random(len(newidx))*200 -100)[...,None], (len(newidx),len(rt)) )
    p2[newidx] = np.broadcast_to((rng.random(len(newidx))*200 -100)[...,None], (len(newidx),len(rt)) )
    p3[newidx] = np.broadcast_to((rng.random(len(newidx))*200 -100)[...,None], (len(newidx),len(rt)) )
    p4[newidx] = np.broadcast_to((rng.random(len(newidx))*200 -100)[...,None], (len(newidx),len(rt)) )
    p5[newidx] = np.broadcast_to((rng.random(len(newidx))*200 -100)[...,None], (len(newidx),len(rt)) )
    p6[newidx] = np.broadcast_to((rng.random(len(newidx))*200 -100)[...,None], (len(newidx),len(rt)) )

    # mutate the old
    p1[passidx]+=np.broadcast_to(rng.normal(0.0,0.80,size=len(passidx))[...,None], (len(passidx),len(rt)) )
    p2[passidx]+=np.broadcast_to(rng.normal(0.0,0.80,size=len(passidx))[...,None], (len(passidx),len(rt)) )
    p3[passidx]+=np.broadcast_to(rng.normal(0.0,0.30,size=len(passidx))[...,None], (len(passidx),len(rt)) )
    p4[passidx]+=np.broadcast_to(rng.normal(0.0,0.80,size=len(passidx))[...,None], (len(passidx),len(rt)) )
    p5[passidx]+=np.broadcast_to(rng.normal(0.0,0.80,size=len(passidx))[...,None], (len(passidx),len(rt)) )
    p6[passidx]+=np.broadcast_to(rng.normal(0.0,0.30,size=len(passidx))[...,None], (len(passidx),len(rt)) )

    stop= time.time()
    if epoch%100==0:
        print(" time:=", stop-start)
        plt.plot(np.log(loss))
        plt.title("log of log of loss for current gen")
        # plt.show()
        plt.draw()
        plt.pause(0.01)
        plt.cla()



losses=np.array(losses)
plt.imshow(np.log(losses))
plt.title("losses")
plt.show()
plt.cla()
plt.fill_between(range(Nepochs), minloss, maxloss, color="blue", alpha=0.1)
plt.plot(meanloss, color="blue")
# plt.plot(selectloss, color="red", alpha=0.5)
plt.title("losses")
plt.show()
plt.pause(2)
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
plt.pause(99)
