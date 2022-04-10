#include <stdio.h>
#include <time.h>
#include <stdlib.h>

int board[3][3] = {
    {0,0,0},
    {0,0,0},
    {0,0,0},
};

int minmax(int player,int *row, int *col, int depth);
void displayboard();
void getinput(int player);
int checkwin();
void compmoveRand();
int evaluate();

int main() {
    int nplays=0;
    int row, col;
    while (checkwin() == 0 && nplays < 9) {
        displayboard();
        if(nplays%2==1){
            getinput(1);
        }else{
            printf("\n%d\n",minmax(-1, &row, &col,0));
            if (row==-1 && col==-1) {
                compmoveRand();
                printf("\n we make a random move\n");
            }
            board[row][col] = -1;
        }
        nplays++;
    }
    displayboard();
    if(checkwin() == 1){
        printf("Player x wins!\n");
    }else if(checkwin() == -1){
        printf("Player o wins!\n");
    }else{
        printf("Tie!\n");
    }
    return 0;
}

void displayboard() {
    int i, j;
    printf("\n");
    for (i = 0; i < 3; i++) {
        for (j = 0; j < 3; j++) {
            // use x for player 1, o for player -1
            if (board[i][j] == 1) {
                printf( " X ");
            } else if (board[i][j] == -1) {
                printf(" O ");
            } else {
                printf("   ");
            }
            if(j!=2){
                printf("│");
            }
        }
        if(i!=2){
            printf("\n───┼───┼───\n");
        }
    }
    printf("\n\n");
}

// get user input
void getinput(int player) {
    int row, col;
    // mark x if player 1, o if player -1
    char m = (player == 1) ? 'x' : 'o';
    printf("Player %c, enter row and column: ", m);
    scanf("%d %d", &row, &col);
    if( row<0 || row>2 || col<0 || col>2 ){
        printf("Invalid input.\n");
        getinput(player);
    }
    else if( board[row][col] != 0 ){
        printf("Invalid input.\n");
        getinput(player);
    }
    else {
        board[row][col] = player;
    }
}

// check if game is finished
int checkwin() {
    int i, j;
    // check rows
    for (i = 0; i < 3; i++) {
        if (board[i][0] == board[i][1] && board[i][1] == board[i][2]) {
            if (board[i][0] != 0) {
                return board[i][0];
            }
        }
    }
    // check columns
    for (j = 0; j < 3; j++) {
        if (board[0][j] == board[1][j] && board[1][j] == board[2][j]) {
            if (board[0][j] != 0) {
                return board[0][j];
            }
        }
    }
    // check diagonals
    if (board[0][0] == board[1][1] && board[1][1] == board[2][2]) {
        if (board[0][0] != 0) {
            return board[0][0];
        }
    }
    // check other diagonal
    if (board[0][2] == board[1][1] && board[1][1] == board[2][0]) {
        if (board[0][2] != 0) {
            return board[0][2];
        }
    }
    return 0;
}

void compmoveRand(){
    int i, j;
    int row, col;
    for (i = 0; i < 3; i++) {
        for (j = 0; j < 3; j++) {
            if (board[i][j] == 0) {
                board[i][j] = -1;
                if (checkwin() == -1) {
                    board[i][j] = -1;
                    return;
                }
                board[i][j] = 0;
            }
        }
    }
    do {
        row = rand() % 3;
        col = rand() % 3;
    } while (board[row][col] != 0);
    board[row][col] = -1;
}

int minmax(int player,int *row, int *col, int depth) {
    int i, j;
    int score;
    int bestscore = (player == 1) ? -2 : 2;
    int bestrow = -1;
    int bestcol = -1;
    if (checkwin() != 0) {
        return evaluate();
    }
    if (depth == 9) {
        return 0;
    }
    for (i = 0; i < 3; i++) {
        for (j = 0; j < 3; j++) {
            if (board[i][j] == 0) {
                board[i][j] = player;
                score = minmax(-player, row, col, depth + 1);
                if (player == 1) {
                    if (score > bestscore) {
                        bestscore = score;
                        bestrow = i;
                        bestcol = j;
                    }
                } else {
                    if (score < bestscore) {
                        bestscore = score;
                        bestrow = i;
                        bestcol = j;
                    }
                }
                board[i][j] = 0;
            }
        }
    }
    if (depth == 0) {
        *row = bestrow;
        *col = bestcol;
    }
    return bestscore;
}

// evaluate board
int evaluate() {
    int i, j;
    // check rows
    for (i = 0; i < 3; i++) {
        if (board[i][0] == board[i][1] && board[i][1] == board[i][2]) {
            if (board[i][0] != 0) {
                return board[i][0]*10;
            }
        }
    }
    // check columns
    for (j = 0; j < 3; j++) {
        if (board[0][j] == board[1][j] && board[1][j] == board[2][j]) {
            if (board[0][j] != 0) {
                return board[0][j]*10;
            }
        }
    }
    // check diagonals
    if (board[0][0] == board[1][1] && board[1][1] == board[2][2]) {
        if (board[0][0] != 0) {
            return board[0][0]*10;
        }
    }
    // check other diagonal
    if (board[0][2] == board[1][1] && board[1][1] == board[2][0]) {
        if (board[0][2] != 0) {
            return board[0][2]*10;
        }
    }
    return 0;
}