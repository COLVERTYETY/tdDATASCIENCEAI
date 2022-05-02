#ifndef BOARD
#define BOARD

#include <stdlib.h>     /* srand, rand */
#include <time.h>       /* time */
#include <unordered_map> /*hashmap*/

#define SIZE 9

class Board{
    public:
        int tiles[SIZE];
        std::unordered_map<int[SIZE], int> evals;
        Board();
        int hamming();
        int manhattan();
        int evaluate();
};

#endif 