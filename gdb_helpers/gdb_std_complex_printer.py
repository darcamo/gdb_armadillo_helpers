import cmath
import math


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
        self.c = complex(self.real_part, self.imag_part)

    def to_string(self):
        angle = 180.0 * cmath.phase(self.c) / math.pi
        sign = "+" if self.imag_part >= 0 else "-"
        return "{0:.4} {1} {2:.4}i ({3:.2}:{4:.2}°)".format(float(self.real_part), sign, abs(float(self.imag_part)), abs(self.c), angle)



import gdb.printing
pp = gdb.printing.RegexpCollectionPrettyPrinter('std::complex')
pp.add_printer('std::complex<int>', '^std::complex<int>', StdComplexIntPrinter)
pp.add_printer('std::complex<double>', '^std::complex<double>', StdComplexDoublePrinter)
gdb.printing.register_pretty_printer(gdb.current_objfile(), pp, replace=True)
