from __future__ import annotations
import numpy as np

class caserne:
    gridWidth=12
    thegrid = None
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.score = -1.0

    def crossover(self, other: caserne) -> None:
        if np.random.randint(0,2)==1:
            self.x = other.x
        else:
            self.y = other.y

    def mutate(self,amplitude) ->None:
        rnd = np.random.randint(0,7)
        self.x+=amplitude*np.cos(rnd)
        self.y+=amplitude*np.sin(rnd)
        self.clampcoords()

    def evaluate(self) -> float:
        loss = 0.0
        for i in range(len(caserne.thegrid)):
            for j in range(len(caserne.thegrid[0])):
                loss+= caserne.thegrid[i][j]*np.sqrt(((self.x-i)**2) + ((self.y-j)**2))
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
        return cls(np.random.randint(0,caserne.gridWidth), np.random.randint(0,caserne.gridWidth))