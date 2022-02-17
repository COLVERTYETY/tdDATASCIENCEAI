#ifndef QUEENS
#define QUEENS
#include <iostream>
#include <stdio.h>
#include <stdlib.h>     /* srand, rand */
#include <time.h>

class Queen{
    private:
        int* myqueens;
        int score;
    public:
        Queen();
        ~Queen();
        void mutate();
        void crossover(Queen& Q);
        void evaluate();
        int getscore();
        friend bool operator<(const Queen& a,const Queen& b);
        friend std::ostream& operator<<( std::ostream&  out, const Queen& Q);
        static bool comp(const Queen* a, const Queen* b);
};


#endif
