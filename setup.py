#!/usr/bin/env python

""" PYLIPSMIN, Python Bindings to LIPSMIN
"""
DOCLINES = __doc__.split("\n")

# build with: $ python setup.py build_ext --inplace
# clean with: # python setup.py clean --all
# see:
# http://www.scipy.org/Documentation/numpy_distutils
# http://docs.cython.org/docs/tutorial.html

import os
import sys
from distutils.core import setup, Extension
from distutils.core import Command
from numpy.distutils.misc_util import get_numpy_include_dirs
import inspect


BASEDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

BOOST_DIR   = os.environ.get('BOOST_DIR', os.path.join(BASEDIR, '/usr/local'))
LIPSMIN_DIR   = os.environ.get('LIPSMIN_DIR', os.path.join(BASEDIR, 'PACKAGES/LIPSMIN/inst'))

boost_include_path   = os.path.join(BOOST_DIR, 'include')
boost_library_path1  = os.path.join(BOOST_DIR, 'lib')
boost_library_path2  = os.path.join(BOOST_DIR, 'lib64')

lipsmin_include_path   = os.path.join(LIPSMIN_DIR, 'include')
lipsmin_library_path1  = os.path.join(LIPSMIN_DIR, 'lib')
lipsmin_library_path2  = os.path.join(LIPSMIN_DIR, 'lib64')

# ADAPT THIS TO FIT YOUR SYSTEM
extra_compile_args = ['-std=c++11 -ftemplate-depth-100 -DBOOST_PYTHON_DYNAMIC_LIB']

if sys.platform == 'darwin' and os.environ.get('CC', 'clang').find('clang') > 0:
    extra_compile_args += ['-stdlib=libc++ -mmacosx-version-min=10.9']

include_dirs = [get_numpy_include_dirs()[0], boost_include_path, lipsmin_include_path]
library_dirs = [boost_library_path1, boost_library_path2, lipsmin_library_path1, lipsmin_library_path2]
libraries = ['boost_python','LiPsMin']

print ''
print '\033[1;31mPlease check that the following settings are correct for your system:\n\033[1;m'
print 'include_dirs = %s\n'%str(include_dirs)
print 'library_dirs = %s\n'%str(library_dirs)
print '''
If LIPSMIN cannot be found, you can manually set the paths via
``export LIPSMIN_DIR=/path/to/lipsmin``

* where /path/to/lipsmin contains the folders ``./include`` and ``./lib64``.

You can also specify the compiler, e.g. by
``export CC=clang`` and ``export CXX=clang++`` or run

Example:

    CC=clang CXX=clang++ python setup.py

'''
raw_input("Press enter to build pylipsmin.")


# PACKAGE INFORMATION
CLASSIFIERS = """\
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved
Programming Language :: C++
Programming Language :: Python
Topic :: Software Development
Topic :: Scientific/Engineering
Operating System :: Linux
"""

NAME                = 'pylipsmin'
MAINTAINER          = "Sebastian F. Walter"
MAINTAINER_EMAIL    = "sebastian.walter@gmail.com"
DESCRIPTION         = DOCLINES[0]
LONG_DESCRIPTION    = "\n".join(DOCLINES[2:])
URL                 = "http://www.github.com/b45ch1/pylipsmin"
DOWNLOAD_URL        = "http://www.github.com/b45ch1/pylipsmin"
LICENSE             = 'BSD'
CLASSIFIERS         = filter(None, CLASSIFIERS.split('\n'))
AUTHOR              = "Sebastian F. Walter"
AUTHOR_EMAIL        = "sebastian.walter@gmail.com"
PLATFORMS           = ["Linux"]
MAJOR               = 0
MINOR               = 1
MICRO               = 0
ISRELEASED          = False
VERSION             = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

# IT IS USUALLY NOT NECESSARY TO CHANGE ANTHING BELOW THIS POINT
# override default setup.py help output
import sys
if len(sys.argv) == 1:
    print """

    You didn't enter what to do!

    Options:
    1: build the extension with
    python setup.py build

    2: install the extension with
    python setup.py install

    3: alternatively build inplace
    python setup.py build_ext --inplace

    4: remove generated files with
    python setup.py clean --all


    Remark: This is an override of the default behaviour of the distutils setup.
    """
    exit()

class clean(Command):
    """
    This class is used in numpy.distutils.core.setup.
    When $python setup.py clean is called, an instance of this class is created and then it's run method is called.
    """

    description = "Clean everything"
    user_options = [("all","a","the same")]

    def initialize_options(self):
        self.all = None

    def finalize_options(self):
        pass

    def run(self):
        import os
        os.system("rm -rf build")
        os.system("rm _lipsmin.so")
        os.system("rm -f py_lipsmin.os num_util.os")
        os.system("rm *.pyc")


def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

# find all files that should be included
packages, data_files = [], []
for dirpath, dirnames, filenames in os.walk('lipsmin'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

options_dict = {}
options_dict.update({
'name':NAME,
'version':VERSION,
'description' :DESCRIPTION,
'long_description' : LONG_DESCRIPTION,
'license':LICENSE,
'author':AUTHOR,
'platforms':PLATFORMS,
'author_email': AUTHOR_EMAIL,
'url':URL,
'packages' :packages,
'ext_package' : 'lipsmin',
'ext_modules': [Extension('_lipsmin', ['lipsmin/src/pylipsmin.cpp', 'lipsmin/src/num_util.cpp'],
                                include_dirs = ['lipsmin/src'] + include_dirs,
                                library_dirs = library_dirs,
                                runtime_library_dirs = library_dirs,
                                libraries = libraries,
                                extra_compile_args = extra_compile_args),
],

'cmdclass' : {'clean':clean}
})

setup(**options_dict)
