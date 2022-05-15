#ifndef NODE
#define NODE
#include <vector>
#include <cstdlib>
#include <algorithm>
#include <cmath>
#include <utility>
#include <time.h>
#include <iostream>
#include <chrono>
#include <unistd.h>


class node
{
private:
public:
    int x,y;
    std::vector<node*> children;
    std::vector<node*> available_moves;
    node* parent;
    int wins;
    int simulations;
    int player;
    int depth;
    int hasbeenexpanded;
    int isroot = 0;
    node(/* args */);
    node(int x_, int y_, node* parent_, int player_);
    node(int x_, int y_, node* parent_, int player_, int depth_);
    ~node();
    void expand(int board[15][15], int neightbours[15][15], int star[15][15]);
    void expand2(int board[15][15], int neightbours[15][15]);
    int simulate(int player,int board[15][15], int neightbours[15][15], int depth);
    void add_neighbour(int x_, int y_, int neightbours[15][15]);
    void sub_neighbour(int x_, int y_, int neightbours[15][15]);
    void add_star(int x_, int y_, int star[15][15]);
    void sub_star(int x_, int y_, int star[15][15]);
    node* UCB1();
    void backpropagate(int winner);
    double best_child(int *x, int *y);
    void mcts(int board[15][15], int neightbours[15][15], int star[15][15], int depth);
    void mcts_max(int board[15][15], int neightbours[15][15],int depth);
    int rootmove(int board[15][15], int neightbours[15][15], int star[15][15], int ms, int depth, int*x, int*y);
    int rootmove_max(int board[15][15], int neightbours[15][15], int ms,int depth, int *x, int *y);
    double get_highest_leaf(double highscore,node* best);
    void fill_available_moves(int board[15][15], int neighbours[15][15]);
    node* update_root(int new_board[15][15], int board[15][15], int neightbours[15][15], int star[15][15],int player_);
};

#endif // NODE