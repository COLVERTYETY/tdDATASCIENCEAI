import numpy as np
import random

class individu:
    def __init__(self) -> None:
        self.sum360=set()
        while len(self.sum360)!=5:
            card = (np.random.randint(0,10), np.random.randint(1,5))
            self.sum360.add(card)
        self.sum36=set()
        while len(self.sum36)!=5:
            card = (np.random.randint(0,10), np.random.randint(1,5))
            if card not in self.sum360:
                self.sum36.add(card)
        self.score = -1    
        self.score36 = -1    
        self.score360 = -1    
    
    def mutate(self):
        self.sum360.discard(random.choice(tuple( self.sum360)))
        self.sum36.discard(random.choice(tuple( self.sum36)))
        while len(self.sum360)!=5:
            card = (np.random.randint(0,10), np.random.randint(1,5))
            if card not in self.sum36:
                self.sum360.add(card)
        while len(self.sum36)!=5:
            card = (np.random.randint(0,10), np.random.randint(1,5))
            if card not in self.sum360:
                self.sum36.add(card)

    def crossover(self, other) -> bool:
        if np.random.randint(0,2)==1:
            if other.sum36.isdisjoint(self.sum360):
                self.sum36 = other.sum36.copy()
                return True
            else:
                return False 
        else:
            if other.sum360.isdisjoint(self.sum36):
                self.sum360 = other.sum360.copy()
                return True
            else:
                return False

    def evaluate(self):
        sum360=0.0
        for val, col in self.sum360:
            sum360+=float(val)
        sum36=0.0
        for val, col in self.sum36:
            sum36+=float(val)
        self.score360 = ((sum360 - 360.0)/360.0)**2
        self.score36 = ((sum36 - 36.0)/36.0)**2
        imp360=1.0
        imp36=2.0
        self.score = (imp360*(self.score360) + imp36*(self.score36))/(imp360+imp36)

    def __lt__(self, other):
        if self.score == -1:
            self.evaluate()
        if other.score == -1:
            other.evaluate()
        return self.score<other.score

    def __str__(self):
        text = "360:{ "
        s360 = 0
        for val, col in self.sum360:
            s360+=val
            text+=f"({val}:{col})| "
        text+= "}+= "
        text+=str(s360).zfill(3)
        text+="  36:{ "
        s36 = 0
        for val, col in self.sum36:
            s36+=val
            text+=f"({val}:{col})| "
        text+= "}+= "
        text+=str(s36).zfill(3)
        text+=f"  score= {self.score}"
        return text

