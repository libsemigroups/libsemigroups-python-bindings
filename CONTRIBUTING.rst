Information for developers
==========================

None yet...

Information for the maintainer
==============================

Uploading the package to pipy
-----------------------------

Build the binary wheel::

    rm -rf dist
    python setup.py sdist

The first time::

    twine register dist/*.tar.gz

For latter releases::

    twine upload -s dist/*.tar.gz

Updating the conda package
--------------------------

The conda package has its own git repository at:

https://github.com/conda-forge/libsemigroups-python-bindings-feedstock

The relevant files are:
* [meta.yaml](meta.yaml)
* [build.sh](build.sh)

To update the package:

* Update the version and md5sum in `meta.yaml`

* Install conda and go into your conda environment.
  See the getting started section in the
  `Conda documentation <https://conda.io/docs/index.html>`_ for details.

* Run::

    conda build .

* Try it with::

    conda install --use-local libsemigroups

* Publish it: see https://conda-forge.github.io/

References:

* `Conda's Tutorials on building packages
  <https://conda.io/docs/build_tutorials.html>`_
* A `repository of conda recipes for classical programs
  <https://github.com/conda/conda-recipes>`_; nice source of inspiration

Trick to debug segmentation faults
----------------------------------

Install Sage

Install gdb in Sage::

    sage -i gdb

Run sage as::

    sage -gdb

and type the commands that trigger the segfault. Then `gdb` will be
fired automatically, allowing for analysing the stack trace.
