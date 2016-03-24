#include <boost/python.hpp>
#include "pylipsmin.hpp"


using namespace std;

/* C STYLE CALLS OF FUNCTIONS */
/* easy to use drivers */
void c_wrapped_LiPsMin(PyObject* file_obj, 
		       short tape_tag, 
		       double q, 
		       int n,
		       bpn::array &bpn_x, 
		       bpn::array &bpn_y ){
  double* x = (double*) nu::data(bpn_x);
  double* y = (double*) nu::data(bpn_y);
  assert(PyFile_Check(file_obj));
  return ::LiPsMin(PyFile_AsFile(file_obj), tape_tag, q, n, x, y);
}
