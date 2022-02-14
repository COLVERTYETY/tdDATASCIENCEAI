from __future__ import annotations
import random


class Board:

    ncrossover = 4

    def __init__(self) -> None:
        self.queens = []
        allposiible = [1,2,3,4,5,6,7,8]
        while len(allposiible)!=0:
            x = random.choice(allposiible)
            allposiible.remove(x)
            self.queens.append(x)
        self.score = None

    def evaluates(self) -> float:
        # calculate how many conflicts on the board
        loss = 0
        for i in range(len(self.queens)):
            for j in range(len(self.queens)):
                if i != j:
                    # diagonals
                    if abs(i - j) == abs(self.queens[i] - self.queens[j]):
                        loss+=1
        self.score = loss

    def crossover(self, other) -> None:
        newqueens = []
        for i in range(Board.ncrossover):
            newqueens.append(self.queens[i])
        for i in range(Board.ncrossover, len(self.queens)):
            newqueens.append(other.queens[i])
        self.queens = newqueens
            

    def mutate(self, n):
        for _ in range(n):
            a = random.randint(0,len(self.queens)-1)
            b = random.randint(0,len(self.queens)-1)
            self.queens[a], self.queens[b] = self.queens[b], self.queens[a]


    def __lt__(self, other: Board) -> bool:
        if self.score == None:
            self.evaluates()
        if other.score == None:
            other.evaluates()
        return self.score < other.score

    def copy(self) -> Board:
        board = Board()
        board.queens = self.queens.copy()
        board.score = self.score
        return board

        
            
        
    def __str__(self) -> str:
        txt = '('
        for queen in self.queens:
            txt += f'{queen};'
        txt += f') score = {self.score}'
        return txt