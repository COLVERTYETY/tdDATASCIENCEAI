#include <stdio.h>
#include <time.h>
#include <stdlib.h>

#define side 3

int board[side*side];

void display(){
    printf("\n");
    for(int i=0;i<side;i++){
        for(int j=0;j<side;j++){
            printf("%d ",board[(side*i)+j%side]);
            // printf(" ");
        }
        printf("\n");
    }
}

int hamming(){
    int distance = 0;
    int SIZE = side*side;
    for(int i=0;i<SIZE-1;i++){
        if(board[i]!=(i+1)){distance++;}
    }
    return distance;
}

int manhattan(){
    int distance = 0;
    int SIZE = side*side;
    for(int i=0;i<SIZE-1;i++){
        if(board[i]!=(i+1)){distance+=((i%3)+i/3) - ((board[i]%3)+board[i]/3);}
    }
    return distance;
}

void main(){
    /// init
    printf("starting\n");
    int SIZE = side*side;
    srand(time(NULL));
    display();
    //fill
    for(int i=0;i<(side*side)-1;i++){
        board[i]=i+1;
    }
    display();
    //shuffle
    int x = 2;
    int y = 2;
    int temp;
    for(int i=0;i<10*SIZE;i++){
        switch (rand()%4)
        {
        case 0:
            if(x>0){
                temp = board[3*x+y];
                board[3*x+y] = board[3*(x-1)+y];
                x--;
                board[3*x+y] = temp;
            }
            break;
        case 1:
            if(x<2){
                temp = board[3*x+y];
                board[3*x+y] = board[3*(1+x)+y];
                x++;
                board[3*x+y] = temp;
            }
            break;
        case 2:
            if(y>0){
                temp = board[3*x+y];
                board[3*x+y] = board[3*x+(y-1)];
                y--;
                board[3*x+y] = temp;
            }
            break;
        case 3:
            if(y<2){
                temp = board[3*x+y];
                board[3*x+y] = board[3*x+(y+1)];
                y++;
                board[3*x+y] = temp;
            }
            break;
        default:
            break;
        }
        // display();
    }
    display();
    printf("over\n");
}