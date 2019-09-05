import gdb
import gdb.xmethod

# xmethod for the empty method in armadillo
#
# This class only acts as a descriptor and it has a `name` and a `enabled` attribute. We add a `get_worker` method that
# we can use in the Matcher class.
class ArmaMat_empty(gdb.xmethod.XMethod):
    def __init__(self):
        gdb.xmethod.XMethod.__init__(self, 'empty')

    def get_worker(self, method_name):
        if method_name == 'empty':
            return ArmaMatWorker_empty()

# class ArmaMat_operator_parentheses(gdb.xmethod.XMethod):
#     def __init__(self):
#         gdb.xmethod.XMethod.__init__(self, 'operator()')

#     def get_worker(self, method_name):
#         if method_name == 'operator()':
#             return ArmaMatWorker_operator_parentheses()


class ArmaMatMatcher(gdb.xmethod.XMethodMatcher):
    def __init__(self):
        gdb.xmethod.XMethodMatcher.__init__(self, 'ArmaMatMatcher')
        # List of methods 'managed' by this matcher
        self.methods = [
            ArmaMat_empty(),
            #ArmaMat_operator_parentheses()
        ]

    # This method should return an XMethodWorker object, or a sequence of 'XMethodWorker' objects. Only those xmethod
    # workers whose corresponding 'XMethod' descriptor object is enabled should be returned.
    def match(self, class_type, method_name):
        # if class_type.tag != 'class arma::Mat<double>::fixed<3, 3>':
        #     return None
        workers = []
        for method in self.methods:
            if method.enabled:
                worker = method.get_worker(method_name)
                if worker:
                    workers.append(worker)

        return workers



class ArmaMatWorker_empty(gdb.xmethod.XMethodWorker):
    def get_arg_types(self):
        """
        A sequence of gdb.Type objects corresponding to the arguments of the xmethod are returned. If the xmethod takes no
        arguments, then 'None' or an empty sequence is returned.
        """
        return None

    def get_result_type(self, obj):
        """
        Return the type of the result of the xmethod.

        Returns:
            A gdb.Type object representing the type of the result of the
            xmethod.
        """
        return gdb.lookup_type('void')

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


# class ArmaMatWorker_operator_parentheses(gdb.xmethod.XMethodWorker):
#     def get_arg_types(self):
#         return None

#     def get_result_type(self, obj):
#         return gdb.lookup_type('double')

#     def __call__(self, obj, idx):
#         return obj['operator()']

gdb.xmethod.register_xmethod_matcher(None, ArmaMatMatcher())
