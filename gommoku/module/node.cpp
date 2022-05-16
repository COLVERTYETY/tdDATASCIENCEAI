#include "node.h"

node::node(/* args */)
{
}

node::~node(/* args */)
{
    if(children.size() > 0)
    {
        for(int i = 0; i < children.size(); i++)
        {
            delete children[i];
        }
    }
    children.clear();
}

int get_victor(int board[15][15]){
    /// detect if 5 or more of the same color are in a row
    // detect horizontal
    for (int i = 0; i < 15; i++) {
        for (int j = 0; j < 11; j++) {
            if (board[i][j] != 0 && board[i][j] == board[i][j+1] && board[i][j] == board[i][j+2] && board[i][j] == board[i][j+3] && board[i][j] == board[i][j+4]) {
                // std::cout<<"horizontal winner: "<<board[i][j]<<std::endl;
                return  board[i][j];
            }
        }
    }
    // detect vertical
    for (int i = 0; i < 11; i++) {
        for (int j = 0; j < 15; j++) {
            if (board[i][j] != 0 && board[i][j] == board[i+1][j] && board[i][j] == board[i+2][j] && board[i][j] == board[i+3][j] && board[i][j] == board[i+4][j]) {
                // std::cout<<"vertical winner: "<<board[i][j]<<std::endl;
                return board[i][j];
            }
        }
    }
    // detect diagonal
    for (int i = 0; i < 11; i++) {
        for (int j = 0; j < 11; j++) {
            if (board[i][j] != 0 && board[i][j] == board[i+1][j+1] && board[i][j] == board[i+2][j+2] && board[i][j] == board[i+3][j+3] && board[i][j] == board[i+4][j+4]) {
                // std::cout <<"diagonal winner: "<<board[i][j]<<std::endl;
                return board[i][j];
            }
        }
    }
    // detect other diagonal
    for (int i = 0; i < 11; i++) {
        for (int j = 4; j < 15; j++) {
            if (board[i][j]!=0 && board[i][j] == board[i+1][j-1] && board[i][j] == board[i+2][j-2] && board[i][j] == board[i+3][j-3] && board[i][j] == board[i+4][j-4]) {
                // std::cout <<"other diagonal winner: "<<board[i][j]<<std::endl;
                return board[i][j];
            }
        }
    }
    return 0;
}

node::node(int x_, int y_, node* parent_, int player_)
{
    x = x_;
    y = y_;
    parent = parent_;
    wins = 0;
    simulations = 0;
    player = player_;
}

node::node(int x_, int y_, node* parent_, int player_, int depth_)
{
    x = x_;
    y = y_;
    parent = parent_;
    depth = depth_;
    wins = 0;
    simulations = 0;
    player = player_;
}

void node::add_star(int x_, int y_, int star[15][15])
{
    int starpattern[][2] = {{2,0},{3,0},{4,0},{-2,0},{-3,0},{-4,0},{0,-2},{0,-3},{0,-4},{0,2},{0,3},{0,4},{2,2},{3,3},{4,4},{2,-2},{3,-3},{4,-4},{-2,-2},{-3,-3},{-4,-4},{-2,2},{-3,3},{-4,4}};
    for (int i = 0; i < 24; i++)
    {
        int x_ = x_ + starpattern[i][0];
        int y_ = y_ + starpattern[i][1];
        if (x_ >= 0 && x_ < 15 && y_ >= 0 && y_ < 15)
        {
            star[x_][y_] +=1;
        }
    }
}

void node::sub_star(int x_, int y_, int star[15][15])
{
    int starpattern[][2] = {{2,0},{3,0},{4,0},{-2,0},{-3,0},{-4,0},{0,-2},{0,-3},{0,-4},{0,2},{0,3},{0,4},{2,2},{3,3},{4,4},{2,-2},{3,-3},{4,-4},{-2,-2},{-3,-3},{-4,-4},{-2,2},{-3,3},{-4,4}};
    for (int i = 0; i < 24; i++)
    {
        int x_ = x_ + starpattern[i][0];
        int y_ = y_ + starpattern[i][1];
        if (x_ >= 0 && x_ < 15 && y_ >= 0 && y_ < 15)
        {
            star[x_][y_] -=1;
        }
    }
}

void node::add_neighbour(int x_, int y_, int neightbours[15][15])
{
    // std::cout<< "beginning of function" << std::endl;
    int neightbourpattern[8][2] = {{-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 1}, {1, -1}, {1, 0}, {1, 1}};
    // std::cout<<"before for loop"<<std::endl;
    for (int i = 0; i < 8; i++)
    {
        int x_ = x_ + neightbourpattern[i][0];
        int y_ = y_ + neightbourpattern[i][1];
        if (x_ >= 0 && x_ < 15 && y_ >= 0 && y_ < 15)
        {
            // std::cout<<"addded a neighbour"<<std::endl;
            neightbours[x_][y_] +=1;
        }
    }
}

void node::sub_neighbour(int x_, int y_, int neightbours[15][15])
{
    int neightbourpattern[8][2] = {{-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 1}, {1, -1}, {1, 0}, {1, 1}};
    for (int i = 0; i < 8; i++)
    {
        int x_ = x_ + neightbourpattern[i][0];
        int y_ = y_ + neightbourpattern[i][1];
        if (x_ >= 0 && x_ < 15 && y_ >= 0 && y_ < 15)
        {
            neightbours[x_][y_] -= 1;
        }
    }
}

void node::expand(int board[15][15], int neightbours[15][15], int star[15][15]){
    // std::cout<< "expanding"<<std::endl;
    for (int i = 0; i < 15; i++) {
        for (int j = 0; j < 15; j++) {
            if (board[i][j]==0 && (neightbours[i][j] > 0)) {
                children.push_back(new node(i, j, this, -player));
            }
        }
    }
}

int node::simulate(int player, int board[15][15], int neightbours[15][15], int depth){
    // std::cout << "simulating"<< std::endl;
    int available_turns = 0;
    // check if there are any available turns
    for (int i = 0; i < 15; i++) {
        for (int j = 0; j < 15; j++) {
            if (board[i][j]==0) {
                available_turns++;
            }
        }
    }
    if (available_turns == 0) {
        return get_victor(board);
    }
    available_turns = (available_turns>depth)?depth:available_turns;
    // create a copy of the board
    int board_[15][15];
    for (int i = 0; i < 15; i++) {
        for (int j = 0; j < 15; j++) {
            board_[i][j] = board[i][j];
        }
    }
    // create a copy of the neightbours
    int neightbours_[15][15];
    for (int i = 0; i < 15; i++) {
        for (int j = 0; j < 15; j++) {
            neightbours_[i][j] = neightbours[i][j];
        }
    }
    // std::cout << "the boards were copied"<< std::endl;
    //simulate the game
    while (available_turns > 0) {
        // std::cout << "available turns: " << available_turns << std::endl;
        int y = std::rand() % 15;
        int x = std::rand() % 15;
        int xm= (std::rand()%2==0)?-1:1;
        int ym= (std::rand()%2==0)?-1:1;
        do{
            x+=xm;
            x=(x+15)%15;
            if(x==0){
                y+=ym;
                y=(y+15)%15;
            }
        }while (board_[x][y] != 0 && neightbours_[x][y] > 0);
        board_[x][y] = player;
        available_turns--;
        int winner = get_victor(board_);
        if (winner != 0) {
            // std::cout << "winner: " << winner << " turns " << available_turns<< std::endl;
            return winner;
        }
        add_neighbour(x, y, neightbours_);
        player = -player;
    }
    return 0;
}

// get highest leaf node
double node::get_highest_leaf(double highscore,node* best){
    // if is a leaf
    // children = 0 or moves are available
    std::cout << "status " << children.size() <<" "<< available_moves.size()<< " "<<std::endl;
    if (children.size() == 0 || available_moves.size() > 0) {
        double score = (double)(wins)/(double)(simulations);
        if (score >= highscore) {
            highscore = score;
            best = this;
            // std::cout << "is null " << (best == NULL) << std::endl;
        }
    }
    if (children.size() > 0) {
        std::cout<< "we have children"<<std::endl;
        for (int i = 0; i < children.size(); i++) {
            double score = children[i]->get_highest_leaf(highscore, best);
            if (score >= highscore) {
                std::cout<< "another better"<<std::endl;
                highscore = score;
            }
        }
    }
    std::cout << "is null 2 " << (best == NULL) << std::endl;
    return highscore;
}

// get available moves
void node::fill_available_moves(int board[15][15], int neighbours[15][15]){
    hasbeenexpanded=1;
    for(int i=0;i<15;i++){
        for(int j=0;j<15;j++){
            if(board[i][j]==0 && neighbours[i][j]>0){
                available_moves.push_back(new node(i,j,this,-player, depth-1));
            }
        }
    }
}

void node::expand2(int board[15][15], int neightbours[15][15]){
    std::cout<< "expanding"<<  this->available_moves.size()<<" "<< this->children.size()<<std::endl;
    if (this->available_moves.size() == 0 && this->children.size() == 0) {
        std::cout << "searching for moves" << std::endl;
        fill_available_moves(board, neightbours);
    }else{
        // transfer a move to the children
        if (available_moves.size() > 0) {
            std::cout << "transferring a move" << std::endl;
            node* temp = this->available_moves.back();
            this->children.push_back(temp);
            this->available_moves.pop_back();
            std::cout << "simulate" << std::endl;
            int win = temp->simulate(player, board, neightbours, temp->depth);
            std::cout << "simulate done" << std::endl;
            backpropagate(win);
            // delete temp;
        }
    }
}

node* node::UCB1()
{
    // find the child with the highest score
    // for every child
    node* best;
    double best_usb1=0;
    for( node* n:children){
        if(n->simulations==0){
            best = n;
            // return children[rand()%children.size()];
            break;
        }else{
            double v = ((double)(n->wins)/(double)(n->simulations))+0.9*sqrt(log((double)simulations)/(double)(n->simulations));
            if (v>=best_usb1){
                best_usb1=v;
                best = n;
            }
        }
    }
    // std::cout << "best ucb1 score is: "<< best_usb1<<std::endl;
    return best;
}

void node::backpropagate(int winner){
    // update the score
    // std::cout<<"backprog"<< (parent == NULL) << std::endl;
    simulations++;
    if (winner == player) {
        wins++;
    }
    // update the parent
    if (parent != NULL) {
        parent->backpropagate(winner);
    }
}

double node::best_child(int *x, int *y){
    node* best; // the best child
    double best_score = 0; // the best score
    // for every child
    for( node* n:children){
        if(n->simulations!=0 && ((double)(n->wins)/(double)(n->simulations))>=best_score){
            best = n;
            best_score = ((double)(n->wins)/(double)(n->simulations));
        }
    }
    *x = best->x;
    *y = best->y;
    return best_score;
}

void node::mcts(int board[15][15], int neightbours[15][15], int star[15][15],int depth){
    // play our move
    // std::cout << "mcts "<<board[x][y]<<std::endl;
    if(parent != NULL) {
        board[x][y] = player;
        add_neighbour(x, y, neightbours);
        // add_star(x, y, star);
        // add_star(x, y, star);
    }
    int winner = get_victor(board);
    // std::cout << "neighbours added and victor is: "<< winner<<std::endl;
    if (winner != 0 || depth == 0) {
        // std::cout << "terminal node" <<std::endl;
        backpropagate(winner);
    } else{
        // if the node is a leaf
        if (children.size() == 0) {
            // expand the node
            expand(board, neightbours, star);
            // simulate the game
            int winner = simulate(player, board, neightbours,depth);
            // backpropagate the result
            backpropagate(winner);
        }else{
            // find the best child
            node* best = UCB1();
            best->mcts(board, neightbours, star, depth-1);
        }
    }

    if(parent!=NULL){
        // undo our move
        board[x][y] = 0;
        sub_neighbour(x, y, neightbours);
        // sub_star(x, y, star);
        // sub_star(x, y, star);
    }

}

void node::mcts_max(int board[15][15], int neightbours[15][15], int depth){
    node* best;
    double best_score = get_highest_leaf(-1,best); //! not null inside
    std::cout << "best score is: "<< best_score<< " " <<(best==NULL)<<std::endl;//! but here null???
    best->expand2(board, neightbours);

}



int node::rootmove(int board[15][15], int neightbours[15][15], int star[15][15], int ms,int depth, int *x, int *y){
    // while we still have time
    std::cout<<"starting the root moove"<<std::endl;
    auto start = std::chrono::high_resolution_clock::now();
    int iteration=0;
    while (iteration<120000 && (std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now()-start).count()) < ms) {
        mcts(board, neightbours, star, depth);
        iteration++;
        std::cout<<"\rit "<<iteration;
    }
    // find the best child
    double best_score = best_child(x, y);
    std::cout<<std::endl<<"best score is: "<< best_score<<std::endl;
    return iteration;
}

int node::rootmove_max(int board[15][15], int neightbours[15][15], int ms,int depth, int *x, int *y){
    // while we still have time
    std::cout<<"starting the root moove MAX"<<std::endl;
    auto start = std::chrono::high_resolution_clock::now();
    int iteration=0;
    simulations=1;
    // expand2(board, neightbours);
    while (iteration<120000 && (std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now()-start).count()) < ms) {
        mcts_max(board, neightbours, depth);
        iteration++;
        std::cout<<"\rit "<<iteration;
    }
    // find the best child
    double best_score = best_child(x, y);
    std::cout<<std::endl<<"best score is: "<< best_score<<std::endl;
    return iteration;
}

// node* node::update_root(int new_board[15][15], int board[15][15], int neightbours[15][15], int star[15][15], int player_){
//     int dx, dy,ndiff;
//     // find the difference between the baord and the new board
//     for (int i = 0; i < 15; i++) {
//         for (int j = 0; j < 15; j++) {
//             if (board[i][j] != new_board[i][j]) {
//                 dx = i;
//                 dy = j;
//                 ndiff++;
//             }
//         }
//     }
//     // update board
//     for (int i = 0; i < 15; i++) {
//         for (int j = 0; j < 15; j++) {
//             board[i][j] = new_board[i][j];
//         }
//     }
//     if (ndiff <= 1 && player == player_) {
//         // search if a child with the same coordinates exists
//         for (node* n:children){
//             if (n->x == dx && n->y == dy){
//                 std::cout << "this path is part of the computed tree" << std::endl;
//                 // delete the other children
//                 for (node* m:children){
//                     if (m->x != dx || m->y != dy){
//                         delete m;
//                     }
//                 }
//                 return n;
//             }
//         }
//         std::cout<< "no child found" << std::endl;
//     }else{
//         std::cout << "too many differences" << std::endl;
//     }
//     std::cout << "creating new tree" << std::endl;
//     // if not delete the old children and create a new one
//     for (node* n:children){
//         delete n;
//     }
//     children.clear();
//     x = dx;
//     y = dy;
//     simulations=0;
//     wins=0;
//     player = -player;
//     expand(board, neightbours, star);
//     return this;
// }

