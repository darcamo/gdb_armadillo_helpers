# GDB Armadillo helpers

For now this mainly include pretty printers for vectors and matrices in the
[armadillo](http://arma.sourceforge.net/) library.

It also includes a pretty printer for `std::complex<int>` and `std::complex<double>`.


## Using these pretty printers

Clone this repository to some folder and add the code below to the .gdbinit in
your home folder

```gdb
source /path_where_you_cloned/gdb_armadillo_helpers/gdb_helpers/gdb_armadillo_printers.py
source /path_where_you_cloned/gdb_armadillo_helpers/gdb_helpers/gdb_std_complex_printer.py
source /path_where_you_cloned/gdb_armadillo_helpers/gdb_helpers/gdb_armadillo_xmethods.py
```

After that just use `p some_variable** in gdb to see the result.

**Note**: This also works inside CLion and possible in other IDEs.
