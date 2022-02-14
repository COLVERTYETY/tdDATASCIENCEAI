from board import Board
import random
if __name__ == '__main__':

    keep = 0.6
    popSize = 100

    boards: list = []
    for _ in range(popSize):
        boards.append(Board())

    for epoch in range(1000):
        boards.sort()
        print(f"epoch : {epoch} | best : {boards[0]}, second : {boards[1]}")

        futureBoards = []
        futureBoards.append(boards[0])

        for i in range(1,int(keep*len(boards))):
            futureBoards.append(boards[i].mutate(1))
            futureBoards[i].crossover(random.choice(futureBoards))

        while len(futureBoards) != popSize:
            futureBoards.append(Board())

        boards = futureBoards.copy()

    map(print, boards)
        