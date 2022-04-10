import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

def main(pid=-1):
    plt.ion()

    data = np.genfromtxt("./position_sample.csv",delimiter=";").T
    # print("unsorted",data)
    idx = np.argsort(data[0])
    rt = np.take(data[0], idx)
    rx = np.take(data[1], idx)  
    ry = np.take(data[2], idx)
    # plt.scatter(rx,ry, color="red")

    Nindiv = 25000
    Nepochs = 201
    ratio1 = 0.3
    ratio2 = 0.8
    displayrate=100

    rng = np.random.default_rng()


    # create random population
    p1 = rng.uniform(-100,100,size=Nindiv)
    p2 = rng.uniform(-100,100,size=Nindiv)
    p3 = rng.uniform(-100,100,size=Nindiv)
    p4 = rng.uniform(-100,100,size=Nindiv)
    p5 = rng.uniform(-100,100,size=Nindiv)
    p6 = rng.uniform(-100,100,size=Nindiv)
    lossx = np.ones(Nindiv)*np.inf
    lossy = np.ones(Nindiv)*np.inf

    #shape data to population
    RT = rt.T
    RX = rx.T
    RY = ry.T

    # debug
    maxlossx = []
    minlossx = []
    meanlossx = []
    maxlossy = []
    minlossy = []
    meanlossy = []
    total_runtime=0

    rejection_mask = np.ones(Nindiv, dtype=bool)
    indexes = np.arange(Nindiv)

    for epoch in range(Nepochs):  
        start = time.time()  
        # evaluate
        xs = p1[:,None]*np.sin((p2[:,None]*RT[None,:])+p3[:,None])
        ys = p4[:,None]*np.sin((p5[:,None]*RT[None,:])+p6[:,None])
        lossx = np.sum((xs-RX[None,:])**2, axis=1)
        lossy = np.sum((ys-RY[None,:])**2, axis=1)
        
        # debug
        if pid==-1:
            maxlossx.append(lossx.max())
            maxlossy.append(lossy.max())
            minlossx.append(lossx.min())
            minlossy.append(lossy.min())
            meanlossx.append(lossx.mean())
            meanlossy.append(lossy.mean())

        # display the best one
        if epoch%displayrate==0:
            print(f"{pid} {epoch}: {np.min(lossx)} {np.min(lossy)} ",end="")
        
        length = int(Nindiv * ratio1)
        keys_x = np.argsort(lossx)
        keys_y = np.argsort(lossy)
        selectidx = keys_x[:length]
        selectidy = keys_y[:length]

        #create indexes of the non selected individuals
        rejection_mask.fill(True)
        rejection_mask[selectidx] = False
        x_rejection_idx = indexes[rejection_mask]
        lengthx = int(len(x_rejection_idx)*ratio2)
        childrenx = x_rejection_idx[:lengthx]
        newindividualsx = x_rejection_idx[lengthx:]    

        rejection_mask.fill(True)
        rejection_mask[selectidy] = False
        y_rejection_idx = indexes[rejection_mask]
        lengthy = int(len(y_rejection_idx)*ratio2)
        childreny = y_rejection_idx[:lengthy]
        newindividualsy = y_rejection_idx[lengthy:]

        #associate each child with a parent
        s2= (lossx)[selectidx]
        s=np.sum(1/s2)
        parent = rng.choice(selectidx, size=len(childrenx), replace=True,p=(1/s2/s))
        p1[childrenx] = p1[parent] + rng.normal(0.0,(Nepochs-epoch)/Nepochs/400,size=len(childrenx))
        p2[childrenx] = p2[parent] + rng.normal(0.0,(Nepochs-epoch)/Nepochs/400,size=len(childrenx))
        p3[childrenx] = p3[parent] + rng.normal(0.0,(Nepochs-epoch)/Nepochs/800,size=len(childrenx))
        s2 = lossy[selectidy]
        s=np.sum(1/s2)
        parent = rng.choice(selectidy, size=len(childreny), replace=True,p=(1/s2/s))
        p4[childreny] = p4[parent] + rng.normal(0.0,(Nepochs-epoch)/Nepochs/400,size=len(childreny))
        p5[childreny] = p5[parent] + rng.normal(0.0,(Nepochs-epoch)/Nepochs/400,size=len(childreny))
        p6[childreny] = p6[parent] + rng.normal(0.0,(Nepochs-epoch)/Nepochs/800,size=len(childreny))

        # ceate new individuals
        p1[newindividualsx] = rng.uniform(-100,100,size=len(newindividualsx))
        p2[newindividualsx] = rng.uniform(-100,100,size=len(newindividualsx))
        p3[newindividualsx] = rng.uniform(-100,100,size=len(newindividualsx))
        p4[newindividualsy] = rng.uniform(-100,100,size=len(newindividualsy))
        p5[newindividualsy] = rng.uniform(-100,100,size=len(newindividualsy))
        p6[newindividualsy] = rng.uniform(-100,100,size=len(newindividualsy))

        # mutate
        p1[selectidx]+=rng.normal(0.0,(Nepochs-epoch)/Nepochs/30,size=len(selectidx))
        p2[selectidx]+=rng.normal(0.0,(Nepochs-epoch)/Nepochs/30,size=len(selectidx))
        p3[selectidx]+=rng.normal(0.0,(Nepochs-epoch)/Nepochs/60,size=len(selectidx))
        p4[selectidy]+=rng.normal(0.0,(Nepochs-epoch)/Nepochs/30,size=len(selectidy))
        p5[selectidy]+=rng.normal(0.0,(Nepochs-epoch)/Nepochs/30,size=len(selectidy))
        p6[selectidy]+=rng.normal(0.0,(Nepochs-epoch)/Nepochs/60,size=len(selectidy))

        stop= time.time()
        total_runtime+=stop-start
        if epoch%displayrate==0:
            print(" time:=", stop-start)


    #last sort for disp
    # sort by loss 
    indx = np.argsort(lossx)
    lossx = np.take(lossx, indx)
    p1 = np.take(p1, indx)
    p2 = np.take(p2, indx)
    p3 = np.take(p3, indx)
    indy = np.argsort(lossy)
    lossy = np.take(lossy, indy)
    p4 = np.take(p4, indy)
    p5 = np.take(p5, indy)
    p6 = np.take(p6, indy)
    print("lossx:=", lossx[0])
    print("lossy:=", lossy[0])
    if pid==-1:
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
            a=p1[0]*np.sin((p2[0]*t)+p3[0])
            x.append(a)
            b=p4[0]*np.sin((p5[0]*t)+p6[0])
            y.append(b)
        plt.scatter(x,y, color="blue")
        plt.title("best fit")
        plt.show()
    print("best")
    print("p1:=", p1[0])
    print("p2:=", p2[0])
    print("p3:=", p3[0])
    print("p4:=", p4[0])
    print("p5:=", p5[0])
    print("p6:=", p6[0])
    np.savetxt(f"./bestindivs/bestindivsplit{time.time()}.txt",np.array([p1[0],p2[0],p3[0],p4[0],p5[0],p6[0]]))
    np.savetxt(f"./runtimes/mytime{time.time()}.txt", np.array([total_runtime, total_runtime/Nepochs, len(rt), lossx[0], lossy[0]]))

if __name__ == '__main__':
    main()
