#include <stdio.h>
#include "queens.h"
#include <vector>
#include <bits/stdc++.h>

#define pop_size 64
#define nkeep 0.5
#define epochs 1000


int main(){
    std::cout << "START\n";
    srand(time(NULL));
    std::vector<Queen*> theQueens;
    for(int i=0;i<pop_size;i++){
        theQueens.push_back(new Queen());
    }
    int nepochs = 0;
    while((nepochs<epochs)){
        nepochs++;
        // evaluate
        for(int i=0;i<pop_size;i++){
            theQueens.at(i)->evaluate();
        }
        // sort
        std::sort(theQueens.begin(), theQueens.end(), Queen::comp);
        // disp best
        std::cout<<nepochs<<"/"<<epochs<<"  best is: "<<*theQueens.at(0)<<"\n";
        // check for sol
        if((*theQueens.at(0)).getscore()==0){
            break;
        }
        // select
        theQueens.erase(theQueens.begin()+(int)(nkeep*pop_size),theQueens.end());
        //mutate
        for(std::vector<Queen*>::iterator it = std::begin(theQueens)+1; it != std::end(theQueens); ++it){
            (*it)->mutate();
        }
        // repopulate
        while(theQueens.size()!=pop_size){
            theQueens.push_back(new Queen);
        }
    }

    std::cout<<"   OVER  \n";
    // disp and delete
    for(Queen* q : theQueens){
        // std::cout<<*q<<"\n";
        delete(q);
    }

    return 0;
}
