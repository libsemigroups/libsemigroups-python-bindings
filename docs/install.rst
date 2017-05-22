Installation
------------

Installing with conda
^^^^^^^^^^^^^^^^^^^^^

This installation method assumes that you have anaconda or miniconda
installed. See the `getting started <https://conda.io/docs/get-started.html>`_
and `miniconda download page <https://conda.io/miniconda.html>`_
on the `conda <https://conda.io/>`_ website.

Activate the `conda-forge <https://conda-forge.github.io/>`_ package repository::

    conda config --add channels conda-forge

Install the Python bindings::

    conda install libsemigroups-python-bindings

Installing from the sources
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Install some dependencies::

    sudo -H pip install cython cysignals --upgrade

Install the libsemigroups C++ library, e.g. from sources::

    git clone https://github.com/james-d-mitchell/libsemigroups
    cd libsemigroups
    ./autogen.sh ; ./configure ; make ; sudo make install
    cd ..

Install the python bindings::

    git clone https://github.com/james-d-mitchell/libsemigroups-python-bindings
    cd libsemigroups-python-bindings
    pip install --user . --upgrade
    cd ..

Try it out::

    python

    >>> from semigroups import Semigroup, Transformation
    >>> S = Semigroup(Transformation([1, 1, 4, 5, 4, 5]),
    ...               Transformation([2, 3, 2, 3, 5, 5]))
    >>> S.size()
    5
    >>> quit()

