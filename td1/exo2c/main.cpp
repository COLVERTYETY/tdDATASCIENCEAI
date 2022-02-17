#include <stdio.h>
#include "queens.h"

int main(){
    std::cout << "START\n";
    srand(time(NULL));
    Queen* queens[10];
    std::cout <<"LOOP\n";
    for(int i=0;i<8;i++){
        queens[i] = new Queen();
        std::cout << *queens[i]<<"\n";
    }
    return 0;
}
