'''
This module contains classes for representing semigroups.
'''
# pylint: disable = no-member, protected-access, invalid-name,

import libsemigroups
from semigroups.elements import Element, Transformation
from libsemigroups import PythonElement


class Semigroup(libsemigroups.CySemigroup):
    '''
    A class for handles to libsemigroups semigroups

    Examples:
        >>> from semigroups import Semigroup, Transformation
        >>> S = Semigroup(Transformation([1, 2, 0]), Transformation([2, 1, 0]))
        >>> # the symmetric group
        >>> S.size()
        6
    '''
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], list):
            self.__init__(*args[0])
            return
        elif len(args) == 0:
            ValueError('there must be at least 1 argument')

        gens = [g._cy_element if isinstance(g, Element) else PythonElement(g)
                for g in args]
        libsemigroups.CySemigroup.__init__(self, gens)


def FullTransformationMonoid(n):
    '''
    Returns the full transformation monoid of degree n.
    '''
    assert isinstance(n, int) and n >= 1
    if n == 1:
        return Semigroup(Transformation([0]))
    elif n == 2:
        return Semigroup(Transformation([1, 0]), Transformation([0, 0]))

    return Semigroup([Transformation([1, 0] + list(range(2, n))),
                      Transformation([0, 0] + list(range(2, n))),
                      Transformation([n - 1] + list(range(n - 1)))])
