from itertools import product


class ShowArmaContentParameter(gdb.Parameter):
    """
When arma-show-content is enabled (default) the armadillo pretty-printers
will print the elements of armadillo vectors, matrices and cubes. When
disabled only the dimension of the container are printed.
    """

    set_doc = "Enable/disable the arma-show-content parameter."
    show_doc = "Show the value of arma-show-content"
    def __init__(self):
        super().__init__("arma-show-content", gdb.COMMAND_NONE, gdb.PARAM_BOOLEAN)
        self.value = True
        # self.show_doc = "the show doc"


    def get_set_string(self):
        if self.value:
            return "arma-show-content is enabled"
        else:
            return "arma-show-content is disabled"

    def get_show_string(self, svalue):
        return f"arma-show-content is set to {svalue}"

arma_show_content = ShowArmaContentParameter()


class ArmaVecPrinter:
    """
    Print a armadillo vectors

    @note Does not work very well with row vectors.
    """
    def __init__(self, val):
        self.val = val
        self.n_rows = val['n_rows']
        self.n_cols = val['n_cols']
        self.n_elem = val['n_elem']
        self.mem = val['mem']

    def to_string(self):
        return f"{self.val.type}({self.n_elem})"

    def next_element(self):
        for i in range(self.n_elem):
            yield str(i), (self.mem+i).dereference()

    def children(self):
        if arma_show_content.value:
            return self.next_element()
        return []

    def display_hint(self):
        return "array"


class ArmaMatPrinter:
    """Print a armadillo matrices"""

    def __init__(self, val):
        self.val = val
        self.n_rows = val['n_rows']
        self.n_cols = val['n_cols']
        self.n_elem = val['n_elem']
        # self.mem = val['mem']
        self.mem = val['mem']
        self.elem_type = self.mem.type.target().unqualified()

    def get_column(self, col_idx):
        """
        Return the column with index `col_idx` as an array that gdb can pretty
        print.
        """
        # The column type is an array with `self.n_rows` elements
        column_type = self.elem_type.array(self.n_rows-1)
        # Deference self.mem to get the first element in the column and then
        # cast it to be an array of elements. This will result in an array
        # containing all elements in the column
        column = ((self.mem+col_idx*self.n_rows).dereference()).cast(column_type)

        return column

    def next_element(self):
        """
        Each 'element' is a column in the matrix, whose type is an array.

        Since gdb also pretty prints the element, the returned array
        representing the row will also be pretty printed.
        """
        for col_idx in range(self.n_cols):
            yield "Column "+str(col_idx), self.get_column(col_idx)

    def to_string(self):
        return f"{self.val.type}({self.n_rows},{self.n_cols})"

    def children(self):
        if arma_show_content.value:
            return self.next_element()
        return []

    def display_hint(self):
        return "array"


class ArmaCubePrinter:
    """Print a armadillo matrices"""
    def __init__(self, val):
        self.val = val
        self.n_rows = val['n_rows']
        self.n_cols = val['n_cols']
        self.n_slices = val['n_slices']
        self.n_elem = val['n_elem']
        # self.mem = val['mem']
        self.mem = val['mem']
        self.elem_type = self.mem.type.target().unqualified()

    def get_slice(self, col_idx):
        """
        Return the column with index `col_idx` as an array that gdb can pretty
        print.
        """
        num_elements_per_slice = self.n_rows * self.n_cols

        # The column type is an array with `self.n_rows` elements
        column_type = self.elem_type.array(self.n_rows-1)
        slice_type = column_type.array(self.n_cols-1)
        # Deference self.mem to get the first element in the column and then
        # cast it to be an array of elements. This will result in an array
        # containing all elements in the column
        column = ((self.mem+col_idx*num_elements_per_slice).dereference()).cast(slice_type)

        return column

    def next_element(self):
        """
        Each 'element' is a column in the matrix, whose type is an array.

        Since gdb also pretty prints the element, the returned array
        representing the row will also be pretty printed.
        """
        for slice_idx in range(self.n_slices):
            yield "Slice "+str(slice_idx), self.get_slice(slice_idx)

    def to_string(self):
        return f"{self.val.type}({self.n_rows},{self.n_cols},{self.n_slices})"

    def children(self):
        if arma_show_content.value:
            return self.next_element()
        return []

    def display_hint(self):
        return "array"





import gdb.printing
pp = gdb.printing.RegexpCollectionPrettyPrinter('armadillo')
pp.add_printer('arma::Col', '^arma::Col', ArmaVecPrinter)
pp.add_printer('arma::Mat', '^arma::Mat', ArmaMatPrinter)
pp.add_printer('arma::Cuve', '^arma::Cube', ArmaCubePrinter)
gdb.printing.register_pretty_printer(gdb.current_objfile(), pp, replace=True)


