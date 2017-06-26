'''
This module contains classes for representing semigroups.
'''
# pylint: disable = no-member, protected-access, invalid-name

import libsemigroups
from semigroups.elements import Transformation
from libsemigroups import ElementABC, PythonElementNC


class Semigroup(libsemigroups.SemigroupNC):
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

        gens = [g if (isinstance(g, ElementABC) and str(type(g)) !=
                      "<class 'semigroups.semifp._FPSOME'>")
                else PythonElementNC(g) for g in args]
        libsemigroups.SemigroupNC.__init__(self, gens)

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
