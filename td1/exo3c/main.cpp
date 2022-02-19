#include "cartes.h"
#include <vector>
#include <stdio.h>
#include <bits/stdc++.h>

#define pop_size 1000
#define epochs 1000000
#define nkeep 0.4

int main(){
    std::vector<Carte*> thecards;
    std::cout<<"starting\n";
    for(int i=0;i<pop_size;i++){
        thecards.push_back(new Carte());
        // std::cout<<*thecards.at(i)<<"\n";
    }
    // cycle
    for(int nepochs=0;nepochs<epochs;nepochs++){
        //evaluate
        for(Carte* c : thecards){
            c->evaluate();
        }
        //sort
        std::sort(thecards.begin(),thecards.end(),Carte::comp);
        //show the king
        std::cout<<std::setw(4)<<nepochs<<"/"<<epochs<<" :"<<*thecards.at(0)<<"\n";
        //select
        thecards.erase(thecards.begin()+(int)(nkeep*pop_size),thecards.end());
        //mutate
        for(std::vector<Carte*>::iterator it = std::begin(thecards)+1; it != std::end(thecards); ++it){
            (*it)->mutate();
        }
        //crossover
        for(std::vector<Carte*>::iterator it = std::begin(thecards)+1; it != std::end(thecards); ++it){
            int rnd = rand()%thecards.size();
            (*it)->crossover(*thecards.at(rnd));
        }
        //repopulate
        while(thecards.size()!=pop_size){
            thecards.push_back(new Carte);
        }
    }
    for(Carte* c : thecards){
        delete(c);
    }
    return 0;
}
