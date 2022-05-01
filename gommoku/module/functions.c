#include "/usr/include/python3.10/Python.h"

#include <stdlib.h>

#define widthN 4
#define MAX_DEPTH 10
#define BETA 1000000
#define ALPHA -1000000

/// 2d array of char to hold the game board, 12*12
int board[12][12];
int neighbors[8][2] = {{-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 1}, {1, -1}, {1, 0}, {1, 1}};
int neighbour_count[12][12];

static PyObject* myError;

void add_neighbors(int x, int y) {
    int i, j;
    for (i = 0; i < 8; i++) {
        j = x + neighbors[i][0];
        int k = y + neighbors[i][1];
        if (j >= 0 && j < 12 && k >= 0 && k < 12) {
            neighbour_count[j][k] += 1;
        }
    }
}

void sub_neighbors(int x, int y) {
    int i, j;
    for (i = 0; i < 8; i++) {
        j = x + neighbors[i][0];
        int k = y + neighbors[i][1];
        if (j >= 0 && j < 12 && k >= 0 && k < 12) {
            neighbour_count[j][k] -= 1;
        }
    }
}

int get_stalemate() {
    int i, j;
    for (i = 0; i < 12; i++) {
        for (j = 0; j < 12; j++) {
            if (board[i][j] == -1) {
                return 0;
            }
        }
    }
    return 1;
}

void get_most_neighbors(int list[][2], int start) {
    int counts[widthN];
    int i, j;
    for (i = 0; i < widthN; i++) {
        counts[i] = 0;
    }
    // for every cell of the neighbor_count array
    for (i = 0; i < 12; i++) {
        for (j = 0; j < 12; j++) {
            // if the cell is not empty and has the highest neighbor count and not filled in the board
            if ((neighbour_count[i][j] > counts[0]) && (board[i][j] != -1)) {
                for(int l = 0; l < widthN; l++) {
                    if (neighbour_count[i][j] > counts[l]) {
                        // shift all the other counts down
                        for (int m = widthN - 1; m > l; m--) {
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

void get_neighbours(int list[][2], int start, int x, int y) {
    //for every neighbour of the cell
    for (int i = 0; i < 8; i++) {
        int j = x + neighbors[i][0];
        int k = y + neighbors[i][1];
        // if the neighbour is not out of bounds and not filled in the board
        if (j >= 0 && j < 12 && k >= 0 && k < 12 && board[j][k] != -1) {
            // add the neighbour to the list
            list[start+i][0] = j;
            list[start+i][1] = k;
        }
    }
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

int evaluate_board(int player) {
    int score = 0;
    // for every empty cell of the board with atleast one neighbor 
    for (int i = 0; i < 12; i++) {
        for (int j = 0; j < 12; j++) {
            if (neighbour_count[i][j] > 0 && board[i][j] == -1) {
                score += is_winning_move(i, j, player);
                score -= is_winning_move(i, j, (player+1)%2);
            }
        }
    }
    return score;
}

int get_victor(){
    /// detect if 4 or more of the same color are in a row
    // detect horizontal
    for (int i = 0; i < 12; i++) {
        for (int j = 0; j < 9; j++) {
            if (board[i][j] != -1 && board[i][j] == board[i][j+1] && board[i][j] == board[i][j+2] && board[i][j] == board[i][j+3]) {
                return  board[i][j];
            }
        }
    }
    // detect vertical
    for (int i = 0; i < 9; i++) {
        for (int j = 0; j < 12; j++) {
            if (board[i][j] != -1 && board[i][j] == board[i+1][j] && board[i][j] == board[i+2][j] && board[i][j] == board[i+3][j]) {
                return board[i][j];
            }
        }
    }
    // detect diagonal
    for (int i = 0; i < 9; i++) {
        for (int j = 0; j < 9; j++) {
            if (board[i][j] != -1 && board[i][j] == board[i+1][j+1] && board[i][j] == board[i+2][j+2] && board[i][j] == board[i+3][j+3]) {
                return board[i][j];
            }
        }
    }
    // detect other diagonal
    for (int i = 0; i < 9; i++) {
        for (int j = 3; j < 12; j++) {
            if (board[i][j]!=-1 && board[i][j] == board[i+1][j-1] && board[i][j] == board[i+2][j-2] && board[i][j] == board[i+3][j-3]) {
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
    for (int i = 0; i < 12; i++) {
        for (int j = 0; j < 12; j++) {
            board[i][j] = PyLong_AsLong(PyList_GetItem(board_state, i*12+j));
        }
    }
    return Py_BuildValue("i", get_victor());
}

int solve_alpha_beta(int player, int depth, int alpha, int beta, int last_x, int last_y) {
    // if the game is over
    int victor = get_victor();
    if (victor != -1) {
        return victor*((MAX_DEPTH - depth)*(MAX_DEPTH - depth));
    }
    // if the depth is MAX
    if (depth == MAX_DEPTH) {
        return evaluate_board(player);
    }
    /// explore possible moves
    int best_score = -1000000;
    int score;
    int moves[8+widthN][2];
    // fll moves with -1
    for (int i = 0; i < 8+widthN; i++) {
        moves[i][0] = -1;
    }
    get_neighbours(moves,0,last_x,last_y);
    get_most_neighbors(moves,9);
    // for every possible move
    for (int i = 0; i < 8+widthN; i++) {
        if (moves[i][0] != -1) {
            // make the move
            board[moves[i][0]][moves[i][1]] = player;
            // update neighbour count
            add_neighbors(moves[i][0], moves[i][1]);
            // get the score
            score = -solve_alpha_beta((player+1)%2, depth+1, -beta, -alpha, moves[i][0], moves[i][1]);
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
    for (int i = 0; i < 12; i++) {
        for (int j = 0; j < 12; j++) {
            board[i][j] = PyLong_AsLong(PyList_GetItem(board_state, i*12+j));
        }
    }
    /// initialize the neighbour count array
    for (int i = 0; i < 12; i++) {
        for (int j = 0; j < 12; j++) {
            neighbour_count[i][j] = 0;
        }
    }
    /// count the number of neighbours for each cell
    for (int i = 0; i < 12; i++) {
        for (int j = 0; j < 12; j++) {
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
    printf("got: p:%d x:%d y:%d\n",player, last_x, last_y);
    /// convert the python object to a 2d array of char
    for (int i = 0; i < 12; i++) {
        for (int j = 0; j < 12; j++) {
            board[i][j] = PyLong_AsLong(PyList_GetItem(board_state, i*12+j));
        }
    }
    /// initialize the neighbour count array
    for (int i = 0; i < 12; i++) {
        for (int j = 0; j < 12; j++) {
            neighbour_count[i][j] = 0;
        }
    }
    /// count the number of neighbours for each cell
    for (int i = 0; i < 12; i++) {
        for (int j = 0; j < 12; j++) {
            if (board[i][j] != -1) {
                add_neighbors(i, j);
            }
        }
    }
    printf("solving...\n");

    /// solve the game

    /// explore possible moves
    int best_score = -1000000;
    int best_x = -1;
    int best_y = -1;
    int score;
    int moves[8+widthN][2];
    // fll moves with -1
    for (int i = 0; i < 8+widthN; i++) {
        moves[i][0] = -1;
    }
    get_neighbours(moves,0,last_x,last_y);
    get_most_neighbors(moves,9);
    printf("got neighbours...\n");
    // for every possible move
    int alpha = ALPHA;
    int beta = BETA;
    for (int i = 0; i < 8+widthN; i++) {
        printf("\r%d/%d", i, 8+widthN);
        if (moves[i][0] != -1) {
            // make the move
            board[moves[i][0]][moves[i][1]] = player;
            // update neighbour count
            add_neighbors(moves[i][0], moves[i][1]);
            // get the score
            score = -solve_alpha_beta((player+1)%2, 0, -beta, -alpha, moves[i][0], moves[i][1]);
            // undo the move
            board[moves[i][0]][moves[i][1]] = -1;
            // update neighbour count
            sub_neighbors(moves[i][0], moves[i][1]);
            // if the score is better than the best score
            if (score > best_score) {
                best_score = score;
                best_x = moves[i][0];
                best_y = moves[i][1];
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
    
    return PyTuple_Pack(3,best_score,best_x,best_y); // return a tuple of 3 ints: (score, row, column)
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

