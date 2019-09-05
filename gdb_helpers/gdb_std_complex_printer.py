

class StdComplexIntPrinter:
    """
    Print std::complex<int> without the annoying _M_value
    """
    def __init__(self, val):
        self.real_part = val["_M_real"]
        self.imag_part = val["_M_imag"]

    def to_string(self):
        if self.imag_part >= 0:
            return "{0} + {1}i".format(self.real_part, self.imag_part)
        return "{0} - {1}i".format(self.real_part, abs(self.imag_part))


class StdComplexDoublePrinter:
    """
    Print std::complex<double> without the annoying _M_value
    """
    def __init__(self, val):
        self.val = val.cast(gdb.lookup_type("double").array(1))
        self.real_part = self.val[0]
        self.imag_part = self.val[1]

    def to_string(self):
        if self.imag_part >= 0:
            return "{0} + {1}i".format(self.real_part, self.imag_part)
        return "{0} - {1}i".format(self.real_part, abs(self.imag_part))



import gdb.printing
pp = gdb.printing.RegexpCollectionPrettyPrinter('std::complex')
pp.add_printer('std::complex<int>', '^std::complex<int>', StdComplexIntPrinter)
pp.add_printer('std::complex<double>', '^std::complex<double>', StdComplexDoublePrinter)
gdb.printing.register_pretty_printer(gdb.current_objfile(), pp, replace=True)
