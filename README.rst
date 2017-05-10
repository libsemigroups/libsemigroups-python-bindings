Python bindings for libsemigroups
=================================

This is a basic package providing python bindings for the `libsemigroups
<https://james-d-mitchell.github.io/libsemigroups/>`_  C++ library.

`libsemigroups
<https://james-d-mitchell.github.io/libsemigroups/>`_ is a C++ library for semigroups and monoids; it is partly based on 
`Algorithms for computing finite semigroups <https://www.irif.fr/~jep/PDF/Rio.pdf>`_, 
`Expository Slides <https://www.irif.fr/~jep/PDF/Exposes/StAndrews.pdf>`_, and 
`Semigroupe 2.01
<https://www.irif.fr/~jep/Logiciels/Semigroupe2.0/semigroupe2.html>`_
Jean-Eric Pin.


Basic instructions
------------------

Installing with conda
^^^^^^^^^^^^^^^^^^^^^

This installation method assumes that you have anaconda or miniconda
installed. See the `getting started <https://conda.io/docs/get-started.html>`_
and `miniconda download page <https://conda.io/miniconda.html>`_
on the `conda <https://conda.io/>`_ website.

Activate the `conda-forge <https://conda-forge.github.io/>`_ package repository::

    conda config --add channels conda-forge

Install the C++ library (headers, static and shared library)::

    conda install libsemigroups

Install the Python bindings::

    conda install libsemigroups-python-bindings

From the source
^^^^^^^^^^^^^^^

Install the libsemigroups C++ library, e.g. from sources::

    git clone https://github.com/james-d-mitchell/libsemigroups-python-bindings
    cd libsemigroups
    ./autogen.sh ; make ; sudo make install

Install the python bindings::

    cd libsemigroups-python-bindings
    pip install --user . --upgrade

Try it out::

    cd libsemigroups-python-bindings
    pip install --user . --upgrade
    python

    >>> from semigroups import Semigroup, Transformation
    >>> S = Semigroup(Transformation([1, 1, 4, 5, 4, 5]),
    ...               Transformation([2, 3, 2, 3, 5, 5]))
    >>> S.size()
    5

Issues
------

If you find any problems with libsemigroups-python-bindings or have any
suggestions for features that you'd like to see please use the 
`issue tracker 
<https://github.com/james-d-mitchell/libsemigroups-python-bindings/issues>`_.

Documentation
-------------
The documentation is generated using
`Sphinx <http://www.sphinx-doc.org>`_ and is available
`here <http://james-d-mitchell.github.io/libsemigroups-python-bindings/>`_.
