from __future__ import annotations
import random


class Board:

    ncrossover = 4

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
        # for _ in range(Board.ncrossover):
        #     original = random.choice(tuple(self.queens))
        #     self.queens.discard(original)
        #     n = 0
        #     while len(self.queens) != 8 and n!=10:
        #         queen = random.choice(tuple(other.queens))
        #         self.queens.add(queen)
        #         n+=1
        #     if len(self.queens) != 8:
        #         self.queens.add(original)
        total = set().union(self.queens, other.queens)
        # print(total)
        self.queens = set(random.sample(total,8))
            

    def mutate(self, n):
        for _ in range(n):
            queen = random.choice(tuple(self.queens))
            self.queens.discard(queen)
            while len(self.queens) != 8:
                dx = random.randint(-1, 1)
                dy = random.randint(-1, 1)
                coords = ((queen[0] + dx+8)%8, (queen[1] + dy+8)%8)
                self.queens.add(coords)

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
        txt = ''
        for queen in self.queens:
            txt += f'({queen[0]};{queen[1]}),'
        txt += f'score = {self.score}'
        return txt