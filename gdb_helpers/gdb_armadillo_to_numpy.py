import numpy as np


def _cast_to_complex(gdb_value):
    """
    Cast a gdb.Value containing a std::complex<double> number into a python
    complex number.

    Parameters
    ----------
    gdb_value : gdb.Value
        The gdb.Value object containing the complex number

    Returns
    -------
    complex
        The python complex number
    """
    double_t = gdb.lookup_type('double')
    # We need to cast gdb_value into an array of two doubles. Then we can
    # access the real and imaginary parts as the first and second elements
    real_and_imag_parts = gdb_value.cast(double_t.array(1))
    return complex(real_and_imag_parts[0], real_and_imag_parts[1])


def _get_list_of_elements(arma_container):
    """
    Get a list containing all elements in the arma_container.

    Parameters
    ----------
    arma_container : gdb.Value
        A gdb.Value object containing an armadillo type.

    Returns
    -------
    list[gdb.Value], list[complex]
        A list of gdb.Value objects containing the individual elements. If the
        armadillo container is of complex type, then a list of complex numbers
        is returned instead.
    """
    n_elem = arma_container["n_elem"]
    mem = arma_container["mem"]
    elem_type = mem.type.target().unqualified()

    if 'complex' in elem_type.name:
        return [_cast_to_complex(mem[i]) for i in range(n_elem)]

    return [mem[i] for i in range(n_elem)]


# Note: You can use this method from python interactive inside gdb
def get_array(arma_container):
    """
    Get a numpy array with the elements and shape of arma_container.

    Parameters
    ----------
    arma_container : gdb.Value, str
        A `gdb.Value` object containing an armadillo type or a variable name
        from which we can obtain a `gdb.Value` using `gdb.parse_and_eval`

    Returns
    -------
    np.ndarray
        A numpy array with the elements and the same shape as the provided
        arma_container.
    """
    if isinstance(arma_container, str):
        arma_container = gdb.parse_and_eval(arma_container)

    n_rows = arma_container["n_rows"]
    n_cols = arma_container["n_cols"]
    n_elem = arma_container["n_elem"]
    mem = arma_container["mem"]
    elem_type = mem.type.target().unqualified()

    elem_type_to_numpy_types = {
        "double": np.float64,
        "std::complex<double>": np.complex128,
        "unsigned long long": np.uint64,
        "long long": np.int64
    }

    vector_classes = ["arma::vec", "arma::uvec", "arma::cx_vec", "arma::ivec"]
    matrix_classes = [
        "arma::mat", "arma::umat", "arma::cx_mat", "arma::imat",
        "arma::Mat<double>"
    ]
    cube_classes = [
        "arma::cube", "arma::ucube", "arma::cx_cube", "arma::icube"
    ]

    if arma_container.type.name in vector_classes:
        shape = (n_elem)
        dtype = elem_type_to_numpy_types[elem_type.name]

    if arma_container.type.name in matrix_classes:
        shape = (n_rows, n_cols)
        dtype = elem_type_to_numpy_types[elem_type.name]
    if arma_container.type.name in cube_classes:
        n_slices = arma_container["n_slices"]
        shape = (n_rows, n_cols, n_slices)
        dtype = elem_type_to_numpy_types[elem_type.name]

    return np.array(_get_list_of_elements(arma_container),
                    dtype=dtype,
                    order='F').reshape(shape, order='F')


# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# xxxxxxxxxxxxxxx Custom GDB commands xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


# Inspired from
# https://interrupt.memfault.com/blog/automate-debugging-with-gdb-python-api
class PrintNumpyArrayCommand(gdb.Command):
    """
    Class implementing the gdb command 'print-numpy-array'.

    This command can be called from gdb prompt and will have completion for all
    armadillo type variables in the current scope.
    """
    def __init__(self):
        super().__init__("print-numpy-array", gdb.COMMAND_USER)

    def complete(self, text, word):  # pylint: disable=W0613, C0111, R0201
        # The comment return below would return all available symbols,
        # including internal ones and variables which are not armadillo type
        #
        # return gdb.COMPLETE_SYMBOL

        # See https://stackoverflow.com/questions/30013252/get-all-global-variables-local-variables-in-gdbs-python-interface
        # Get the current selected frame
        frame = gdb.selected_frame()
        # A 'block' represents the current scope
        block = frame.block()

        # We can iterate over a block to get the list of symbols
        #
        # If we return this list of symbols, then our command will only
        # complete for these symbols. We return the names of all variables in
        # the current scope which are armadillo variables
        return [
            i.name for i in block
            if i.type.name is not None and i.type.name[:6] == 'arma::'
        ]

    def invoke(self, args, from_tty):
        argsv = gdb.string_to_argv(args)
        if len(argsv) > 1:
            for variable in argsv:
                print(f'{variable}:\n',
                      get_array(variable))
        else:
            print(get_array(argsv[0]))


PrintNumpyArrayCommand()

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# if __name__ == '__main__':
#     v1 = gdb.parse_and_eval("v1")
#     v2 = gdb.parse_and_eval("v2")
#     v3 = gdb.parse_and_eval("v3")
#     v4 = gdb.parse_and_eval("v4")

#     m1 = gdb.parse_and_eval("m1")
#     m2 = gdb.parse_and_eval("m2")
#     m3 = gdb.parse_and_eval("m3")
#     m4 = gdb.parse_and_eval("m4")

#     u1 = gdb.parse_and_eval("u1")
#     u2 = gdb.parse_and_eval("u2")
#     u3 = gdb.parse_and_eval("u3")
#     u4 = gdb.parse_and_eval("u4")

#     print(_get_list_of_elements(m1))

#     print("v1:\n", get_array(v1))
#     print("v2:\n", get_array(v2))
#     print("v3:\n", get_array(v3))
#     print("v4:\n", get_array(v4))
#     print()

#     print("m1:\n", get_array(m1))
#     print("m2:\n", get_array(m2))
#     print("m3:\n", get_array(m3))
#     print("m4:\n", get_array(m4))
#     print()

#     print("u1:\n", get_array(u1))
#     print("u2:\n", get_array(u2))
#     print("u3:\n", get_array(u3))
#     print("u4:\n", get_array(u4))

# # TIP: In GDB, run interactive python with `pi` command then in the python prompt run
# # exec(open("../../gdb_helpers/gdb_armadillo_to_numpy.py").read())
