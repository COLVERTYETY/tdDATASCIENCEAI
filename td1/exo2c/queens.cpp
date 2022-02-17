#include "queens.h"
#include <stdlib.h>     /* srand, rand */
#include <time.h>

Queen::Queen(){
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
}

Queen::~Queen(){
    delete(myqueens);
}

std::ostream& operator<<( std::ostream&  out, const Queen& Q){
    for(int i=0;i<8;i++){
        out<<Q.myqueens[i];
        out<<" ";
    }
    out<<": ";
    out<<Q.score;
    return out;
}

void Queen::mutate(){
    int a = rand()%8;
    int b = rand()%8;
    int temp = myqueens[a];
    myqueens[a] = myqueens[b];
    myqueens[b]=temp;
}

void Queen::evaluate(){
    int sum=0;
    for(int i=0;i<8;i++){
        for(int j=0;j<8;j++){
            if(j!=i){
                sum+=(abs(myqueens[i]-myqueens[j])==abs(i-j));
            }
        }
    }
    score=sum;
}

int Queen::getscore(){
    return score;
}

bool operator<(const Queen& a,const Queen& b){
    return a.score<b.score;
}

bool Queen::comp(const Queen* a, const Queen* b){
    return (*a)<(*b);
}
