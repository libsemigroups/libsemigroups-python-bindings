# -*- coding: utf-8 -*-

import codecs
from sys import platform
from os import path
from setuptools import setup, Extension
from Cython.Build import cythonize

# from setuptools.dist import Distribution
# from Cython.Distutils import build_ext
# Distribution(dict(setup_requires='Cython'))

here = path.abspath(path.dirname(__file__))

extra_compile_args = ['-std=c++11']
if platform == 'darwin':
    extra_compile_args.append('-mmacosx-version-min=10.9')

# Get the long description from the README file
with codecs.open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    install_requires=['cysignals', 'networkx'],
    version='0.3.1',
    name='semigroups',
    description='Python bindings for the libsemigroups mathematics library',
    long_description=long_description,
    url=('https://github.com/james-d-mitchell/libsemigroups-python-bindings'),
    author='James Mitchell and Nicolas M. Thiéry',
    author_email='TODO',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='Mathematics, semigroup theory',
    packages=['semigroups'],

    ext_modules=cythonize([
        Extension('libsemigroups',
                  sources=['semigroups/libsemigroups.pyx',
                           'semigroups/libsemigroups_cpp.cpp'],
                  depends=['semigroups/libsemigroups.pxd',
                           'semigroups/libsemigroups_cpp.h'],
                  libraries=['semigroups'],
                  language='c++',             # generate C++ code
                  extra_compile_args=extra_compile_args
                  )]),

    tests_require=['cysignals'],
)

# Note: getting the headers included in the source distribution seems tricky.
# For now, we use the MANIFEST.in, as recommended on
# https://stackoverflow.com/questions/43163315/how-to-include-header-file-in-cython-correctly-setup-py
