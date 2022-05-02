#include <Python.h>

#include <stdlib.h>
#include <iostream>
#include <cmath>

#define widthN 4
#define widthN1 10
#define MAX_DEPTH 6
#define winmweight 999
#define BETA 1000000
#define ALPHA -1000000

/// 2d array of char to hold the game board, 15*15
int board[15][15];
int neighbors[8][2] = {{-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 1}, {1, -1}, {1, 0}, {1, 1}};
int starpattern[][2] = {{2,0},{3,0},{4,0},{-2,0},{-3,0},{-4,0},{0,-2},{0,-3},{0,-4},{0,2},{0,3},{0,4},{2,2},{3,3},{4,4},{2,-2},{3,-3},{4,-4},{-2,-2},{-3,-3},{-4,-4},{-2,2},{-3,3},{-4,4}};
int neighbour_count[15][15];

static PyObject* myError;

void add_neighbors(int x, int y) {
    int i, j;
    for (i = 0; i < 8; i++) {
        j = x + neighbors[i][0];
        int k = y + neighbors[i][1];
        if (j >= 0 && j < 15 && k >= 0 && k < 15) {
            neighbour_count[j][k] += 2;
        }
    }
}

void add_star_neighbors(int x, int y) {
    int i, j;
    for (i = 0; i < 24; i++) {
        j = x + starpattern[i][0];
        int k = y + starpattern[i][1];
        if (j >= 0 && j < 15 && k >= 0 && k < 15) {
            neighbour_count[j][k] += 1;
        }
    }
}

void sub_star_neighbors(int x, int y) {
    int i, j;
    for (i = 0; i < 24; i++) {
        j = x + starpattern[i][0];
        int k = y + starpattern[i][1];
        if (j >= 0 && j < 15 && k >= 0 && k < 15) {
            neighbour_count[j][k] -= 1;
        }
    }
}

void sub_neighbors(int x, int y) {
    int i, j;
    for (i = 0; i < 8; i++) {
        j = x + neighbors[i][0];
        int k = y + neighbors[i][1];
        if (j >= 0 && j < 15 && k >= 0 && k < 15) {
            neighbour_count[j][k] -= 1;
        }
    }
}

int get_stalemate() {
    int i, j;
    for (i = 0; i < 15; i++) {
        for (j = 0; j < 15; j++) {
            if (board[i][j] == -1) {
                return 0;
            }
        }
    }
    return 1;
}

void get_most_neighbors(int list[][2], int start,int Q) {
    int counts[Q];
    int i, j;
    for (i = 0; i < Q; i++) {
        counts[i] = 0;
    }
    // for every cell of the neighbor_count array
    for (i = 0; i < 15; i++) {
        for (j = 0; j < 15; j++) {
            
            // if the cell is not empty and has a count higher than 0 and empty in the board
            if ((neighbour_count[i][j] > 0) && (board[i][j] == -1)) {
                // if not already in the list
                int found = 0;
                for(int l = 0; l < start; l++) {
                    if(list[l][0] == i && list[l][1] == j) {
                        found = 1;
                        break;
                    }
                }
                    if(found == 0) {
                        for(int l = 0; l < Q; l++) {
                            if (neighbour_count[i][j] > counts[l]) {
                                // shift all the other counts down
                                for (int m = Q - 1; m > l; m--) {
                                    counts[m] = counts[m - 1];
                                    // shift the cell down
                                    list[m+start][0] = list[m - 1][0];
                                    list[m+start][1] = list[m - 1][1];
                                }
                                // set the new count
                                counts[l] = neighbour_count[i][j];
                                // set the new cell
                                list[l+start][0] = i;
                                list[l+start][1] = j;
                                break;
                            }
                        }
                    }
            }

        }
    }
    // display the list
    // for (i = start; i < start+widthN; i++) {
    //     std::cout << list[i][0] << " " << list[i][1] << std::endl;
    // }
}

void get_neighbours(int list[][2], int start, int x, int y) {
    //for every neighbour of the cell
    for (int i = 0; i < 8; i++) {
        int j = x + neighbors[i][0];
        int k = y + neighbors[i][1];
        // if the neighbour is not out of bounds and not filled in the board
        if (j >= 0 && j < 15 && k >= 0 && k < 15 && board[j][k] == -1) {
            // add the neighbour to the list
            list[start+i][0] = j;
            list[start+i][1] = k;
        }
    }
    // display the list
    // for (int i = start; i < 8; i++) {
    //     std::cout << list[i][0] << " " << list[i][1] << std::endl;
    // }
}

int is_winning_move(int x, int y, int player) {
    int i, j;
    board[x][y] = player;
    // check for horizontal win
    for (j = -3; j <= 3; j++) {
        if (y + j >= 0 && y + j < 9) {
            if (board[x][y + j] == player && board[x][y + j + 1] == player && board[x][y + j + 2] == player && board[x][y + j + 3] == player) {
                return 1;
            }
        }
    }
    // check for vertical win
    for (i = -3; i <= 3; i++) {
            if (x + i >= 0 && x + i < 9 ) {
                if (board[x + i][y] == player && board[x + i + 1][y] == player && board[x + i + 2][y] == player && board[x + i + 3][y] == player) {
                    return 1;
                }
            }
    }
    // check for diagonal win
    for (i = -3; i <= 3; i++) {
        if (x + i >= 0 && x + i < 9 && y + i >= 0 && y + i < 9) {
            if (board[x + i][y + i] == player && board[x + i + 1][y + i + 1] == player && board[x + i + 2][y + i + 2] == player && board[x + i + 3][y + i + 3] == player) {
                return 1;
            }
        }
    }
    // check for other diagonal win
    for (i = -3; i <= 3; i++) {
        if (x + i >= 0 && x + i < 9 && y - i >= 0 && y - i < 9) {
            if (board[x + i][y - i] == player && board[x + i + 1][y - i - 1] == player && board[x + i + 2][y - i - 2] == player && board[x + i + 3][y - i - 3] == player) {
                return 1;
            }
        }
    }
    return 0;
}

int alignement_score(int player) {
    int score = 0;
    /// detect all the alignements
    for(int m=1; m<=5; m++) {
        int breakcon=0;
        //detect horizontal
        for (int i = 0; i < 15; i++) {
            for (int j = 0; j < 15-m; j++) {
                for(int k=0; k<=m; k++) {
                    if(board[i][j+k] != player) {
                        break;
                    }
                    if(k==m) {
                        score+=std::pow(10,m);
                        breakcon=1;
                    }
                }
            }
        }
        //detect vertical
        for (int i = 0; i < 15-m; i++) {
            for (int j = 0; j < 15; j++) {
                for(int k=0; k<=m; k++) {
                    if(board[i+k][j] != player) {
                        break;
                    }
                    if(k==m) {
                        score+=std::pow(10,m);
                        breakcon=1;
                    }
                }
            }
        }
        //detect diagonal
        for (int i = 0; i < 15-m; i++) {
            for (int j = 0; j < 15-m; j++) {
                for(int k=0; k<=m; k++) {
                    if(board[i+k][j+k] != player) {
                        break;
                    }
                    if(k==m) {
                        score+=std::pow(10,m);
                        breakcon=1;
                    }
                }
            }
        }
        //detect other diagonal
        for (int i = 0; i < 15-m; i++) {
            for (int j = m; j < 15; j++) {
                for(int k=0; k<=m; k++) {
                    if(board[i+k][j-k] != player) {
                        break;
                    }
                    if(k==m) {
                        score+=std::pow(10,m);
                        breakcon=1;
                    }
                }
            }
        }
        if(breakcon==0) {
            break;
        }
    }
    return score;

}

int evaluate_board(int player) {
    int score = 0;
    // // for every empty cell of the board with atleast one neighbor 
    // for (int i = 0; i < 15; i++) {
    //     for (int j = 0; j < 15; j++) {
    //         if (neighbour_count[i][j] > 0 && board[i][j] == -1) {
    //             score += is_winning_move(i, j, player);
    //             score -= is_winning_move(i, j, 1-player);
    //         }
    //     }
    // }
    score+=alignement_score(player);
    score-=alignement_score(1-player);
    return score;
}

int get_victor(){
    /// detect if 5 or more of the same color are in a row
    // detect horizontal
    for (int i = 0; i < 15; i++) {
        for (int j = 0; j < 8; j++) {
            if (board[i][j] != -1 && board[i][j] == board[i][j+1] && board[i][j] == board[i][j+2] && board[i][j] == board[i][j+3] && board[i][j] == board[i][j+4]) {
                return  board[i][j];
            }
        }
    }
    // detect vertical
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 15; j++) {
            if (board[i][j] != -1 && board[i][j] == board[i+1][j] && board[i][j] == board[i+2][j] && board[i][j] == board[i+3][j] && board[i][j] == board[i+4][j]) {
                return board[i][j];
            }
        }
    }
    // detect diagonal
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            if (board[i][j] != -1 && board[i][j] == board[i+1][j+1] && board[i][j] == board[i+2][j+2] && board[i][j] == board[i+3][j+3] && board[i][j] == board[i+4][j+4]) {
                return board[i][j];
            }
        }
    }
    // detect other diagonal
    for (int i = 0; i < 8; i++) {
        for (int j = 4; j < 15; j++) {
            if (board[i][j]!=-1 && board[i][j] == board[i+1][j-1] && board[i][j] == board[i+2][j-2] && board[i][j] == board[i+3][j-3] && board[i][j] == board[i+4][j-4]) {
                return board[i][j];
            }
        }
    }
    return -1;
}

static PyObject* hello_world(PyObject* self, PyObject* args) {
    return Py_BuildValue("s", "Hello World!");
}

/// detect if the game is over
static PyObject* game_over(PyObject* self, PyObject* args) {
    /// read the new board state from the python script
    PyObject* board_state = PyTuple_GetItem(args, 0);
    /// convert the python object to a 2d array of char
    for (int i = 0; i < 15; i++) {
        for (int j = 0; j < 15; j++) {
            board[i][j] = PyLong_AsLong(PyList_GetItem(board_state, i*15+j));
        }
    }
    return Py_BuildValue("i", get_victor());
}

int solve_alpha_beta(int player, int depth, int alpha, int beta, int last_x, int last_y) {
    // if the game is over
    // if the depth is MAX
    if (depth == MAX_DEPTH) {
        return evaluate_board(player);
    }
    int victor = get_victor();
    if (victor != -1) {
        // return victor *((MAX_DEPTH - depth)*(MAX_DEPTH - depth));
        // std::cout << "victor: " << victor << " "<<evaluate_board(player)<<" "<<evaluate_board(player)*((MAX_DEPTH+1 - depth)*(MAX_DEPTH+1 - depth))<<std::endl;
        // if (victor==player) {
        //     return evaluate_board(player)*((MAX_DEPTH+1 - depth)*(MAX_DEPTH+1 - depth));
        // } else {
        //     return -evaluate_board(player)*((MAX_DEPTH+1 - depth)*(MAX_DEPTH+1 - depth));
        // }
        return evaluate_board(1-player)*((MAX_DEPTH+1 - depth)*(MAX_DEPTH+1 - depth));
    }
    /// explore possible moves
    int best_score = -100000000;
    int score;
    int moves[8+widthN][2];
    // fll moves with -1
    for (int i = 0; i < 8+widthN; i++) {
        moves[i][0] = -1;
    }
    get_neighbours(moves,0,last_x,last_y);
    get_most_neighbors(moves,9,widthN);
    // for every possible move
    for (int i = 0; i < 8+widthN; i++) {
        if (moves[i][0] != -1) {
            // make the move
            board[moves[i][0]][moves[i][1]] = player;
            // update neighbour count
            add_neighbors(moves[i][0], moves[i][1]);
            // get the score
            score = -solve_alpha_beta(1-player, depth+1, -beta, -alpha, moves[i][0], moves[i][1]);
            // undo the move
            board[moves[i][0]][moves[i][1]] = -1;
            // update neighbour count
            sub_neighbors(moves[i][0], moves[i][1]);
            // if the score is better than the best score
            if (score > best_score) {
                best_score = score;
            }
            // if the score is better than the alpha
            if (score > alpha) {
                alpha = score;
            }
            // if the alpha is greater than the beta
            if (alpha >= beta) {
                break;
            }
        }
    }
    return best_score;
}

/// python function to evaluate the board
static PyObject* evaluate_board_py(PyObject* self, PyObject* args) {
    /// read the new board state from the python script
    PyObject* board_state = PyTuple_GetItem(args, 0);
    // get the player
    int player = PyLong_AsLong(PyTuple_GetItem(args, 1));
    /// convert the python object to a 2d array of char
    for (int i = 0; i < 15; i++) {
        for (int j = 0; j < 15; j++) {
            board[i][j] = PyLong_AsLong(PyList_GetItem(board_state, i*15+j));
        }
    }
    /// initialize the neighbour count array
    for (int i = 0; i < 15; i++) {
        for (int j = 0; j < 15; j++) {
            neighbour_count[i][j] = 0;
        }
    }
    /// count the number of neighbours for each cell
    for (int i = 0; i < 15; i++) {
        for (int j = 0; j < 15; j++) {
            if (board[i][j] != -1) {
                add_neighbors(i, j);
            }
        }
    }
    return Py_BuildValue("i", evaluate_board(player));
}

/// pythpn function to solve the game
static PyObject* solve(PyObject* self, PyObject* args) {
    /// read the new board state from the python script
    PyObject* board_state = PyTuple_GetItem(args, 0);
    //get the player
    int player = PyLong_AsLong(PyTuple_GetItem(args, 1));
    // get the last x and y
    int last_x = PyLong_AsLong(PyTuple_GetItem(args, 2));
    int last_y = PyLong_AsLong(PyTuple_GetItem(args, 3));
    // printf("got: p:%d x:%d y:%d\n",player, last_x, last_y);
    std::cout << "got: p:" << player << " x:" << last_x << " y:" << last_y << std::endl;
    /// convert the python object to a 2d array of char
    for (int i = 0; i < 15; i++) {
        for (int j = 0; j < 15; j++) {
            board[i][j] = PyLong_AsLong(PyList_GetItem(board_state, i*15+j));
        }
    }
    /// initialize the neighbour count array
    for (int i = 0; i < 15; i++) {
        for (int j = 0; j < 15; j++) {
            neighbour_count[i][j] = 0;
        }
    }
    /// count the number of neighbours for each cell
    for (int i = 0; i < 15; i++) {
        for (int j = 0; j < 15; j++) {
            if (board[i][j] != -1) {
                add_neighbors(i, j);
            }
        }
    }

    // // search for an easy dub
    // /// for every cell with count >0 and free on the board
    for (int i = 0; i < 15; i++) {
        for (int j = 0; j < 15; j++) {
            if (neighbour_count[i][j] > 0 && board[i][j] == -1) {
                // make the move
                board[i][j] = player;
                if (get_victor() == player) {
                    PyObject* move_list = PyList_New(0);
                    return Py_BuildValue("OO", move_list, Py_BuildValue("iii", 999, i, j));
                }
                // undo the move
                board[i][j] = -1;
            }
        }
    }

    /// solve the game

    /// explore possible moves
    int best_score = -1000000;
    int best_x = -1;
    int best_y = -1;
    int score;
    int moves[8+widthN1][2];
    // fll moves with -1
    for (int i = 0; i < 8+widthN1; i++) {
        moves[i][0] = -1;
        moves[i][1] = -1;
    }
    get_neighbours(moves,0,last_x,last_y);
    get_most_neighbors(moves,9,widthN1);
    // create a list of tuples to return
    PyObject* move_list = PyList_New(8+widthN1);
    // fill the list with the moves
    for (int i = 0; i < 8+widthN1; i++) {
            PyList_SetItem(move_list, i, Py_BuildValue("(ii)", moves[i][0], moves[i][1]));
    }
    // for every possible move
    int alpha = ALPHA;
    int beta = BETA;
    std::cout << "compute space is: " << widthN1*std::pow((8 + widthN), MAX_DEPTH) << std::endl;
    // for (int i = 0; i < 8+widthN1; i++) {
    // for each empty cell with a neighbour
    for (int i = 0; i < 15; i++) {
        for (int j = 0; j < 15; j++) {
            if (board[i][j] == -1 && neighbour_count[i][j] > 0) {
                // make the move
                // std::cout << "\n" << i << "/" << 8+widthN1;
                // std::cout << "  "<<moves[i][0] << "," << moves[i][1] << std::endl;
                // make the move
                board[i][j] = player;
                // update neighbour count
                add_neighbors(i, j);
                // get the score
                score = -solve_alpha_beta(1-player, 0, -beta, -alpha, i, j);
                // undo the move
                board[i][j] = -1;
                // update neighbour count
                sub_neighbors(i, j);
                // if the score is better than the best score
                if (score > best_score) {
                    best_score = score;
                    best_x = i;
                    best_y = j;
                }
                // if the score is better than the alpha
                if (score > alpha) {
                    alpha = score;
                }
                // if the alpha is greater than the beta
                if (alpha >= beta) {
                    break;
                }
            }
        }
    }
    
    std::cout << std::endl << "best score: " << best_score << std::endl;
    std::cout << "best x: " << best_x << std::endl;
    std::cout << "best y: " << best_y << std::endl;
    // create a tuple of 3 ints: (score, row, column)
    PyObject* values =  Py_BuildValue("iii", best_score, best_x, best_y);
    // return the tuple of the list and the values
    return Py_BuildValue("OO", move_list, values);
}

static PyMethodDef gommoku_methods[] = {
    /// list of all user accessible functions and their arguments
    /// order is 
    /// name, function, args, return type
    {
        "hello_world",
        hello_world,
        METH_VARARGS,
        "Return a string 'Hello World!'",
    },
    {
        "game_over",
        game_over,
        METH_VARARGS,
        "Return the winner of the game",
    },
    {
        "solve",
        solve,
        METH_VARARGS,
        "Return the best move",
    },
    {
        "evaluate_board",
        evaluate_board_py,
        METH_VARARGS,
        "Return the score of the board",
    },
    {NULL, NULL, 0, NULL},  // sentinel
};


static PyModuleDef gommoku_module = {
    PyModuleDef_HEAD_INIT,
    "gommoku",
    "An example Python C extension module.",
    -1,
    gommoku_methods,
};

PyMODINIT_FUNC PyInit_gommoku() {
    PyObject* module;

    module = PyModule_Create(&gommoku_module);
    if (module == NULL) {
        return NULL;
    }
    myError = PyErr_NewException("spam.Error", NULL, NULL);
    Py_INCREF(myError);
    PyModule_AddObject(module, "Error", myError);
    return module;
}

