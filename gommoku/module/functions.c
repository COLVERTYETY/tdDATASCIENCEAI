#include "/usr/include/python3.10/Python.h"

#include <stdlib.h>

/// 2d array of char to hold the game board, 12*12
int board[12][12];


static PyObject* myError;

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

