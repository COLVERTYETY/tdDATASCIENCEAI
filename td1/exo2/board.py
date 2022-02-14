from __future__ import annotations
import random


class Board:

    ncrossover = 2

    def __init__(self) -> None:
        self.queens = set()
        self.score = None
        while len(self.queens) != 8:
            coord = (random.randint(0, 7), random.randint(0,7))
            self.queens.add(coord)

    def evaluates(self) -> float:
        # calculate how many conflicts on the board
        loss = 0
        for queen1 in self.queens:
            for queen2 in self.queens:
                if queen1 != queen2:
                    # line
                    if(queen1[0] == queen2[0]):
                        loss+=1
                    # column
                    elif queen1[1] == queen2[1]:
                        loss+=1
                    # diagonals
                    elif abs(queen1[0] - queen2[0]) == abs(queen1[1] - queen2[1]):
                        loss+=1
        self.score = loss

    def crossover(self, other) -> None:
        for _ in range(Board.ncrossover):
            self.queens.discard(random.choice(self.queens))
            while len(self.queens) != 8:
                queen = random.choice(other.queens)
                self.queens.add(queen)

    def mutate(self, n):
        for _ in range(n):
            queen = random.choice(self.queens)
            self.queens.discard(queen)
            dx = random.randint(-1, 1)
            dy = random.randint(-1, 1)
            queen[0] += dx
            queen[1] += dy
            self.queens.add(queen)

    def __lt__(self, other: Board) -> bool:
        if self.score == None:
            self.evaluates()
        if other.score == None:
            other.evaluates()
        return self.score < other.score

        
            
        
    def __str__(self) -> str:
        txt = ''
        for queen in self.queens:
            txt += f'({queen[0]};{queen[1]}), '
        txt += f'score = {self.score}'
        return txt