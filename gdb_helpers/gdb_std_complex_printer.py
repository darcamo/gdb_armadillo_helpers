import cmath
import math

import gdb.printing


class ShowComplexNumberInPolar(gdb.Parameter):
    """
    When complex-show-polar is enabled (default) the std::complex
    pretty-printer will print the complex number also in polar form. When disabled
    only the rectangular form is printed.
    """

    set_doc = "Enable/disable the complex-show-polar parameter."
    show_doc = "Show the value of complex-show-polar"

    def __init__(self):
        super().__init__("complex-show-polar", gdb.COMMAND_NONE,
                         gdb.PARAM_BOOLEAN)
        self.value = True

    def get_set_string(self):
        if self.value:
            return "complex-show-polar is enabled"
        else:
            return "complex-show-polar is disabled"

    def get_show_string(self, svalue):
        return f"complex-show-polar is set to {svalue}"


complex_show_polar = ShowComplexNumberInPolar()
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


class StdComplexIntPrinter:
    """
    Print std::complex<int> without the annoying _M_value
    """
    def __init__(self, val):
        self.real_part = val["_M_real"]
        self.imag_part = val["_M_imag"]
        self.c = complex(self.real_part, self.imag_part)

    def to_string(self):
        real_sign = " " if self.real_part >= 0 else "-"
        imag_sign = "+" if self.imag_part >= 0 else "-"

        real_part = "{0}{1} {2} {3}i".format(real_sign, abs(self.real_part),
                                             imag_sign, abs(self.imag_part))

        angle = 180.0 * cmath.phase(self.c) / math.pi

        if complex_show_polar.value:
            imag_part = " ({0:.2f} ⦞ {1:.2f}°)".format(abs(self.c), angle)
            return real_part + imag_part

        return real_part


class StdComplexDoublePrinter:
    """
    Print std::complex<double> without the annoying _M_value
    """
    def __init__(self, val):
        # Cast to an array of two doubles, where the first one is the real part
        # and the second one is the imaginary part.
        val = val.cast(gdb.lookup_type("double").array(1))
        self.real_part = val[0]
        self.imag_part = val[1]
        self.c = complex(self.real_part, self.imag_part)

    def to_string(self):
        angle = 180.0 * cmath.phase(self.c) / math.pi
        real_sign = " " if self.real_part >= 0 else "-"
        imag_sign = "+" if self.imag_part >= 0 else "-"

        real_part = "{0}{1:.4f} {2} {3:.4f}i".format(
            real_sign, abs(float(self.real_part)), imag_sign,
            abs(float(self.imag_part)))

        if complex_show_polar.value:
            imag_part = " ({0:.2f} ⦞ {1:.2f}°)".format(abs(self.c), angle)
            return real_part + imag_part

        return real_part

        # return "{0}{1:.4f} {2} {3:.4f}i ({4:.2f} ⦞ {5:.2f}°)".format(real_sign, abs(float(self.real_part)), imag_sign, abs(float(self.imag_part)), abs(self.c), angle)


pp = gdb.printing.RegexpCollectionPrettyPrinter('std::complex')
pp.add_printer('std::complex<int>', '^std::complex<int>', StdComplexIntPrinter)
pp.add_printer('std::complex<double>', '^std::complex<double>',
               StdComplexDoublePrinter)
gdb.printing.register_pretty_printer(gdb.current_objfile(), pp, replace=True)
