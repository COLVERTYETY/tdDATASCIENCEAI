#include <stdio.h>
#include "main.h"
#include <time.h>
#include <stdlib.h>

int board[3][3] = {
    {0,0,0},
    {0,0,0},
    {0,0,0},
};

int main() {
    srand(time(NULL));
    int nplays=0;
    while (checkwin() == 0 && nplays < 9) {
        displayboard();
        if(nplays%2==0){
            getinput(1);
        }else{
            compmoveAB(1);
        }
        nplays++;
    }
    if (nplays == 9) {
        printf("Tie game!\n");
    } else {
        // mark x if player won
        char m = (checkwin() == 1) ? 'x' : 'o';
        printf("Player %c wins!\n", m);
    }
    if(checkwin() == 1) {
        printf("Player 1 wins!\n");
    } else if (checkwin() == -1) {
        printf("Player -1 wins!\n");
    }
    return 0;
}

void displayboard() {
    int i, j;
    for (i = 0; i < 3; i++) {
        for (j = 0; j < 3; j++) {
            // use x for player 1, o for player -1
            if (board[i][j] == 1) {
                printf("x");
            } else if (board[i][j] == -1) {
                printf("o");
            } else {
                printf("_");
            }
        }
        printf("\n");
    }
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
                    board[i][j] = 0;
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

// computer moves using alpha-beta pruning
void compmoveAB(int player){
    int i, j;
    int row, col;
    for (i = 0; i < 3; i++) {
        for (j = 0; j < 3; j++) {
            if (board[i][j] == 0) {
                board[i][j] = -1;
                if (checkwin() == -1) {
                    board[i][j] = 0;
                    return;
                }
                board[i][j] = 0;
            }
        }
    }
    int alpha = -3;
    int beta = 3;
    int best = -3;
    int bestRow = -1;
    int bestCol = -1;
    for (i = 0; i < 3; i++) {
        for (j = 0; j < 3; j++) {
            if (board[i][j] == 0) {
                board[i][j] = -1;
                int val = minAB(alpha, beta, player);
                board[i][j] = 0;
                if (val > best) {
                    best = val;
                    bestRow = i;
                    bestCol = j;
                }
            }
        }
    }
    board[bestRow][bestCol] = -1;
}

int minAB(int alpha, int beta, int player){
    if (checkwin() != 0) {
        return checkwin();
    }
    int i, j;
    int best = 2;
    for (i = 0; i < 3; i++) {
        for (j = 0; j < 3; j++) {
            if (board[i][j] == 0) {
                board[i][j] = 1;
                int val = maxAB(alpha, beta, player);
                board[i][j] = 0;
                if (val < best) {
                    best = val;
                }
                if (best < beta) {
                    beta = best;
                }
                if (beta <= alpha) {
                    return best;
                }
            }
        }
    }
    return best;
}

int maxAB(int alpha, int beta, int player){
    if (checkwin() != 0) {
        return checkwin();
    }
    int i, j;
    int best = -2;
    for (i = 0; i < 3; i++) {
        for (j = 0; j < 3; j++) {
            if (board[i][j] == 0) {
                board[i][j] = -1;
                int val = minAB(alpha, beta, player);
                board[i][j] = 0;
                if (val > best) {
                    best = val;
                }
                if (best > alpha) {
                    alpha = best;
                }
                if (beta <= alpha) {
                    return best;
                }
            }
        }
    }
    return best;
}