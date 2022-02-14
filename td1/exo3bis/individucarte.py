# import numpy as np
import random

class individu:
    def __init__(self) -> None:
        self.cards = []
        total = [0,1,2,3,4,5,6,7,8,9]
        while len(total)!=0:
            self.cards.append(total.pop(random.randint(0,len(total)-1)))
        self.score = -1       
    
    def mutate(self):
        a = random.randint(0,9)
        b = random.randint(0,9)
        self.cards[a], self.cards[b] = self.cards[b], self.cards[a]


    def crossover(self, other) -> None:
        # for i in range(10):
        #     self.cards[i] = other.cards[self.cards[i]]
        pass

    def evaluate(self):
        sum360=0.0
        for i in self.cards[0:5]:
            sum360+=i
        sum36=0.0
        for j in self.cards[5:10]:
            sum36+=j
        weight36 = 10.0
        weight360 = 1.0
        score360 = (((sum360/360.0)  -1.0)**2)*weight360
        score36 = (((sum36/36.0)  -1.0)**2)*weight36
        self.score = (score360+score36)/(weight360+weight36)
        

    def __lt__(self, other):
        if self.score == -1:
            self.evaluate()
        if other.score == -1:
            other.evaluate()
        return self.score<other.score

    def __str__(self):
        return str(self.cards) + " " + str(self.score)

