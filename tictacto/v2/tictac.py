def minmax(player, depth):
    # if the game is over, return the score
    if checkwin() != 0:
        return evaluate()
    if depth == 9:
        return 0

    # if it's the players turn, find the best move
    if player == 1:
        bestscore = -2
    else:
        bestscore = 2

    # try every possible move
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                board[i][j] = player
                score = minmax(-player, depth + 1)
                if player == 1 and score > bestscore:
                    bestscore = score
                if player == -1 and score < bestscore:
                    bestscore = score
                board[i][j] = 0

    return bestscore

def getinput(player):
    row, col = int(input("Player %c, enter row and column: " % ('x' if player == 1 else 'o'))[0]), int(input("Player %c, enter row and column: " % ('x' if player == 1 else 'o'))[1])
    if row < 0 or row > 2 or col < 0 or col > 2:
        print("Invalid input.")
        getinput(player)
    elif board[row][col] != 0:
        print("Invalid input.")
        getinput(player)
    else:
        board[row][col] = player

def displayboard():
    print("\n")
    for i in range(3):
        for j in range(3):
            # use x for player 1, o for player -1
            if board[i][j] == 1:
                print(" X ", end="")
            elif board[i][j] == -1:
                print(" O ", end="")
            else:
                print("   ", end="")
            if j != 2:
                print("│", end="")
        if i != 2:
            print("\n───┼───┼───")
    print("\n\n")

def evaluate():
    for i in range(3):
        if board[i][0] == board[i][1] and board[i][1] == board[i][2]:
            if board[i][0] != 0:
                return board[i][0]*10
    for j in range(3):
        if board[0][j] == board[1][j] and board[1][j] == board[2][j]:
            if board[0][j] != 0:
                return board[0][j]*10
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        if board[0][0] != 0:
            return board[0][0]*10
    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        if board[0][2] != 0:
            return board[0][2]*10
    return 0