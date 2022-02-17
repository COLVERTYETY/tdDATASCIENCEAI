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
        friend std::ostream& operator<<( std::ostream&  out, const Queen& Q);
};


#endif
