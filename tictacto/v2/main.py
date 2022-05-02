def printboard():
    global board
    print("\n")
    for i in range(3):
        for j in range(3):
            if board[i,j] == 0:
                print("   ", end="")
            if board[i,j] == 1:
                print(" X ", end="")
            if board[i,j] == -1:
                print(" O ", end="")
            if j!=2:
                print("│", end="")
        if i!=2:
            print("\n───┼───┼───")
    print("\n")

def gameover():
    global board
    # check rows
    for i in range(3):
        if board[i,0] == board[i,1] == board[i,2]!=0:
            return True
    # check columns
    for j in range(3):
        if board[0,j] == board[1,j] == board[2,j]!=0:
            return True
    # check diagonals
    if board[0,0] == board[1,1] == board[2,2] != 0:
        return True
    if board[0,2] == board[1,1] == board[2,0] != 0:
        return True
    # check if board is full
    for i in range(3):
        for j in range(3):
            if board[i,j] == 0:
                return False
    return True

def whowon():
    global board
    # check rows
    for i in range(3):
        if board[i,0] == board[i,1] == board[i,2]!=0:
            return board[i,1]
    # check columns
    for j in range(3):
        if board[0,j] == board[1,j] == board[2,j]!=0:
            return board[1,j]
    # check diagonals
    if board[0,0] == board[1,1] == board[2,2] != 0:
        return board[1,1]
    if board[0,2] == board[1,1] == board[2,0] != 0:
        return board[1,1]
    return 0


def evaluate():
    global board
    score = 0
    for i in range(3):
        for j in range(3):
            if board[i,j] == 0:
                board[i,j]=1
                if gameover():
                    score += 1
                board[i,j]=-1
                if gameover():
                    score -= 1
                board[i,j]=0
    return score
    

def alphabeta(player,depth,a,b):
    if depth==0 or gameover():
        # print("score:",10*(evaluate() + whowon())+depth)
        return -10*(evaluate() + whowon())+depth
    if player == 1:
        val = -2
        for i in range(3):
            for j in range(3):
                if board[i,j] == 0:
                    board[i,j] = 1
                    val = max(val,alphabeta(-player,depth-1,a,b))
                    board[i,j] = 0
                    a = max(a,val)
                    if b <= a:
                        return val
    if player == -1:
        val = 2
        for i in range(3):
            for j in range(3):
                if board[i,j] == 0:
                    board[i,j] = -1
                    val = min(val,alphabeta(-player,depth-1,a,b))
                    board[i,j] = 0
                    b = min(b,val)
                    if b <= a:
                        return val
    return val

def computermove():
    global board
    bestval = -2
    bestmove = [0,0]
    for i in range(3):
        for j in range(3):
            if board[i,j] == 0:
                board[i,j] = -1
                val = alphabeta(1,2,-2,2)
                board[i,j] = 0
                if val > bestval:
                    bestval = val
                    bestmove = [i,j]
    board[bestmove[0],bestmove[1]] = -1


# create empty board
board = {}

if __name__ == "__main__":
    #init board
    for i in range(3):
        for j in range(3):
            board[i,j] = 0
    # main loop
    nturns = 0
    while nturns<9 and True:
        printboard()
        if nturns%2==1:
            print("X's turn")
            print("Enter row and column: ", end="")
            vals = input()
            vals = vals.split()
            row = int(vals[0])
            col = int(vals[1])
            if board[row,col] == 0:
                board[row,col] = 1
                nturns += 1
            else:
                print("Invalid move")
        else:
            print("O's turn")
            computermove()
            nturns += 1
        if gameover():
            printboard()
            print("Game over")
            break

