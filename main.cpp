#include <armadillo>
#include <iostream>
#include <vector>

#if defined(ARMA_USE_EXTERN_CXX11_RNG)
namespace arma {
thread_local arma_rng_cxx11 arma_rng_cxx11_instance; // NOLINT
} // namespace arma
#endif

using namespace std::complex_literals;

int main() {
  int a[10] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};

  std::complex<int> c1(1, -3);
  std::complex<double> c2(1.5, -3.3);
  std::complex<double> c3(1.5, 3.3);

  arma::mat m1{{1.1, 2.2, 3}, //
               {4, 5, 6},     //
               {7, 8, 9},     //
               {10, 11, 12},  //
               {13, 14, 15},  //
               {16, 17, 18}};
  arma::cx_mat m2{{1.1 - 1.1j, 2.2 - 7.7j, 3},
                  {4, 5, 6},
                  {7, 8, 9},
                  {10, 11, 12},
                  {13, 14, 15},
                  {16, 17, 18}};
  arma::umat m3{{1, 2, 3},    //
                {4, 5, 6},    //
                {7, 8, 9},    //
                {10, 11, 12}, //
                {13, 14, 15}, //
                {16, 17, 18}};
  arma::imat m4{{1, 2, 3},    //
                {4, 5, 6},    //
                {7, 8, 9},    //
                {10, 11, 12}, //
                {13, 14, 15}, //
                {16, 17, 18}};

  arma::mat33 fm1{{1.1, 2.2, 3}, //
                  {4, 5, 6},     //
                  {7, 8, 9}};
  arma::cx_mat33 fm2{{1.1 - 1.1j, 2.2 - 7.7j, 3}, //
                     {4, 5, 6},                   //
                     {7, 8, 9}};
  arma::umat33 fm3{{1, 2, 3}, //
                   {4, 5, 6}, //
                   {7, 8, 9}};
  arma::imat33 fm4{{1, 2, 3}, //
                   {4, 5, 6}, //
                   {7, 8, 9}};

  arma::vec v1{1.1, 2.2, 3, 4, 5, 6};
  arma::cx_vec v2{1.1 - 1.1j, 2.2 - 2.2j, 3, 4, 5, 6};
  arma::uvec v3{1, 2, 3, 4, 5, 6};
  arma::ivec v4{1, 2, 3, 4, 5, 6};

  arma::vec6 fv1{1.1, 2.2, 3, 4, 5, 6};
  arma::cx_vec6 fv2{1.1 - 1.1j, 2.2 - 2.2j, 3, 4, 5, 6};
  arma::uvec6 fv3{1, 2, 3, 4, 5, 6};
  arma::ivec6 fv4{1, 2, 3, 4, 5, 6};

  arma::cube u1 = arma::randu<arma::cube>(2, 3, 4);
  arma::cx_cube u2 = arma::randu<arma::cx_cube>(2, 3, 4);
  arma::ucube u3 =
      arma::conv_to<arma::ucube>::from(10 * arma::randu<arma::cube>(2, 3, 4));
  arma::icube u4 =
      arma::conv_to<arma::icube>::from(10 * arma::randu<arma::cube>(2, 3, 4));

  // std::cout << "v1.max() is " << v1.max() << std::endl;
  // std::cout << "m1.max() is " << m1.max() << std::endl;
  // std::cout << "u1.max() is " << u1.max() << std::endl;
  //
  // std::cout << "v1.min() is " << v1.min() << std::endl;
  // std::cout << "m1.min() is " << m1.min() << std::endl;
  // std::cout << "u1.min() is " << u1.min() << std::endl;
  //
  // std::cout << "v1.empty() is " << v1.empty() << std::endl;
  // std::cout << "m1.empty() is " << m1.empty() << std::endl;
  // std::cout << "u1.empty() is " << u1.empty() << std::endl;
  //
  // std::cout << "v1.size() is " << v1.size() << std::endl;
  // std::cout << "m1.size() is " << m1.size() << std::endl;
  // std::cout << "u1.size() is " << u1.size() << std::endl;

  v1.print("v1");
  v2.print("v2");
  v3.print("v3");
  v4.print("v4");
  std::cout << std::endl;
  m1.print("m1");
  m2.print("m2");
  m3.print("m3");
  m4.print("m4");
  std::cout << std::endl;
  u1.print("u1");
  u2.print("u2");
  u3.print("u3");
  u4.print("u4");

  std::vector<double> stlvec;
  stlvec.reserve(10000);
  for (unsigned int i = 0; i < 10000; i++) {
    stlvec.push_back(arma::randn());
  }

  // Add a breakpoint below, load the pretty printers and then try to print the
  // variables
  std::cout << "The End" << std::endl;
  return 0;
}
