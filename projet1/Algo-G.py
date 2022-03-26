from lib2to3.pgen2.pgen import generate_grammar
from matplotlib.pyplot import new_figure_manager
import matplotlib.pyplot as plt
from individu import indiv, crossover
import random
import numpy as np
import math

f = open('position_sample.csv','r')
data = []
next(f)
for line in f:
    line = line.replace('\n','')
    data.append(list(map(float,line.split(';'))))
f.close()

Nindiv = 10000
ratio1 = 0.2
ratio2 = 0.8
generationmax=50


population=[]
for _ in range(Nindiv):
    population.append(indiv())

for gen in range(generationmax):
    for i in population:
        i.loss=0
        for p in data:
            i.evaluate(*p)
    population.sort()
    print(f"{gen}/{generationmax}: "+str(population[0]))
    total = sum([1/i.loss for i in population])
    population = list(np.random.choice(population, (int)(ratio1*Nindiv), p=[(1/i.loss)/total for i in population]))
    newguys = []
    for _ in range((int)((Nindiv-len(population))*ratio2)):
        #print(len(population))
        newguys.append(crossover(random.choice(population),random.choice(population)))
    population.extend(newguys)
    for i in population[:(int)(ratio1*Nindiv)]:
        i.mutate()
    while len(population)<Nindiv:
        population.append(indiv())
    
king = sorted(population)[0]
x = []
y = []
for t in range(0,4000):
    x.append(king.genes[0]*math.sin(king.genes[1]*(t/1000)+king.genes[2]))
    y.append(king.genes[3]*math.sin(king.genes[4]*(t/1000)+king.genes[5]))

plt.plot(x,y)

#plt.scatter(x,y)
plt.show()

# print(data)