#include <armadillo>
#include <iostream>

#if defined(ARMA_USE_EXTERN_CXX11_RNG)
namespace arma {
thread_local arma_rng_cxx11 arma_rng_cxx11_instance;  // NOLINT
}  // namespace arma
#endif


int main() {
  int a[10] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};

  std::complex<int> c1(1,-3);
  std::complex<double> c2(1.5,-3.3);
  std::complex<double> c3(1.5, 3.3);

  arma::mat m1{{1.1, 2.2, 3}, {4, 5, 6}, {7, 8, 9}, {10, 11, 12}, {13, 14, 15}, {16, 17, 18}};
  arma::cx_mat m2{{1.1, 2.2-7.7j, 3}, {4, 5, 6}, {7, 8, 9}, {10, 11, 12}, {13, 14, 15}, {16, 17, 18}};
  arma::umat m3{{1, 2, 3}, {4, 5, 6}, {7, 8, 9}, {10, 11, 12}, {13, 14, 15}, {16, 17, 18}};
  arma::imat m4{{1, 2, 3}, {4, 5, 6}, {7, 8, 9}, {10, 11, 12}, {13, 14, 15}, {16, 17, 18}};

  arma::vec v1{1.1, 2.2, 3, 4, 5, 6};
  arma::cx_vec v2{1.1, 2.2, 3, 4, 5, 6};
  arma::uvec v3{1, 2, 3, 4, 5, 6};
  arma::ivec v4{1, 2, 3, 4, 5, 6};

  arma::cube u1 = arma::randu<arma::cube>(2,3,4);
  u1.print();


  // Add a breakpoint below, load the pretty printers and then try to print the variables
  return 0;
}
