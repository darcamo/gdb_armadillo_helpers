import gdb
import gdb.xmethod

# Note: The code here got some inspiration from the xmethods implementations
# for standard library in
# https://github.com/gcc-mirror/gcc/blob/master/libstdc%2B%2B-v3/python/libstdcxx/v6/xmethods.py


# List of interesting methods to implement as xmethods
## Common to vec, mat and cube
#  - min, max, empty, index_min, index_max, size, at
#
## Specific to vectors:
# - subvec, head, tail
#
## Specific to matrices:
# - at, submat, row, col
#
## Specific to cubes:
# - at, slice, tube, col?, row?




# An XMethod class only acts as a descriptor and it has a `name` and a
# `enabled` attribute. We add a `get_worker` method that we can use in the
# Matcher class.

# The XMethodMatcher class has a "match" method that receives a "class_type" (use
# class_type.tag to get class name as string) and a "method_name" argument. It
# must return a list of XMethodWorker classes corresponding to overloads of the
# desired method. Return an empty list if the class does not match the correct
# class.


# The XMethodWorker is in charge of actually implementing the desired
# functionality. It has the following methods: 'get_arg_types', and '__call__'


# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
class ArmaXMethod_common(gdb.xmethod.XMethod):
    """
    Class for implementing XMethods that are common for armadillo vec, mat and
    cube.
    """
    def __init__(self, name, worker_class):
        gdb.xmethod.XMethod.__init__(self, name)
        self.__worker_class = worker_class

    def get_worker(self, method_name):
        if method_name == self.name:
            return self.__worker_class()
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
class ArmaMatcher(gdb.xmethod.XMethodMatcher):
    """
    Matcher that matches vectors, matrices and cubes.

    Add here workers that are the same for all three cases.
    """
    def __init__(self):
        gdb.xmethod.XMethodMatcher.__init__(self, 'ArmaMatcher')
        # List of methods 'managed' by this matcher
        self.methods = [
            ArmaXMethod_common("empty", ArmaEmptyWorker),
            ArmaXMethod_common("size", ArmaSizeWorker),
            ArmaXMethod_common("min", ArmaMinWorker),
            ArmaXMethod_common("max", ArmaMaxWorker),
        ]

    # This method should return an XMethodWorker object, or a sequence of
    # 'XMethodWorker' objects. Only those xmethod workers whose corresponding
    # 'XMethod' descriptor object is enabled should be returned.
    def match(self, class_type, method_name):
        short_class_type_name = class_type.tag[:10]
        if short_class_type_name != 'arma::Mat<' and short_class_type_name != "arma::Vec<" and short_class_type_name != "arma::Cube":
            return None
        workers = []
        for method in self.methods:
            if method.enabled:
                worker = method.get_worker(method_name)
                if worker:
                    workers.append(worker)

        return workers


class ArmaVecMatcher(gdb.xmethod.XMethodMatcher):
    """
    Matcher that matches vectors.

    Add here workers that are specific to vectors.
    """
    def __init__(self):
        gdb.xmethod.XMethodMatcher.__init__(self, 'ArmaVecMatcher')
        # List of methods 'managed' by this matcher
        self.methods = [
            ArmaXMethod_common("at", ArmaVecAtWorker),
        ]

    # This method should return an XMethodWorker object, or a sequence of
    # 'XMethodWorker' objects. Only those xmethod workers whose corresponding
    # 'XMethod' descriptor object is enabled should be returned.
    def match(self, class_type, method_name):
        short_class_type_name = class_type.tag[:10]
        if short_class_type_name != "arma::Col<":
            return None

        workers = []
        for method in self.methods:
            if method.enabled:
                worker = method.get_worker(method_name)
                if worker:
                    workers.append(worker)

        return workers


class ArmaMatMatcher(gdb.xmethod.XMethodMatcher):
    """
    Matcher that matches matrices.

    Add here workers that are specific to matrices.
    """
    def __init__(self):
        gdb.xmethod.XMethodMatcher.__init__(self, 'ArmaMatMatcher')
        # List of methods 'managed' by this matcher
        self.methods = [
            ArmaXMethod_common("at", ArmaVecAtWorker), # The 'vec' worker is for 1d access
            ArmaXMethod_common("at", ArmaMatAtWorker), # The 'vec' worker is for 2d access
        ]

    # This method should return an XMethodWorker object, or a sequence of
    # 'XMethodWorker' objects. Only those xmethod workers whose corresponding
    # 'XMethod' descriptor object is enabled should be returned.
    def match(self, class_type, method_name):
        short_class_type_name = class_type.tag[:10]
        if short_class_type_name != "arma::Mat<":
            return None

        workers = []
        for method in self.methods:
            if method.enabled:
                worker = method.get_worker(method_name)
                if worker:
                    workers.append(worker)

        return workers


class ArmaCubeMatcher(gdb.xmethod.XMethodMatcher):
    """
    Matcher that matches cubes.

    Add here workers that are specific to cubes.
    """
    def __init__(self):
        gdb.xmethod.XMethodMatcher.__init__(self, 'ArmaCubeMatcher')
        # List of methods 'managed' by this matcher
        self.methods = [
            ArmaXMethod_common("at", ArmaVecAtWorker),  # The 'vec' worker is for 1d access
            ArmaXMethod_common("at", ArmaCubeAtWorker), # The 'vec' worker is for 3d access
            ArmaXMethod_common("slice", ArmaCubeSliceWorker), # Returns a 2D array
        ]

    # This method should return an XMethodWorker object, or a sequence of
    # 'XMethodWorker' objects. Only those xmethod workers whose corresponding
    # 'XMethod' descriptor object is enabled should be returned.
    def match(self, class_type, method_name):
        short_class_type_name = class_type.tag[:10]
        if short_class_type_name != "arma::Cube":
            return None

        workers = []
        for method in self.methods:
            if method.enabled:
                worker = method.get_worker(method_name)
                if worker:
                    workers.append(worker)

        return workers
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# Base class for XMethodWorker classes for methods that do not receive any
# argument
class ArmaWorker_noarg_base(gdb.xmethod.XMethodWorker):
    def get_arg_types(self):
        """
        A sequence of gdb.Type objects corresponding to the arguments of the xmethod are returned. If the xmethod takes no
        arguments, then 'None' or an empty sequence is returned.
        """
        return None

    def __call__(self, obj):
        raise RuntimeError("Implement-me")


class ArmaEmptyWorker(ArmaWorker_noarg_base):
    def __call__(self, obj):
        """Invoke the xmethod

        Args:
            args: Arguments to the method.  Each element of the tuple is a
                gdb.Value object.  The first element is the 'this' pointer
                value.

        Returns:
            A gdb.Value corresponding to the value returned by the xmethod.
            Returns 'None' if the method does not return anything.
        """
        return obj['n_elem'] == 0


class ArmaSizeWorker(ArmaWorker_noarg_base):
    def __call__(self, obj):
        """Invoke the xmethod

        Args:
            args: Arguments to the method.  Each element of the tuple is a
                gdb.Value object.  The first element is the 'this' pointer
                value.

        Returns:
            A gdb.Value corresponding to the value returned by the xmethod.
            Returns 'None' if the method does not return anything.
        """
        return obj['n_elem']


class ArmaMinWorker(ArmaWorker_noarg_base):
    def __call__(self, obj):
        """Invoke the xmethod

        Args:
            args: Arguments to the method.  Each element of the tuple is a
                gdb.Value object.  The first element is the 'this' pointer
                value.

        Returns:
            A gdb.Value corresponding to the value returned by the xmethod.
            Returns 'None' if the method does not return anything.
        """
        num_elem = obj['n_elem']
        mem = obj["mem"]
        try:
            min_value = min((mem + i).dereference() for i in range(num_elem))
        except gdb.error:
            raise gdb.error("Error in gdb xmethod implementation for 'min' method")
        return min_value


class ArmaMaxWorker(ArmaWorker_noarg_base):
    def __call__(self, obj):
        """Invoke the xmethod

        Args:
            args: Arguments to the method.  Each element of the tuple is a
                gdb.Value object.  The first element is the 'this' pointer
                value.

        Returns:
            A gdb.Value corresponding to the value returned by the xmethod.
            Returns 'None' if the method does not return anything.
        """
        num_elem = obj['n_elem']
        mem = obj["mem"]
        try:
            max_value = max((mem + i).dereference() for i in range(num_elem))
        except gdb.error:
            raise gdb.error("Error in gdb xmethod implementation for 'max' method")
        return max_value
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
class ArmaVecAtWorker(gdb.xmethod.XMethodWorker):
    def get_arg_types(self):
        return gdb.lookup_type('int')

    def __call__(self, obj, index):
        if index < 0 or index >= obj["n_elem"]:
            raise gdb.error(f"Cannot get element with index {index} from {obj.type.target()} with {obj['n_elem']} elements")
        return obj["mem"][index]


class ArmaMatAtWorker(gdb.xmethod.XMethodWorker):
    def get_arg_types(self):
        return [gdb.lookup_type('int'), gdb.lookup_type('int')]

    def __call__(self, obj, row_idx, col_idx):
        n_rows = obj["n_rows"]
        n_cols = obj["n_cols"]
        if row_idx < 0 or row_idx >= n_rows:
            raise gdb.error(f"Row index out of bounds -> It must be between 0 and {n_rows-1}")
        if col_idx < 0 or col_idx >= n_cols:
            raise gdb.error(f"Column index out of bounds -> It must be between 0 and {n_cols-1}")
        return obj["mem"][col_idx*n_rows + row_idx]


class ArmaCubeAtWorker(gdb.xmethod.XMethodWorker):
    def get_arg_types(self):
        return [gdb.lookup_type('int'), gdb.lookup_type('int'), gdb.lookup_type('int')]

    def __call__(self, obj, row_idx, col_idx, slice_idx):
        n_rows = obj["n_rows"]
        n_cols = obj["n_cols"]
        n_slices = obj["n_slices"]
        num_elem_per_slice = n_rows * n_cols
        if row_idx < 0 or row_idx >= n_rows:
            raise gdb.error(f"Row index out of bounds -> It must be between 0 and {n_rows-1}")
        if col_idx < 0 or col_idx >= n_cols:
            raise gdb.error(f"Column index out of bounds -> It must be between 0 and {n_cols-1}")
        if slice_idx < 0 or slice_idx >= n_slices:
            raise gdb.error(f"Slice index out of bounds -> It must be between 0 and {n_slices-1}")
        return obj["mem"][slice_idx * num_elem_per_slice + col_idx*n_rows + row_idx]


class ArmaCubeSliceWorker(gdb.xmethod.XMethodWorker):
    @staticmethod
    def get_slice_type(obj):
        n_rows = obj["n_rows"]
        n_cols = obj["n_cols"]
        elem_type = obj["mem"].type.target().unqualified()
        column_type = elem_type.array(n_rows-1)
        slice_type = column_type.array(n_cols-1)

        return slice_type

    def get_arg_types(self):
        return gdb.lookup_type('int')

    def __call__(self, obj, slice_idx):
        n_rows = obj["n_rows"]
        n_cols = obj["n_cols"]
        n_slices = obj["n_slices"]
        num_elem_per_slice = n_rows * n_cols

        if slice_idx < 0 or slice_idx >= n_slices:
            raise gdb.error(f"Slice index out of bounds -> It must be between 0 and {n_slices-1}")

        slice_type = self.get_slice_type(obj)

        return (obj["mem"][slice_idx * num_elem_per_slice]).cast(slice_type)



# xxxxxxxxxx Register the xmethods matcher xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
gdb.xmethod.register_xmethod_matcher(None, ArmaMatcher())
gdb.xmethod.register_xmethod_matcher(None, ArmaVecMatcher())
gdb.xmethod.register_xmethod_matcher(None, ArmaMatMatcher())
gdb.xmethod.register_xmethod_matcher(None, ArmaCubeMatcher())
