#ifndef _PYLIPSMIN_HPP_
#define _PYLIPSMIN_HPP_
#define PY_ARRAY_UNIQUE_SYMBOL PyArrayHandle

#include "num_util.h"
#include "LiPsMin/LiPsMin.h"

using namespace std;
namespace b = boost;
namespace bp = boost::python;
namespace bpn = boost::python::numeric;
namespace nu = num_util;


int get_size_of_short(){ return static_cast<int>(sizeof(short)); }
int get_size_of_int(){ return static_cast<int>(sizeof(int)); }
int get_size_of_long(){ return static_cast<int>(sizeof(long)); }

/* C STYLE CALLS OF FUNCTIONS */
void c_wrapped_LiPsMin(PyObject* file_obj, 
		       short tag, 
		       int n, 
		       double q, 
		       bpn::array &x, 
		       bpn::array &y);

BOOST_PYTHON_MODULE(_lipsmin)
{
	using namespace boost::python;
	import_array(); /* some kind of hack to get numpy working */
	bpn::array::set_module_and_type("numpy", "ndarray"); /* some kind of hack to get numpy working */

	scope().attr("__doc__") ="unused: moved docstring to adolc.py";

	def("get_size_of_short", get_size_of_short);
	def("get_size_of_int", get_size_of_int);
	def("get_size_of_long", get_size_of_long);


	/* c style functions */
	def("function", 		&c_wrapped_LiPsMin);
}

#endif
