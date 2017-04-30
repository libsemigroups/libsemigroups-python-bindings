
'''
This module contains classes for semirings.
'''
# pylint: disable = no-member, protected-access, invalid-name,
# FIXME this is only partially complete

class Semiring:
    def __init__(self):
        self._minus_infinity = -float('inf')
        self._plus_infinity = float('inf')


class Integers(Semiring):

    def __init___(self):
        pass

    def plus(self, x, y):
        if not (isinstance(x, int) and isinstance(y, int)):
            raise TypeError
        return x + y

    def prod(self, x, y):
        if not (isinstance(x, int) and isinstance(y, int)):
            raise TypeError
        return x * y

    def zero(self):
        return 0

    def one(self):
        return 1


class MaxPlusSemiring(Semiring):

    def __init___(self):
        pass

    def plus(self, x, y):
        if not ((isinstance(x, int) or x == -float('inf'))
                and (isinstance(y, int) or y == -float('inf'))):
            raise TypeError
        return max(x, y)

    def prod(self, x, y):
        if not ((isinstance(x, int) or x == -float('inf'))
                and (isinstance(y, int) or y == -float('inf'))):
            raise TypeError
        return x + y

    def zero(self):
        return self._minus_infinity

    def one(self):
        return 0


class MinPlusSemiring(Semiring):

    def __init___(self):
        pass

    def plus(self, x, y):
        if not ((isinstance(x, int) or x == float('inf'))
                and (isinstance(y, int) or y == float('inf'))):
            raise TypeError
        return min(x, y)

    def prod(self, x, y):
        if not ((isinstance(x, int) or x == float('inf'))
                and (isinstance(y, int) or y == float('inf'))):
            raise TypeError
        return x + y

    def zero(self):
        return self._plus_infinity

    def one(self):
        return 0
