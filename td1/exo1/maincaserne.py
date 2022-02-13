from caserne import caserne
import numpy as np

Nindiv = 100

epochs = 100

grid = [
    [5, 2, 4, 8, 9, 0, 3, 3, 8, 7],
    [5, 5, 3, 4, 4, 6, 4, 1, 9, 1],
    [4, 1, 2, 1, 3, 8, 7, 8, 9, 1],
    [1, 7, 1, 6, 9, 3, 1, 9, 6, 9],
    [4, 7, 4, 9, 9, 8, 6, 5, 4, 2],
    [7, 5, 8, 2, 5, 2, 3, 9, 8, 2],
    [1, 4, 0, 6, 8, 4, 0, 1, 2, 1],
    [1, 5, 2, 1, 2, 8, 3, 3, 6, 2],
    [4, 5, 9, 6, 3, 9, 7, 6, 5, 10],
    [0, 6, 2, 8, 7, 1, 2, 1, 5, 3]
]

def drawGrid(agrid):
    for i in range(len(agrid)):
        print(grid[i])
            
if __name__ == '__main__':
    drawGrid(grid)
    caserne.thegrid = grid
    caserne.gridWidth = len(grid)
    thelist = []
    for i in range(Nindiv):
        thelist.append(caserne.Random())
    
    for nepoch in range(epochs):
        thelist.sort(reverse=True)
        print(f'{nepoch}/{epochs}:  best individual:= {thelist[0]}    second best:= {thelist[1]}')
        ## turney selection
        newlist = []
        # the first passes for free
        newlist.append(thelist[0])
        del thelist[0]
        for i in range((int)(Nindiv*0.8)):
            first = np.random.randint(0,len(thelist))
            second = np.random.randint(0,len(thelist))
            if thelist[first]>thelist[second]:
                newlist.append(thelist[first])
                del thelist[first]
            else:
                newlist.append(thelist[second])
                del thelist[second]
        thelist=[]
        thelist.append(newlist[0])
        for i in range(1,len(newlist)):
            newlist[i].mutate(1)
            iother = np.random.randint(0,len(newlist))
            newlist[i].crossover(newlist[iother])
            thelist.append(newlist[i])
        newlist=[]
        while len(thelist)<Nindiv:
            thelist.append(caserne.Random())
    
    print("############################################################")
    print("OVER")
    print("all:")
    thelist.sort(reverse=True)
    for ind in thelist:
        print(ind)
    