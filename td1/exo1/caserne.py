from __future__ import annotations
# import numpy as np
import random
import math
class caserne:
    gridWidth=12
    thegrid = None
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.score = -1.0

    def crossover(self, other: caserne) -> None:
        if random.randint(0,1)==1:
            self.x = other.x
        else:
            self.y = other.y

    def mutate(self,amplitude) ->None:
        rnd = random.randint(0,6)
        self.x+=amplitude*math.cos(rnd)
        self.y+=amplitude*math.sin(rnd)
        self.clampcoords()

    def evaluate(self) -> float:
        loss = 0.0
        for i in range(len(caserne.thegrid)):
            for j in range(len(caserne.thegrid[0])):
                loss+= caserne.thegrid[i][j]*math.sqrt(((self.x-i)**2) + ((self.y-j)**2))
        self.score = loss
        return loss

    def clampcoords(self):
        self.x = (int)(self.x)
        self.y = (int)(self.y)
        if self.x>=caserne.gridWidth:
            self.x = caserne.gridWidth-1
        elif self.x<0:
            self.x = 0
        if self.y>=caserne.gridWidth:
            self.y = caserne.gridWidth-1
        elif self.y<0:
            self.y = 0

    def __lt__(self, other: caserne) -> int:
        if self.score==-1.0:
            self.evaluate()
        if other.score==-1:
            other.evaluate()
        return self.score>other.score 

    def __str__(self):
        return f'({self.x};{self.y}) -> {self.score}'

    @classmethod
    def Random(cls) -> caserne:
        return cls(random.randint(0,caserne.gridWidth-1), random.randint(0,caserne.gridWidth-1))