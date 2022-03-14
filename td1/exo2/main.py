"""
Cette implémentation à été développé lors du cours de Datascience,
vous trouverez les fonctions de mutations, selection, croisement dans board.py
"""

from board import Board
import random
from multiprocessing import Pool

def play(poolN):

    keep = 0.2
    popSize = 300
    nepoch = 6000

    boards: list = []
    for _ in range(popSize):
        boards.append(Board())

    for epoch in range(nepoch):
        boards.sort()
        # calculate variance et average
        average = 0
        for board in boards:
            average += board.score
        average /= popSize
        variance = 0
        for board in boards:
            variance += (board.score - average)**2
        variance /= popSize
        if epoch%100 == 0:
            print("{}|Epoch: {}|avg: {}|variance: {}|best: {}|2nd: {}".format(poolN,str(epoch).zfill(4), str(round(average, 1)).zfill(4), str(round(variance,1)).zfill(4), boards[0], boards[1]))
        # print(f"epoch : {epoch} | best : {boards[0]}, second : {boards[1]}")

        futureBoards = []
        futureBoards.append(boards[0])

        for i in range(10):
            baby = boards[0].copy()
            baby.mutate(1)
            futureBoards.append(baby)

        for i in range(11,int(max(epoch/nepoch, 0.2)*len(boards))):
            # l = len(futureBoards)
            # while len(futureBoards) != l+1:
            newBoard = boards[i]
            newBoard.mutate(1)
            futureBoards.append(newBoard)
            if i % 2 == 0 or epoch > 2000:
                futureBoards[i].crossover(random.choice(futureBoards))
                # futureBoards[i].crossover(boards[0])
        

        while len(futureBoards) != popSize:
            futureBoards.append(Board())

        boards = futureBoards.copy()

    map(print, boards)

if __name__ == '__main__':
    with Pool(processes=6) as pool:
        pool.map(play, range(6))

