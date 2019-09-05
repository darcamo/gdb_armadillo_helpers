
# Try block has all the code here which depend on the gdb_numpy module
try:
    # Install this from https://github.com/TorosFanny/gdb_numpy
    import gdb_numpy

    # variable_name: name of the armadillo variable in gdb
    def get_memory_name(variable_name):
        return "{0}.mem_local".format(variable_name)


    def get_numpy_from_mat(variable_name):
        m = gdb.parse_and_eval(variable_name)
        n_cols = m["n_cols"]
        n_rows = m["n_rows"]

        return gdb_numpy.to_array("{0}.mem_local".format(variable_name))[:(n_cols*n_rows)].reshape(n_rows,n_cols,order="F")


    def print_mat(variable_name):
        print(get_numpy_from_mat(variable_name))

except Exception:
    print("WARNING: The gdb_numpy module is not installed -> The armadillo-to-numpy functions will not be available")
