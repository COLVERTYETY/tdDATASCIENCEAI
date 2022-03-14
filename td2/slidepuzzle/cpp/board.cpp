#include "board.h"

Board::Board(){
    for(int i=0;i<SIZE-1;i++){
        tiles[i]=i+1;
    }
    // now shuffle
    int x = 2;
    int y = 2;
    int temp;
    for(int i=0;i<10*SIZE;i++){
        switch (std::rand()%4)
        {
        case 0:
            if(x>0){
                temp = tiles[3*x+y];
                tiles[3*x+y] = tiles[3*(x-1)+y];
                x--;
                tiles[3*x+y] = temp;
            }
            break;
        case 1:
            if(x<2){
                temp = tiles[3*x+y];
                tiles[3*x+y] = tiles[3*(1+x)+y];
                x++;
                tiles[3*x+y] = temp;
            }
            break;
        case 2:
            if(y>0){
                temp = tiles[3*x+y];
                tiles[3*x+y] = tiles[3*x+(y-1)];
                y--;
                tiles[3*x+y] = temp;
            }
            break;
        case 3:
            if(y<2){
                temp = tiles[3*x+y];
                tiles[3*x+y] = tiles[3*x+(y+1)];
                y++;
                tiles[3*x+y] = temp;
            }
            break;
        default:
            break;
        }
    }
}

int Board::hamming(){
    int distance = 0;
    for(int i=0;i<SIZE-1;i++){
        if(tiles[i]!=(i+1)){distance++;}
    }
    return distance;
}

int Board::manhattan(){
    int distance = 0;
    for(int i=0;i<SIZE-1;i++){
        if(tiles[i]!=(i+1)){distance+=((i%3)+i/3) - ((tiles[i]%3)+tiles[i]/3);}
    }
    return distance;
}