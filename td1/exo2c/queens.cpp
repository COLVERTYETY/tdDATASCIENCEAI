#include "queens.h"
#include <stdlib.h>     /* srand, rand */
#include <time.h>

Queen::Queen(){
    std::cout <<"starting";
    myqueens = (int*)malloc(8*sizeof(int));
    int possible[]={1,2,3,4,5,6,7,8};
    int chosen[]=  {0,0,0,0,0,0,0,0};
    bool succes=false;
    for(int i=0;i<8;i++){
        // myqueens[i] = 1+rand()%8;
        // std::cout <<myqueens[i];
        succes = false;
        while(!succes){
            int rnd = rand()%8;
            if(chosen[rnd]==0){
                succes = true;
                chosen[rnd]=1;
                myqueens[i] = possible[rnd];
            }
        }
    }
    std::cout<<"\n";
}

Queen::~Queen(){
    delete(myqueens);
}

std::ostream& operator<<( std::ostream&  out, const Queen& Q){
    for(int i=0;i<8;i++){
        out<<Q.myqueens[i];
        out<<" ";
    }
    return out;
}
