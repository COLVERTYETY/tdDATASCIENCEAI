import numpy as np
from matplotlib import pyplot as plt
import os



def main():
    plt.ion()

    bestindivs = []

    # load data from "position_sample.csv"
    data = np.genfromtxt("./position_sample.csv",delimiter=";").T
    # print("unsorted",data)
    idx = np.argsort(data[0])
    rt = np.take(data[0], idx)
    rx = np.take(data[1], idx)
    ry = np.take(data[2], idx)


    # for each file in the directory
    for filename in os.listdir("./bestindivs"):
        # load indiv to np array
        indiv = np.genfromtxt("./bestindivs/"+filename,delimiter=";").T
        loss=0
        for i in range(data.shape[1]):
            # print(p[0],p[1],p[2])
            x = indiv[0]*np.sin((indiv[1]*rt[i])+indiv[2])
            y = indiv[3]*np.sin((indiv[4]*rt[i])+indiv[5])
            loss += np.power(x-rx[i],2)+np.power(y-ry[i],2)
            bestindivs.append((indiv, loss, filename))
            plt.scatter(x,y, color="blue")
            plt.scatter(rx[i],ry[i], color="red")
        os.remove("./bestindivs/"+filename)
        plt.draw()
        plt.title("loss: "+str(loss))
        plt.pause(0.01)
        plt.clf()

    # sort by fitness
    bestindivs = sorted(bestindivs, key=lambda x: x[1])
    s = sum([x[1] for x in bestindivs])
    mean = s/len(bestindivs)
    #calculate std
    std = 0
    for x in bestindivs:
        std += (x[1]-mean)**2
    std = np.sqrt(std/len(bestindivs))
    print("mean: "+str(mean))
    print("std: "+str(std))
    plt.hist([x[1] for x in bestindivs])
    plt.title("best loss is: "+str(bestindivs[0][1])+"\nsecond best:"+str(bestindivs[1][1]) +"\nmean : "+str(mean)+"\nstd: "+str(std))
    plt.show()
    plt.pause(1)
    np.savetxt("THEVERYBEST.csv",bestindivs[0][0],delimiter=";")
    np.savetxt("./bestindivs/LASTBEST.txt",bestindivs[0][0])

if __name__ == '__main__':
    main()