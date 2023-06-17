#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <funchook.h>
binaryfunc unicode_concat_origin;
void (*unicode_append_origin)(PyObject **l, PyObject *r);
PyObject *apply_hook(PyObject *self, PyObject *arg);

static PyMethodDef methods[] = {
        {"apply_hook",
                (PyCFunction)apply_hook,
                METH_NOARGS,
                ""},
        {NULL, NULL, 0, NULL}
};

static struct PyModuleDef fh_hook_definition = {
        PyModuleDef_HEAD_INIT,
        "fh_hook",
        "description here",
        -1,
        methods,
        NULL,
        NULL,
        NULL,
        NULL};

PyMODINIT_FUNC PyInit_fh_hook(void) {
    return PyModule_Create(&fh_hook_definition);
}

PyObject *unicode_concat_new(PyObject *l, PyObject *r) {
    // do something
    printf("OK, append is hooked\n");
    PyObject *result = unicode_concat_origin(l, r);

    if (result == NULL) {
        return result;
    }

    return result;
}

void unicode_append_new(PyObject **l, PyObject *r) {
    // do something
    printf("OK, append is hooked\n");
    PyObject *origin_l = *l;
    Py_XINCREF(origin_l);
    unicode_append_origin(l, r);

    if (*l == NULL) {
        Py_XDECREF(origin_l);
        return;
    }

    Py_XDECREF(origin_l);
}


PyObject *apply_hook(PyObject *self, PyObject *arg) {
    funchook_t *funchook = funchook_create();
    int rv;

    unicode_concat_origin = PyUnicode_Concat;
    rv = funchook_prepare((funchook), (void **)(&unicode_concat_origin), (void *)(unicode_concat_new));
    if (rv != 0) {
        /* error */
        printf("hook concat error!\n");
    }

    unicode_append_origin = PyUnicode_Append;
    rv = funchook_prepare((funchook),  (void **)(&unicode_append_origin), (void *)(unicode_append_new));
    if (rv != 0) {
        /* error */
        printf("hook append error!\n");
    }

    rv = funchook_install(funchook, 0);
    if(rv!=0){
        printf("funchook_install error!\n");
    }
    Py_RETURN_NONE;
}
