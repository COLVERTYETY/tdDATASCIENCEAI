import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import gc
import os, psutil

def main(pid=-1):
    plt.ion()

    data = np.genfromtxt("./position_sample.csv",delimiter=";").T
    # print("unsorted",data)
    idx = np.argsort(data[0])
    rt = np.take(data[0], idx)
    rx = np.take(data[1], idx)  
    ry = np.take(data[2], idx)
    # plt.scatter(rx,ry, color="red")

    Nindiv = 5000
    Nepochs = 3001
    ratio1 = 0.6
    ratio2 = 0.96
    displayrate=200
    nuke=10000
    ratio3 = 0.2
    ratio4 = 0.2

    rng = np.random.default_rng()


    # create random population
    p1 = np.repeat((rng.random(Nindiv)*200 -100)[...,None], len(rt), axis=1)
    p2 = np.repeat((rng.random(Nindiv)*200 -100)[...,None], len(rt), axis=1)
    p3 = np.repeat((rng.random(Nindiv)*200 -100)[...,None], len(rt), axis=1)
    p4 = np.repeat((rng.random(Nindiv)*200 -100)[...,None], len(rt), axis=1)
    p5 = np.repeat((rng.random(Nindiv)*200 -100)[...,None], len(rt), axis=1)
    p6 = np.repeat((rng.random(Nindiv)*200 -100)[...,None], len(rt), axis=1)
    lossx = np.ones(Nindiv)*np.inf
    lossy = np.ones(Nindiv)*np.inf

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
    maxlossx = []
    minlossx = []
    meanlossx = []
    lossesx=[]
    maxlossy = []
    minlossy = []
    meanlossy = []
    lossesy=[]
    total_runtime=0
    for epoch in range(Nepochs):  
        start = time.time()  
        xs = p1*np.sin((p2*RT)+p3)
        ys = p4*np.sin((p5*RT)+p6)
        errorx= abs(xs-RX)#np.power(xs-RX,4)#(RX-xs)**2#(((RX-xs)**2)/RX**2)#np.power(xs-RX,2)  # square penalises more the outliers then small errors
        errory= abs(ys-RY)#np.power(ys-RY,2)#(RY-ys)**2#(((RY-ys)**2)/RY**2)#np.power(ys-RY,2)  # ask yliess
        lossx = np.mean(errorx, axis=1)**4
        lossy = np.mean(errory, axis=1)**4

        # sort by loss 
        # indx = np.argsort(lossx)
        # np.take(lossx, indx, out=lossx)
        # p1 = np.take(p1, indx,axis=0,)#mode="clip")
        # p2 = np.take(p2, indx,axis=0,)#mode="clip")
        # p3 = np.take(p3, indx,axis=0,)#mode="clip")
        # indy = np.argsort(lossy)
        # np.take(lossy, indy, out=lossy)
        # p4 = np.take(p4, indy,axis=0,)#mode="clip")
        # p5 = np.take(p5, indy,axis=0,)#mode="clip")
        # p6 = np.take(p6, indy,axis=0,)#mode="clip")
        # debug
        maxlossx.append(lossx.max())
        maxlossy.append(lossy.max())
        minlossx.append(lossx.min())
        minlossy.append(lossy.min())
        meanlossx.append(lossx.mean())
        meanlossy.append(lossy.mean())
        lossesx.append(lossx)
        lossesy.append(lossy)
        # display the best one
        if epoch%displayrate==0:
            print(f"{pid} {epoch}: {np.sqrt(np.sqrt(np.mean(lossx[:100])))} {np.sqrt(np.sqrt(lossx[0]))} {np.sqrt(np.sqrt(np.mean(lossy[:100])))} {np.sqrt(np.sqrt(lossy[0]))} ",end="")

        # select the best ones
        sx=np.sum(1/lossx)
        sy=np.sum(1/lossy)
        length = int(Nindiv*ratio1)
        if epoch%nuke==0:
            length=int(Nindiv*ratio3)
        selectidx = rng.choice(Nindiv, size=length, replace=False, p=1/lossx/sx)
        selectidy = rng.choice(Nindiv, size=length, replace=False, p=1/lossy/sy)

        #create indexes of the non selected individuals
        nonselectidx = np.ones(Nindiv, dtype=bool)
        nonselectidx[selectidx] = False
        nonselectidx = np.where(nonselectidx)[0]

        nonselectidy = np.ones(Nindiv, dtype=bool)
        nonselectidy[selectidy] = False
        nonselectidy = np.where(nonselectidy)[0]
        #seperate nonselectidx in 2 groups
        rng.shuffle(nonselectidx)
        rng.shuffle(nonselectidy)
        lengthx = int(len(nonselectidx)*ratio2)
        length2x = int(len(nonselectidx)*(1-ratio2))
        lengthy = int(len(nonselectidx)*ratio2)
        length2y = int(len(nonselectidx)*(1-ratio2))
        if epoch%nuke==0:
            lengthx=int(len(nonselectidx)*ratio4)
            length2x=int(len(nonselectidx)*(1-ratio4))
            lengthy=int(len(nonselectidy)*ratio4)
            length2y=int(len(nonselectidy)*(1-ratio4))
        childrenx = np.take(nonselectidx, np.arange(lengthx))
        childreny = np.take(nonselectidy, np.arange(lengthy))
        newindividualsx = np.take(nonselectidx, np.arange(int(length2x),len(nonselectidx)))
        newindividualsy = np.take(nonselectidy, np.arange(int(length2y),len(nonselectidy)))

        #associate each child with a parent
        s=np.sum(1/(selectidx+1))
        parent = rng.choice(selectidx, size=len(childrenx), replace=True,p=1/(selectidx+1)/s)
        p1[childrenx] = p1[parent] + np.repeat(rng.normal(0.0,0.01,size=len(childrenx))[...,None],len(rt), axis=1)
        p2[childrenx] = p2[parent] + np.repeat(rng.normal(0.0,0.01,size=len(childrenx))[...,None],len(rt), axis=1)
        p3[childrenx] = p3[parent] + np.repeat(rng.normal(0.0,0.01,size=len(childrenx))[...,None],len(rt), axis=1)
        parent = rng.choice(selectidx, size=len(childreny), replace=True,p=1/(selectidx+1)/s)
        p4[childreny] = p4[parent] + np.repeat(rng.normal(0.0,0.01,size=len(childreny))[...,None],len(rt), axis=1)
        p5[childreny] = p5[parent] + np.repeat(rng.normal(0.0,0.01,size=len(childreny))[...,None],len(rt), axis=1)
        p6[childreny] = p6[parent] + np.repeat(rng.normal(0.0,0.01,size=len(childreny))[...,None],len(rt), axis=1)

        # ceate new individuals
        p1[newindividualsx] = np.repeat((rng.random(len(newindividualsx))*200 -100)[...,None], len(rt), axis=1)
        p2[newindividualsx] = np.repeat((rng.random(len(newindividualsx))*200 -100)[...,None], len(rt), axis=1)
        p3[newindividualsx] = np.repeat((rng.random(len(newindividualsx))*200 -100)[...,None], len(rt), axis=1)
        p4[newindividualsy] = np.repeat((rng.random(len(newindividualsy))*200 -100)[...,None], len(rt), axis=1)
        p5[newindividualsy] = np.repeat((rng.random(len(newindividualsy))*200 -100)[...,None], len(rt), axis=1)
        p6[newindividualsy] = np.repeat((rng.random(len(newindividualsy))*200 -100)[...,None], len(rt), axis=1)

        # mutate
        p1[selectidx]+=np.repeat(rng.normal(0.0,(Nepochs-epoch)/Nepochs/45,size=len(selectidx))[...,None],len(rt),axis=1)
        p2[selectidx]+=np.repeat(rng.normal(0.0,(Nepochs-epoch)/Nepochs/45,size=len(selectidx))[...,None],len(rt),axis=1)
        p3[selectidx]+=np.repeat(rng.normal(0.0,(Nepochs-epoch)/Nepochs/45,size=len(selectidx))[...,None],len(rt),axis=1)
        p4[selectidy]+=np.repeat(rng.normal(0.0,(Nepochs-epoch)/Nepochs/45,size=len(selectidy))[...,None],len(rt),axis=1)
        p5[selectidy]+=np.repeat(rng.normal(0.0,(Nepochs-epoch)/Nepochs/45,size=len(selectidy))[...,None],len(rt),axis=1)
        p6[selectidy]+=np.repeat(rng.normal(0.0,(Nepochs-epoch)/Nepochs/45,size=len(selectidy))[...,None],len(rt),axis=1)

        # (Nepochs-epoch)/Nepochs/50
        stop= time.time()
        total_runtime+=stop-start
        if epoch%displayrate==0:
            process = psutil.Process(os.getpid())
            print(" time:=", stop-start, "memory:=", process.memory_info().rss/1000000, "Gb")
            if pid==-1:
                pass
                # plt.subplot(1,2,1)
                # plt.cla()
                # # plt.plot(np.log(np.sort(lossx)))
                # plt.subplot(1,2,2)
                # plt.cla()
                # # plt.plot(np.log(np.sort(lossy)))
                # # plt.show()
                # plt.draw()
                # plt.pause(0.001)
                # gc.collect()


    #last sort for disp
    # sort by loss 
    indx = np.argsort(lossx)
    lossx = np.take(lossx, indx)
    p1 = np.take(p1, indx,axis=0)
    p2 = np.take(p2, indx,axis=0)
    p3 = np.take(p3, indx,axis=0)
    indy = np.argsort(lossy)
    lossy = np.take(lossy, indy)
    p4 = np.take(p4, indy,axis=0)
    p5 = np.take(p5, indy,axis=0)
    p6 = np.take(p6, indy,axis=0)
    print("lossx:=", lossx[0])
    print("lossy:=", lossy[0])
    if pid==-1:
        losses=np.array(lossesx)
        plt.ioff()
        plt.imshow(np.log(np.log(losses+1)))
        plt.title("log of log of losses")
        plt.ylabel("generation")
        plt.xlabel("log of log of loss on X")
        plt.legend()
        plt.show()

        plt.cla()
        plt.subplot(1,2,1)
        plt.fill_between(range(1,Nepochs+1), np.log(minlossx), np.log(maxlossx), color="blue", alpha=0.1)
        plt.plot(np.log(meanlossx), color="blue")
        plt.ylabel("log of loss")
        plt.xlabel("generations")
        # plt.ylim((0,10))
        plt.title("losses on X")
        plt.subplot(1,2,2)
        plt.fill_between(range(1,Nepochs+1), np.log(minlossy), np.log(maxlossy), color="blue", alpha=0.1)
        plt.plot(np.log(meanlossy), color="blue")
        plt.title("losses on Y")
        plt.ylabel("log of loss")
        plt.xlabel("generations")
        print("total runtime:=", total_runtime)
        print("avg runtime:=", total_runtime/Nepochs)
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

    np.savetxt(f"./bestindivs/bestindivsplit{time.time()}.txt",np.array([p1[0][0],p2[0][0],p3[0][0],p4[0][0],p5[0][0],p6[0][0]]))
    np.savetxt(f"./runtimes/mytime{time.time()}.txt", np.array([total_runtime, total_runtime/Nepochs, len(rt), lossx[0], lossy[0]]))

if __name__ == '__main__':
    main()
