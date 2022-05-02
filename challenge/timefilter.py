import numpy as np
from matplotlib import pyplot as plt
import os



def main():

    df= []
    totalruntime=[]
    genruntime=[]
    lossX=[]
    lossY=[]
    # for each file in the directory
    for filename in os.listdir("./runtimes"):
        # load indiv to np array
        data = np.genfromtxt("./runtimes/"+filename,delimiter=";")
        df.append(data)
        totalruntime.append(data[0])
        genruntime.append(data[1])
        lossX.append(data[3])
        lossY.append(data[4])

    df = np.array(df)
    print(df)
    nruns = len(df)
    avgtotalruntime = np.mean(totalruntime)
    avggenruntime = np.mean(genruntime)
    avglossX = np.mean(lossX)
    avglossY = np.mean(lossY)
    print("nruns: ",nruns)
    print("population size: ",5000)
    print("Nepochs",1001)
    print("avgT", avgtotalruntime)
    print("avgG", avggenruntime)
    print("avgX", avglossX)
    print("avgY", avglossY)
    plt.hist(totalruntime)
    plt.ylabel("Frequency")
    plt.xlabel("Total runtime (s)")
    plt.title("Total runtime")
    plt.show()
    plt.hist(genruntime)
    plt.ylabel("Frequency")
    plt.xlabel("Generation runtime (s)")
    plt.title("Generation runtime")
    plt.show()
    plt.subplot(2,1,1)
    plt.hist(lossX)
    plt.ylabel("Frequency")
    plt.xlabel("Loss X")
    plt.title("Loss X")
    plt.subplot(2,1,2)
    plt.hist(lossY)
    plt.ylabel("Frequency")
    plt.xlabel("Loss Y")
    plt.title("Loss Y")
    plt.show()


if __name__ == '__main__':
    main()