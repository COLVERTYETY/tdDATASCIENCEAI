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
Nepochs = 10011
ratio1 = 0.6
ratio2 = 0.95
displayrate=100

rng = np.random.default_rng()


# create random population
p1 = np.broadcast_to((rng.normal(-1.318790093926389773e+01,3,size=Nindiv))[...,None],(Nindiv,len(rt)) )
p2 = np.broadcast_to((rng.normal(2.110149765178334391e+01,3,size=Nindiv))[...,None],(Nindiv,len(rt)) )
p3 = np.broadcast_to((rng.normal(-7.025977695418418989e+01,3,size=Nindiv))[...,None],(Nindiv,len(rt)) )
p4 = np.broadcast_to((rng.normal(-2.289704910332054411e+01,3,size=Nindiv))[...,None],(Nindiv,len(rt)) )
p5 = np.broadcast_to((rng.normal(4.109781425940588662e+01,3,size=Nindiv))[...,None],(Nindiv,len(rt)) )
p6 = np.broadcast_to((rng.normal(-3.784734245773484673e+01,3,size=Nindiv))[...,None],(Nindiv,len(rt)) )
loss = np.ones(Nindiv)*np.inf

#shape data to population
RT = np.tile(rt, (Nindiv,1))
RX = np.tile(rx, (Nindiv,1))
RY = np.tile(ry, (Nindiv,1))

# prealocate memory
errorx=np.zeros_like(p1)
errory=np.zeros_like(p1)
xs=np.zeros_like(p1)
ys=np.zeros_like(p1)

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
    errorx= np.power(xs-RX,2)#(RX-xs)**2#(((RX-xs)**2)/RX**2)#np.power(xs-RX,2)  # square penalises more the outliers then small errors
    # a = ((xs-RX)**2)
    # (xs-RX)**2
    # print(sum(sum(a-errorx)))
    #(ys-RY)**2
    errory= np.power(ys-RY,2)#(RY-ys)**2#(((RY-ys)**2)/RY**2)#np.power(ys-RY,2)  # ask yliess
    loss = np.mean(errorx, axis=1) + np.mean(errory, axis=1)

    # sort by loss 
    indx = np.argsort(loss)
    np.take(loss, indx, out=loss)
    p1 = np.take(p1, indx,axis=0,)#mode="clip")
    p2 = np.take(p2, indx,axis=0,)#mode="clip")
    p3 = np.take(p3, indx,axis=0,)#mode="clip")
    p4 = np.take(p4, indx,axis=0,)#mode="clip")
    p5 = np.take(p5, indx,axis=0,)#mode="clip")
    p6 = np.take(p6, indx,axis=0,)#mode="clip")
    # debug
    maxloss.append(loss.max())
    minloss.append(loss.min())
    meanloss.append(loss.mean())
    losses.append(loss)
    # display the best one
    if epoch%displayrate==0:
        print(f"{epoch}: {np.mean(loss[:100])} {loss[0]} ",end="")

    # select the best ones
    s=np.sum(1/loss)
    selectidx = rng.choice(Nindiv, size=int(Nindiv*ratio1), replace=False, p=1/loss/s)

    #create indexes of the non selected individuals
    nonselectidx = np.ones(Nindiv, dtype=bool)
    nonselectidx[selectidx] = False
    nonselectidx = np.where(nonselectidx)[0]
    
    #seperate nonselectidx in 2 groups
    rng.shuffle(nonselectidx)
    children = np.take(nonselectidx, np.arange(int(len(nonselectidx)*ratio2)))
    newindividuals = np.take(nonselectidx, np.arange(int(len(nonselectidx)*(1-ratio2)),len(nonselectidx)))

    #associate each child with a parent
    s=np.sum(1/(selectidx+1))
    parent = rng.choice(selectidx, size=len(children), replace=True,p=1/(selectidx+1)/s)
    p1[children] = p1[parent] + np.broadcast_to(rng.normal(0.0,0.001,size=len(children))[...,None], (len(children),len(rt)) )
    p2[children] = p2[parent] + np.broadcast_to(rng.normal(0.0,0.001,size=len(children))[...,None], (len(children),len(rt)) )
    p3[children] = p3[parent] + np.broadcast_to(rng.normal(0.0,0.001,size=len(children))[...,None], (len(children),len(rt)) )
    parent = rng.choice(selectidx, size=len(children), replace=True,p=1/(selectidx+1)/s)
    p4[children] = p4[parent] + np.broadcast_to(rng.normal(0.0,0.001,size=len(children))[...,None], (len(children),len(rt)) )
    p5[children] = p5[parent] + np.broadcast_to(rng.normal(0.0,0.001,size=len(children))[...,None], (len(children),len(rt)) )
    p6[children] = p6[parent] + np.broadcast_to(rng.normal(0.0,0.001,size=len(children))[...,None], (len(children),len(rt)) )

    # ceate new individuals
    p1[newindividuals] = np.broadcast_to((rng.normal(-1.318790093926389773e+01,3,size=len(newindividuals)))[...,None],(len(newindividuals),len(rt)))
    p2[newindividuals] = np.broadcast_to((rng.normal(2.110149765178334391e+01,3,size=len(newindividuals)))[...,None],( len(newindividuals),len(rt)) )
    p3[newindividuals] = np.broadcast_to((rng.normal(-7.025977695418418989e+01,3,size=len(newindividuals)))[...,None],(len(newindividuals),len(rt)))
    p4[newindividuals] = np.broadcast_to((rng.normal(-2.289704910332054411e+01,3,size=len(newindividuals)))[...,None],(len(newindividuals),len(rt)))
    p5[newindividuals] = np.broadcast_to((rng.normal(4.109781425940588662e+01,3,size=len(newindividuals)))[...,None],( len(newindividuals),len(rt)) )
    p6[newindividuals] = np.broadcast_to((rng.normal(-3.784734245773484673e+01,3,size=len(newindividuals)))[...,None],(len(newindividuals),len(rt)))

    # mutate
    p1[selectidx]+=np.broadcast_to(rng.normal(0.0,(Nepochs-epoch)/Nepochs/400,size=len(selectidx))[...,None], (len(selectidx),len(rt)) )
    p2[selectidx]+=np.broadcast_to(rng.normal(0.0,(Nepochs-epoch)/Nepochs/400,size=len(selectidx))[...,None], (len(selectidx),len(rt)) )
    p3[selectidx]+=np.broadcast_to(rng.normal(0.0,(Nepochs-epoch)/Nepochs/400,size=len(selectidx))[...,None], (len(selectidx),len(rt)) )
    p4[selectidx]+=np.broadcast_to(rng.normal(0.0,(Nepochs-epoch)/Nepochs/400,size=len(selectidx))[...,None], (len(selectidx),len(rt)) )
    p5[selectidx]+=np.broadcast_to(rng.normal(0.0,(Nepochs-epoch)/Nepochs/400,size=len(selectidx))[...,None], (len(selectidx),len(rt)) )
    p6[selectidx]+=np.broadcast_to(rng.normal(0.0,(Nepochs-epoch)/Nepochs/400,size=len(selectidx))[...,None], (len(selectidx),len(rt)) )
    
    # (Nepochs-epoch)/Nepochs/50
    stop= time.time()
    if epoch%displayrate==0:
        print(" time:=", stop-start)
        plt.plot(np.log(loss))
        # plt.show()
        plt.draw()
        plt.pause(0.001)
        plt.cla()


#last sort for disp
# sort by loss 
indx = np.argsort(loss)
loss = np.take(loss, indx)
p1 = np.take(p1, indx,axis=0)
p2 = np.take(p2, indx,axis=0)
p3 = np.take(p3, indx,axis=0)
p4 = np.take(p4, indx,axis=0)
p5 = np.take(p5, indx,axis=0)
p6 = np.take(p6, indx,axis=0)

losses=np.array(losses)
plt.ioff()
plt.imshow(np.log(np.log(losses+1)))
plt.title("log of log of losses")
plt.show()

plt.cla()
plt.fill_between(range(1,Nepochs+1), np.log(minloss), np.log(maxloss), color="blue", alpha=0.1)
plt.plot(np.log(meanloss), color="blue")
# plt.ylim((0,10))
plt.title("losses")
plt.show()
plt.cla()
for i, txt in enumerate(rt):
    plt.annotate(txt, (rx[i], ry[i]))
plt.scatter(rx,ry, color="red", label=rt)
x=[]
y=[]
for t in rt:
    a=p1[0][0]*np.sin((p2[0][0]*t)+p3[0][0])
    x.append(a)
    b=p4[0][0]*np.sin((p5[0][0]*t)+p6[0][0])
    y.append(b)
plt.scatter(x,y, color="blue")
plt.title("best fit")
plt.show()

np.savetxt("bestindiv.txt",np.array([p1[0][0],p2[0][0],p3[0][0],p4[0][0],p5[0][0],p6[0][0]]))
