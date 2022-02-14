import random
from individucarte import individu

Nindiv = 200
keep = 0.4
Nepochs = 1000

if __name__ == '__main__':
    thelist = []
    for _ in range(Nindiv):
        thelist.append(individu())
    
    for epoch in range(Nepochs):
        thelist.sort()
        print(f"{epoch}/{Nepochs}  best indiv:= {thelist[0]}")
        newlist=[]
        for i in range(int(Nindiv*keep)):
            newlist.append(thelist[i])
        for j in range(2,len(newlist)):
            newlist[j].mutate()
        thelist = newlist
        while len(thelist)<Nindiv:
            thelist.append(individu())
        for i in range(2,len(thelist)):
            other = random.choice(thelist[0:len(thelist)//4])
            thelist[i].crossover(other)  

