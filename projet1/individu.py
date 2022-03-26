import random
import math

class indiv():
    def __init__(self) -> None:
        self.genes = []
        for _ in range(6):
            self.genes.append(random.random()*200 - 100)
        self.loss=0
    
    def evaluate(self, t, x,y):
        self.loss+=(x-self.genes[0]*math.sin(self.genes[1]*t+self.genes[2]))**2
        self.loss+=(y-self.genes[3]*math.sin(self.genes[4]*t+self.genes[5]))**2
    
    def mutate(self):
        for i in range(6):
            self.genes[i]+=random.gauss(0,1)
    
    def __lt__(self, other):
        return self.loss < other.loss
    
    def __str__(self):
        return f"{self.loss} "
    
def crossover(a, b):
        n = indiv()
        n.genes=[]
        for i in range(3):
            n.genes.append(a.genes[i])
        for i in range(3,6):
            n.genes.append(b.genes[i])
        return n