import re
from itertools import product

# Register the pretty printers
import gdb.printing


class ShowArmaContentParameter(gdb.Parameter):
    """
When arma-show-content is enabled (default) the armadillo pretty-printers
will print the elements of armadillo vectors, matrices and cubes. When
disabled only the dimension of the container are printed.
    """

    set_doc = "Enable/disable the arma-show-content parameter."
    show_doc = "Show the value of arma-show-content"

    def __init__(self):
        super().__init__("arma-show-content", gdb.COMMAND_NONE,
                         gdb.PARAM_BOOLEAN)
        self.value = True

    def get_set_string(self):
        if self.value:
            return "arma-show-content is enabled"
        else:
            return "arma-show-content is disabled"

    def get_show_string(self, svalue):
        return f"arma-show-content is set to {svalue}"


arma_show_content = ShowArmaContentParameter()
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


class ArmaPrettyPrinterBase:
    def __init__(self, val):
        self.val = val
        self.mem = val['mem']
        # This can be used in subclasses when implementing next_element method
        # to cast self.mem to some appropriated type
        self.elem_type = self.mem.type.target().unqualified()

        # In case 'val' is a fixed size matrix if we try to get the n_rows,
        # n_cols and n_elem fields gdb will complain that they were optimized
        # out. However, if we cast it to the corresponding non-fixed matrix we
        # can get these fields.
        mat_type = gdb.lookup_type(f"arma::Mat<{self.elem_type.name}>")
        val = val.cast(mat_type)
        self.n_rows = int(val['n_rows'])
        self.n_cols = int(val['n_cols'])
        self.n_elem = int(val['n_elem'])

    def to_string(self):
        raise RuntimeError("Implement-me")

    def next_element(self):
        raise RuntimeError("Implement-me")

    def children(self):
        if arma_show_content.value:
            return self.next_element()
        return []

    def display_hint(self):
        return "array"


class ArmaVecPrinter(ArmaPrettyPrinterBase):
    """
    Print a armadillo vectors

    @note Does not work very well with row vectors.
    """
    def __init__(self, val):
        super().__init__(val)

    def to_string(self):
        return f"{self.val.type}({self.n_elem})"

    def next_element(self):
        for i in range(self.n_elem):
            yield str(i), (self.mem + i).dereference()


class ArmaMatPrinter(ArmaPrettyPrinterBase):
    """Print a armadillo matrices"""
    def __init__(self, val):
        super().__init__(val)

    def get_column(self, col_idx):
        """
        Return the column with index `col_idx` as an array that gdb can pretty
        print.
        """
        # The column type is an array with `self.n_rows` elements
        column_type = self.elem_type.array(self.n_rows - 1)
        # Deference self.mem to get the first element in the column and then
        # cast it to be an array of elements. This will result in an array
        # containing all elements in the column
        column = ((self.mem +
                   col_idx * self.n_rows).dereference()).cast(column_type)

        return column

    def next_element(self):
        """
        Each 'element' is a column in the matrix, whose type is an array.

        Since gdb also pretty prints the element, the returned array
        representing the row will also be pretty printed.
        """
        for col_idx in range(self.n_cols):
            yield "Column " + str(col_idx), self.get_column(col_idx)

    def to_string(self):
        return f"{self.val.type}({self.n_rows},{self.n_cols})"


class ArmaCubePrinter(ArmaPrettyPrinterBase):
    """Print a armadillo matrices"""
    def __init__(self, val):
        super().__init__(val)
        # Cubes have an extra parameter called "n_slices"
        self.n_slices = val['n_slices']

    def get_slice(self, col_idx):
        """
        Return the column with index `col_idx` as an array that gdb can pretty
        print.
        """
        num_elements_per_slice = self.n_rows * self.n_cols

        # The column type is an array with `self.n_rows` elements
        column_type = self.elem_type.array(self.n_rows - 1)
        slice_type = column_type.array(self.n_cols - 1)
        # Deference self.mem to get the first element in the column and then
        # cast it to be an array of elements. This will result in an array
        # containing all elements in the column
        column = (
            (self.mem +
             col_idx * num_elements_per_slice).dereference()).cast(slice_type)

        return column

    def next_element(self):
        """
        Each 'element' is a column in the matrix, whose type is an array.

        Since gdb also pretty prints the element, the returned array
        representing the row will also be pretty printed.
        """
        for slice_idx in range(self.n_slices):
            yield "Slice " + str(slice_idx), self.get_slice(slice_idx)

    def to_string(self):
        return f"{self.val.type}({self.n_rows},{self.n_cols},{self.n_slices})"


pp = gdb.printing.RegexpCollectionPrettyPrinter('armadillo')
pp.add_printer('arma::Col', '^arma::Col', ArmaVecPrinter)
pp.add_printer('arma::Mat', '^arma::Mat', ArmaMatPrinter)
pp.add_printer('arma::Cuve', '^arma::Cube', ArmaCubePrinter)
gdb.printing.register_pretty_printer(gdb.current_objfile(), pp, replace=True)
