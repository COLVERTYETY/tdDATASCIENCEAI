from dataclasses import replace
import numpy as np
import cv2
from cv2 import matchTemplate as cv2m
import time
from numba import jit


cneighbour = np.array([[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]])
# cneighbour = np.array([[-1,1,0,-1,1,0,-1,1],[-1,-1,-1,0,0,1,1,1]])
seq = np.array([1,1,1,1,1])
diag = np.array([[1,0,0,0,0],
                [0,1,0,0,0],
                [0,0,1,0,0],
                [0,0,0,1,0],
                [0,0,0,0,1]])
otherdiag = np.array([  [0,0,0,0,1],
                        [0,0,0,1,0],
                        [0,0,1,0,0],
                        [0,1,0,0,0],
                        [1,0,0,0,0]])
eye = np.array([[0,1,0],[1,1,1],[0,1,0]])
cross = np.array([[1,0,1],[0,1,0],[1,0,1]])
block = np.array([[1,1,1],[1,1,1],[1,1,1]])
eye3 = np.array([[0,0,0,0,0],
                [0,0,1,0,0],
                [0,1,1,1,0],
                [0,0,1,0,0],
                [0,0,0,0,0]])
eye3_mask = np.array([[0,0,1,0,0],
                        [0,0,1,0,0],
                        [1,1,1,1,1],
                        [0,0,1,0,0],
                        [0,0,1,0,0]])
cross3 = np.array([[0,0,0,0,0],
                    [0,1,0,1,0],
                    [0,0,1,0,0],
                    [0,1,0,1,0],
                    [0,0,0,0,0]])
cross3_mask = np.array([[1,0,0,0,1],
                    [0,1,0,1,0],
                    [0,0,1,0,0],
                    [0,1,0,1,0],
                    [1,0,0,0,1]])
line = np.array([0,1,1,1,0])
line4 = np.array([0,1,1,1,1,0])
line4_diag = np.array([[0,0,0,0,0,0],
                        [0,1,0,0,0,0],
                        [0,0,1,0,0,0],
                        [0,0,0,1,0,0],
                        [0,0,0,0,1,0],
                        [0,0,0,0,0,0]])
line4_otherdiag = np.array([[0,0,0,0,0,0],
                        [0,0,0,0,1,0],
                        [0,0,0,1,0,0],
                        [0,0,1,0,0,0],
                        [0,1,0,0,0,0],
                        [0,0,0,0,0,0]])
line4_diag_mask = np.array([[1,0,0,0,0,0],
                        [0,1,0,0,0,0],
                        [0,0,1,0,0,0],
                        [0,0,0,1,0,0],
                        [0,0,0,0,1,0],
                        [0,0,0,0,0,1]])
line4_otherdiag_mask = np.array([[0,0,0,0,0,1],
                        [0,0,0,0,1,0],
                        [0,0,0,1,0,0],
                        [0,0,1,0,0,0],
                        [0,1,0,0,0,0],
                        [1,0,0,0,0,0]])
line_diag = np.array([[0,0,0,0,0],
                    [0,1,0,0,0],
                    [0,0,1,0,0],
                    [0,0,0,1,0],
                    [0,0,0,0,0]])
line_otherdiag = np.array([  [0,0,0,0,0],
                        [0,0,0,1,0],
                        [0,0,1,0,0],
                        [0,1,0,0,0],
                        [0,0,0,0,0]])
# diag_mask = np.array([[

# def __init__(self, coords, parent, player, depth):
#     self.coords: np.ndarray = coords
#     self.parent: Node = parent
#     self.player:int = player
#     self.depth:int = depth
#     self.children = []
#     self.wins:int = 0
#     self.plays:int = 0

# @property
# def score(self):
#     return self.wins/self.plays

# def selection(self, board, neighbours):
#     # print(f"selection for {self.coords}")
#     if self.parent:
#         play(self.coords,self.player,board,neighbours)
#     winner = self.get_winner(board)
#     if winner != 0 or self.depth == 0:
#         self.backpropagate(winner)
#     elif len(self.children) == 0:
#         self.expand(board,neighbours)
#         for(child) in self.children:
#             child.simulate(board,neighbours)
#     else:
#         child = self.select_child()
#         child.selection(board,neighbours)
#     if self.parent:
#         unplay(self.coords,self.player,board,neighbours)

# def select_child(self):
#     return max(self.children, key=lambda x: x.score)

# def expand(self,board,neighbours):
#     idx = np.where(board == 0)
#     idxn = np.argmax(neighbours[idx])
#     for i in range(idxn.shape[0]):
#         self.children.append(Node(idxn[i],self,self.player*-1,self.depth-1))

# def simulate(self,board, neighbours):
#     board_=board.copy()
#     player = -self.player
#     neighbours_ = neighbours.copy()
#     depth = self.depth
#     while depth > 0:
#         idx = np.where(board_ == 0)
#         idxn = np.argmax(neighbours_[idx])[0]
#         board_[[idxn]] = player
#         player = -player
#         depth -= 1
#         winner = self.get_winner(board_)
#         if winner != 0:
#             return winner
#     return 0

# def backpropagate(self, winner):
#     self.plays += 1
#     if winner == self.player:
#         self.wins += 1
#     if self.parent:
#         self.parent.backpropagate(winner)

# def __str__(self):
#     return f"Node: {self.coords} {self.player} {self.depth}"

# def __repr__(self):
#     return self.__str__()

@staticmethod
def mcts(board, neighbours, root):
    start = time.time()
    iteration=0
    while time.time() - start < 4:
        iteration += 1
        root.selection(board,neighbours)
    print(f"Iterations: {iteration}")
    return tuple(root.select_child().coords)

@staticmethod
def play(coords,player,board, neighbours):
    board[coords] = player
    neighbours[cneighbour+ coords] +=1

@staticmethod
def unplay(coords,board, neighbours):
    board[coords] = 0
    neighbours[cneighbour+ coords] -=1


def get_winner(board):
    # check the row
    if find_sequence(board, seq)>0:
        return 1
    # check the column
    if find_sequence(board.T, seq)>0:
        return 1
    # check the diagonal
    if find_sequence(board, diag, diag.astype('uint8'))>0:
        return 1
    # check the diagonal
    if find_sequence(board, otherdiag, otherdiag.astype('uint8'))>0:
        return 1
    ## now do the same for teh other player
    if find_sequence(board, seq*-1)>0:
        return -1
    if find_sequence(board.T, seq*-1)>0:
        return -1
    if find_sequence(board, diag*-1,diag.astype('uint8'))>0:
        return -1
    if find_sequence(board, otherdiag*-1,otherdiag.astype('uint8'))>0:
        return -1
    return 0


def find_sequence(arr, seq,mask_=None):
    arr_=arr+2
    seq_=seq+2
    S = cv2m(arr_.astype('uint8'),seq_.astype('uint8'),method=cv2.TM_SQDIFF,mask=mask_)
    idx = np.where(S == 0)[0]
    return idx.shape[0]

# def evaluate_convolve(board,player, x, y):
#     col = board[max(0, x-4):min(15, x+5), y]
#     row = board[x, max(0, y-4):min(15, y+5)]
#     forward_diag = board.diagonal(y-x)
#     backward_diag = board.T.diagonal(y-x)

def explore_convolve(board,player,n):
    val= np.zeros((15,15))
    val+= cv2m(board.astype('uint8'),player*seq.astype('uint8'),method=cv2.TM_CCOEFF)
    val+= cv2m(board.T.astype('uint8'),player*seq.astype('uint8'),method=cv2.TM_CCOEFF)
    val+= cv2m(board.astype('uint8'),player*diag.astype('uint8'),method=cv2.TM_CCOEFF, mask=diag.astype('uint8'))
    val+= cv2m(board.astype('uint8'),player*otherdiag.astype('uint8'),method=cv2.TM_CCOEFF, mask=otherdiag.astype('uint8'))
    val+= cv2m(board.astype('uint8'),player*eye3.astype('uint8'),method=cv2.TM_CCOEFF, mask=eye3_mask.astype('uint8'))
    val+= cv2m(board.astype('uint8'),player*cross3.astype('uint8'),method=cv2.TM_CCOEFF, mask=cross.astype('uint8'))
    # now get the coords of the n max
    idx = np.argpartition(val.flatten(), -n)[-n:]
    idx = idx[np.argsort(val.flatten()[idx])]
    return idx.reshape((n,2))


def convolution_score(board,player):
    val= 0
    p=5
    board_ = board.copy()
    board_[board_ == player] = p
    board_[board_==-player] = 255
    val+= np.sum(cv2m(board_.astype('uint8'),  p*seq.astype('uint8'),method=cv2.TM_SQDIFF)**4)
    val+= np.sum(cv2m(board_.T.astype('uint8'),p*seq.astype('uint8'),method=cv2.TM_SQDIFF)**4)
    val+= np.sum(cv2m(board_.astype('uint8'),  p*diag.astype('uint8'),method=cv2.TM_SQDIFF, mask=diag.astype('uint8'))**4)
    val+= np.sum(cv2m(board_.astype('uint8'),  p*otherdiag.astype('uint8'),method=cv2.TM_SQDIFF, mask=otherdiag.astype('uint8'))**4)
    val+= np.sum(cv2m(board_.astype('uint8'),  p*eye3.astype('uint8'),method=cv2.TM_SQDIFF, mask=eye3_mask.astype('uint8')))
    val+= np.sum(cv2m(board_.astype('uint8'),  p*cross3.astype('uint8'),method=cv2.TM_SQDIFF, mask=cross3.astype('uint8')))
    val+=np.sum(cv2m(board_.astype('uint8'),   p*line.astype('uint8'),method=cv2.TM_SQDIFF, mask=seq.astype('uint8'))**2)
    val+=np.sum(cv2m(board_.T.astype('uint8'), p*line.astype('uint8'),method=cv2.TM_SQDIFF, mask=seq.astype('uint8'))**2)
    val+=np.sum(cv2m(board_.astype('uint8'),   p*line_diag.astype('uint8'),method=cv2.TM_SQDIFF, mask=diag.astype('uint8'))**2)
    val+=np.sum(cv2m(board_.astype('uint8'),   p*line_otherdiag.astype('uint8'),method=cv2.TM_SQDIFF, mask=otherdiag.astype('uint8'))**2)
    return float('1e-30')/(val**2)  # caus lower is better and we want highr

def draw(board):
    for i in range(15):
        for j in range(15):
            if board[i,j] == 0:
                print('-', end='')
            elif board[i,j] == 1:
                print("X", end='')
            else:
                print("O", end='')
        print('')
    print('')


def evaluate_board(board, player):
    # check the row
    score=0
    score+= find_sequence(board, seq*player)*100
    # check the column
    score+= find_sequence(board.T, seq*player)*100
    # check the diagonal
    score+= find_sequence(board, diag*player, diag.astype('uint8'))*100
    # check the diagonal
    score+= find_sequence(board, otherdiag*player, otherdiag.astype('uint8'))*100
    #check line 4
    score+= find_sequence(board, line4*player)*60
    #check line 4 column
    score+= find_sequence(board.T, line4*player)*60
    #check line 4 diagonal
    score+= find_sequence(board, line4_diag*player, line4_diag_mask.astype('uint8'))*60
    #check line 4 other diagonal
    score+= find_sequence(board, line4_otherdiag*player, line4_otherdiag_mask.astype('uint8'))*60
    # check eye
    score+= find_sequence(board, eye3*player, eye3_mask.astype('uint8'))*20
    # check cross
    score+= find_sequence(board, cross3*player, cross3_mask.astype('uint8'))*20
    # check line
    score+= find_sequence(board, line*player, seq.astype('uint8'))*5
    # check line
    score+= find_sequence(board.T, line*player, seq.astype('uint8'))*5
    # check line diag
    score+= find_sequence(board, line_diag*player, diag.astype('uint8'))*5
    # check other line diag
    score+= find_sequence(board, line_otherdiag*player, otherdiag.astype('uint8'))*5
    return score

def get_first_layer(board, neighbour):
    return np.where((board == 0) * (neighbour > 0))

def get_immediate(board,idx):
    # get immediate neighbours
    t = np.tile(cneighbour.T, idx[0].shape[0]).T + np.repeat(np.array(idx).T, 8, axis=0)
    # t = t[np.where(t < 15 ) and np.where(t > 0)]
    # t = np.tile(cneighbour.T, move.shape[1]).T + np.repeat(move.T, 8, axis=0)
    _t = (t[:, 0] >= 0) * (t[:, 0] < 15) * (t[:, 1] >= 0) * (t[:, 1] < 15)
    # t = np.array((t[::2],t[1::2]))
    t = (t[:,0], t[:,1])
    return t

def get_moves(board, neighbours,n):
    #get coordinates of the neighbour cell with the highest score but not in the board
    neighbours_ = neighbours.copy()
    neighbours_[board!=0] = 0
    # print("the fi")
    # for i in range(15):
    #     for j in range(15):
    #         if neighbours_[i,j] == 0:
    #             print('-', end='')
    #         else:
    #             print((int)(neighbours_[i,j]), end='')
    #     print('')
    # print('')
    maxamount = min(n,len(np.where(neighbours_>0)[0]))
    ind = np.unravel_index(np.argsort(neighbours_, axis=None)[::-1][:maxamount], neighbours_.shape)
    # print(ind)
    # print("m",maxamount)
    # print(neighbours_[ind])
    return ind


def alpha_beta_prunning(board, neighbours,player, alpha, beta, depth, idx):
    if depth == 0 :
        # return evaluate_board(board, player)-evaluate_board(board, -player)
        return convolution_score(board,-player) / convolution_score(board,player)
    winner = get_winner(board)
    if winner != 0:
        return -winner*player*depth*9999999999 + (convolution_score(board,-player) / convolution_score(board,player))
    V = -99999999
    # moves = get_immediate(board,idx)
    # temp = (get_moves(board, neighbours,20))
    # moves = (np.append(moves[0], temp[0]), np.append(moves[1], temp[1]))
    # idx = explore_convolve(board,player,10)
    # iss = np.random.randint(0,idx[0].shape[0],nmoves)
    moves = get_moves(board, neighbours,20+5*depth)
    for i in range(len(moves[0])):
        moven = np.array([moves[0][i],moves[1][i]])
        moven = moven[:, None]
        move = (moves[0][i],moves[1][i])
        board[move] = player
        t = np.tile(cneighbour.T, moven.shape[1]).T + np.repeat(moven.T, 8, axis=0)
        # t = t[np.where(t < 15) and np.where(t >= 0)]
        _t = (t[:, 0] >= 0) * (t[:, 0] < 15) * (t[:, 1] >= 0) * (t[:, 1] < 15)
        # t = np.array((t[::2],t[1::2]))
        t = t[_t]
        t = (t[:,0], t[:,1])
        neighbours[t] += 1
        V = max(V,alpha_beta_prunning(board, neighbours, -player, -beta, -alpha, depth-1, t))
        board[move] = 0
        neighbours[t] -= 1
        if V>=beta:
            return V
        alpha = max(alpha,V)
    return alpha



def solve(board,player, last_x, last_y):
    # get remaining depth
    # player = -player

    remaining = 120 - len(np.where(board != 0)[0])
    depth = min(remaining,6)
    # get neighbours
    neighbours = np.zeros(board.shape)
    # get the indexes of the empty cells
    idx = np.where(board != 0 )
    # get the neighbours of the empty cells
    t = np.tile(cneighbour.T, idx[0].shape[0]).T + np.repeat(np.array(idx).T, 8, axis=0)
    # t = t[np.where(t < 15 ) and np.where(t > 0)]
    # t = np.tile(cneighbour.T, move.shape[1]).T + np.repeat(move.T, 8, axis=0)
    _t = (t[:, 0] >= 0) * (t[:, 0] < 15) * (t[:, 1] >= 0) * (t[:, 1] < 15)
    # t = np.array((t[::2],t[1::2]))
    t = t[_t]
    t = (t[:,0], t[:,1])
    neighbours[t] += 1
    #display the neighbours
    print("neighbours")
    print(neighbours)
    print("board")
    draw(board)
    # parameters
    best_x=-1
    best_y=-1
    alpha = -np.Inf
    beta = np.Inf
    V= alpha
    # moves = get_immediate(board,(np.array([last_x]),np.array([last_y])))
    # temp = (get_moves(board, neighbours,15*15))
    # moves = (np.append(moves[0], temp[0]), np.append(moves[1], temp[1]))
    # moves = get_first_layer(board,neighbours)
    moves = get_moves(board, neighbours,15*15)
    print("number of moves:", len(moves[0]), player)
    for i in range(len(moves[0])):
        moven = np.array([moves[0][i],moves[1][i]])
        moven = moven[:, None]
        move = (moves[0][i],moves[1][i])
        # play
        # print(player)
        # print(f"before move: {move}")
        # draw(board)
        board[move] = player
        # print(f"after move: {move}")
        # draw(board)
        t = np.tile(cneighbour.T, moven.shape[1]).T + np.repeat(moven.T, 8, axis=0)
        _t = (t[:, 0] >= 0) * (t[:, 0] < 15) * (t[:, 1] >= 0) * (t[:, 1] < 15)
        # t = np.array((t[::2],t[1::2]))
        t = t[_t]
        t = (t[:,0], t[:,1])
        neighbours[t] += 1
        #evaluate
        V = max(V, alpha_beta_prunning(board,neighbours,-player,-beta,-alpha,depth-1, t))
        print(i,"move: ", move, "score: ", V)
        #unplay
        board[move] = 0
        neighbours[t] -= 1
        if V >= beta:
            best_x = move[0]
            best_y = move[1]
            break
        if V > alpha:
            alpha = V
            best_x = move[0]
            best_y = move[1]
    print("best move: ", best_x, best_y)
    return (best_x, best_y)