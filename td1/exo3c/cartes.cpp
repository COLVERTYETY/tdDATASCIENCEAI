#include "cartes.h"
#include <math.h>

Carte::Carte(){
    mycards = (int*)malloc(sizeof(int)*10);
    int possible[] = {1,2,3,4,5,6,7,8,9,10};
    int chosen[] =   {0,0,0,0,0,0,0,0,0,0};
    bool succes=false;
    for(int i=0;i<10;i++){
        // myqueens[i] = 1+rand()%8;
        // std::cout <<myqueens[i];
        succes = false;
        while(!succes){
            int rnd = rand()%10;
            if(chosen[rnd]==0){
                succes = true;
                chosen[rnd]=1;
                mycards[i] = possible[rnd];
            }
        }
    }
    // extra genes
    weight360 = (float)(rand()%100)/(float)(1+rand()%100)+1;
    weight36 = (float)(rand()%100)/(float)(1+rand()%100)+1;
}

Carte::~Carte(){
    delete(mycards);
}

void Carte::mutate(){
    int a = rand()%10;
    int b = rand()%10;
    int temp = mycards[a];
    mycards[a] = mycards[b];
    mycards[b]=temp;
    // extra
    weight360 += float(((rand()%3) -1)/10.0);
    weight360 = (weight360<=1)?(1):weight360;
    weight36 += float(((rand()%3) -1)/10.0);
    weight36 = (weight36<=1)?(1):weight36;
}

void Carte::crossover(const Carte& other){
    if((rand()%2)==0){
        weight360 = other.weight360;
    }else{
        weight36 = other.weight36;
    }
}

void Carte::evaluate(){
    float prod360=1.0;
    for(int i=0;i<6;i++){
        prod360*=(float)mycards[i];
    }
    float sum36=0.0;
    for(int i=6;i<10;i++){
        sum36+=(float)mycards[i];
    }
    // calc scores
    // score360 = ((prod360/360.0)-1)*((prod360/360.0)-1);
    // score36 = ((sum36/36.0)-1)*((sum36/36.0)-1);
    score360 = (prod360-360.0)*(prod360-360.0);
    score36 = (sum36-36.0)*(sum36-36.0);
    score = (weight360*score360 + weight36*score36)/(weight360+weight36);

}

bool operator<(const Carte& a, const Carte& b){
    return a.score < b.score;
}

float roundoff(float value, unsigned char prec)
{
    float pow_10 = std::pow(10.0f, (float)prec);
    return std::round(value * pow_10) / pow_10;
}


std::ostream& operator<<( std::ostream&  out, const Carte& C){
    for(int i=0;i<10;i++){
        out << C.mycards[i]<<" ";
    }
    out <<"W[ " <<std::setw(4)<<roundoff(C.weight360,2)<<" | "<<std::setw(4)<<roundoff(C.weight36,2)<<" ] S{ "<<std::setw(4)<< roundoff(C.score360,2)<<" | "<<std::setw(4)<<roundoff(C.score36,2)<<" } = "<<std::setw(6)<<roundoff(C.score,4);
    return out;
}

bool Carte::comp(const Carte* a, const Carte* b){
    return (*a)<(*b);
}
