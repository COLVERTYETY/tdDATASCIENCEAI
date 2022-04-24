#include "/usr/include/python3.10/Python.h"

#include <stdlib.h>


static PyObject* customError;

static PyObject* working_module(PyObject* self, PyObject* args) {
    return Py_BuildValue("s", "Hello, World!");
}

static PyMethodDef customMethods[] = {
    {"working_module", working_module, METH_VARARGS, "Prints 'Hello, World!'"},
    {NULL, NULL, 0, NULL},  // sentinel
};

static PyModuleDef custommodule = {
    PyModuleDef_HEAD_INIT,
    "spam",
    "An example Python C extension module.",
    -1,
    customMethods,
};

PyMODINIT_FUNC PyInit_custom() {
    PyObject* module;

    module = PyModule_Create(&custommodule);
    if (module == NULL) {
        return NULL;
    }
    customError = PyErr_NewException("custom.Error", NULL, NULL);
    Py_INCREF(customError);
    PyModule_AddObject(module, "Error", customError);
    return module;
}
