'''
This module contains classes for semirings.
'''
# pylint: disable = no-member, protected-access, invalid-name
# pylint: disable = too-few-public-methods

class SemiringABC:
    r'''
    A *semiring* is a set :math:`R`, together with two binary operations,
    :math:`+` and :math:`\times`, such that :math:`(R, +)` is a commutative
    monoid, with identity called 0, :math:`(R\backslash\{0\},\times)` is a
    monoid, with identity 1, :math:`(R, +, \times)` is left and right
    distributive, and multiplication by 0 must annihilate :math:`R`.

    Multiplication by an element :math:`b\in R` *annihilates* :math:`R` if for
    all :math:`a \in R \quad a \cdot b = b \cdot a = b`.

    Multiplication in :math:`R` is *left distributive* if for all
    :math:`a, b, c \in R \quad a(b + c) = ab + ac`, and *right distributive* if
    for all :math:`a, b, c \in R \quad (a + b)c = ac + bc`.

    This abstract class provides common methods for its subclasses.

    Returns:
        None

    Raises:
        TypeError:  If any argument is given.
    '''

    def __init__(self):
        self._minus_infinity = -float('inf')
        self._plus_infinity = float('inf')

class Integers(SemiringABC):
    '''
    The usual ring of the integers.

    Returns:
        None

    Raises:
        TypeError:  If any argument is given.

    Examples:
        >>> from semigroups import Integers
        >>> Integers().plus(3, 4)
        7
        >>> Integers().prod(3, 4)
        12
    '''

    @staticmethod
    def plus(x, y):
        '''
        A function to find the sum of two integers, since this is the additive
        operation of the integers.

        Args:
            x (int):    One of the integers to be added.
            y (int):    The other of the integers to be added.

        Returns:
            int:    x + y

        Raises:
            TypeError:  If x and y are not both ints.

        Examples:
            >>> from semigroups import Integers
            >>> Integers().plus(2, -5)
            -3
        '''
        if not (isinstance(x, int) and isinstance(y, int)):
            raise TypeError
        return x + y

    @staticmethod
    def prod(x, y):
        '''
        A function to find the sum of two integers, since this is the
        multiplicative operation of the integers.

        Args:
            x (int):    One of the integers to be multiplied.
            y (int):    The other of the integers to be multplied.

        Returns:
            int:    x * y

        Raises:
            TypeError:  If x and y are not both ints.

        Examples:
            >>> from semigroups import Integers
            >>> Integers().prod(-13, 2)
            -26
        '''
        if not (isinstance(x, int) and isinstance(y, int)):
            raise TypeError

        return x * y

    @staticmethod
    def zero():
        '''
        A function to find the additive identity of the integers, which
        is 0.

        Returns:
            int:    0

        Raises:
            TypeError:  If any argument is given.

        Examples:
            >>> from semigroups import Integers
            >>> Integers().zero()
            0
        '''
        return 0

    @staticmethod
    def one():
        '''
        A function to find the multiplicative identity of the integers, which
        is 1.

        Returns:
            int:    1

        Raises:
            TypeError:  If any argument is given.

        Examples:
            >>> from semigroups import Integers
            >>> Integers().one()
            1
        '''

        return 1


class MaxPlusSemiring(SemiringABC):
    r'''
    The *max plus semiring* is a semiring comprising the set
    :math:`\mathbb{Z}\cup\{-\infty\}`, together with an operation which
    returns the maximum of two elements, as the additive operation and addition
    as the multiplicative operation.

    *Minus infinity* is a defined as smaller than all integers, and the integer
    sum of minus infinity and any element of the max plus semiring is minus
    infinity.

    Returns:
        None

    Raises:
        TypeError:  If any argument is given.

    Examples:
        >>> from semigroups import MaxPlusSemiring
        >>> MaxPlusSemiring().plus(-float('inf'), -20)
        -20
        >>> MaxPlusSemiring().prod(-float('inf'), -20)
        -inf
    '''

    @staticmethod
    def plus(x, y):
        '''
        A function to find the maximum of two elements of the max plus
        semiring, since this is the additive operation of the max plus
        semiring.

        Args:
            x (int or float):    One of the elements to be added.
            y (int or float):    The other of the elements to be added.

        Returns:
            int or float:    The maximum of x and y.

        Raises:
            TypeError:  If x and y are not both ints or minus infinity.

        Examples:
            >>> from semigroups import MaxPlusSemiring
            >>> MaxPlusSemiring().plus(7, -20)
            7
        '''
        if not ((isinstance(x, int) or x == -float('inf'))
                and (isinstance(y, int) or y == -float('inf'))):
            raise TypeError

        return max(x, y)

    @staticmethod
    def prod(x, y):
        '''
        A function to find the integer sum of two elements of the max plus
        semiring, since this is the multiplicative operation of the max plus
        semiring. If either input is minus infinity, this function will return
        minus infinity.

        Args:
            x (int or float):    One of the elements to be multiplied.
            y (int or float):    The other of the elements to be multplied.

        Returns:
            int or float:    x + y

        Raises:
            TypeError:  If x and y are not both ints or minus infinity.

        Examples:
            >>> from semigroups import MaxPlusSemiring
            >>> MaxPlusSemiring().prod(7, -20)
            -13
        '''
        if not ((isinstance(x, int) or x == -float('inf'))
                and (isinstance(y, int) or y == -float('inf'))):
            raise TypeError

        return x + y

    @staticmethod
    def zero():
        '''
        A function to find the additive identity of the max plus
        semiring, which is minus infinity.

        Returns:
            float:   -inf

        Raises:
            TypeError:  If any argument is given.

        Examples:
            >>> from semigroups import MaxPlusSemiring
            >>> MaxPlusSemiring().zero()
            -inf
        '''
        return -float('inf')

    @staticmethod
    def one():
        '''
        A function to find the multiplicative identity of the max plus
        semiring, which is 0.

        Returns:
            int:    0

        Raises:
            TypeError:  If any argument is given.

        Examples:
            >>> from semigroups import MaxPlusSemiring
            >>> MaxPlusSemiring().one()
            0
        '''
        return 0

class MinPlusSemiring(SemiringABC):
    r'''
    The *min plus semiring* is a semiring comprising the set
    :math:`\mathbb{Z}\cup\{\infty\}`, together with an operation which
    returns the maximum of two elements, as the additive operation and addition
    as the multiplicative operation.

    *Plus infinity* is a defined as greater than all integers, and the integer
    sum of plus infinity and any element of the max plus semiring is plus
    infinity.

    Returns:
        None

    Raises:
        TypeError:  If any argument is given.

    Examples:
        >>> from semigroups import MinPlusSemiring
        >>> MinPlusSemiring().plus(3, float('inf'))
        3
        >>> MinPlusSemiring().prod(3, float('inf'))
        inf
    '''

    @staticmethod
    def plus(x, y):
        '''
        A function to find the minimum of two elements of the min plus
        semiring, since this is the additive operation of the min plus
        semiring.

        Args:
            x (int or float):    One of the elements to be added.
            y (int or float):    The other of the elements to be added.

        Returns:
            int float:    The minimum of x and y.

        Raises:
            TypeError:  If x and y are not both ints or plus infinity.

        Examples:
            >>> from semigroups import MinPlusSemiring
            >>> MinPlusSemiring().plus(37, 73)
            37
        '''
        if not ((isinstance(x, int) or x == float('inf'))
                and (isinstance(y, int) or y == float('inf'))):
            raise TypeError

        return min(x, y)

    @staticmethod
    def prod(x, y):
        '''
        A function to find the integer sum of two elements of the min plus
        semiring, since this is the multiplicative operation of the min plus
        semiring. If either inpu is plus infinity, this function ill return
        plus infinity.

        Args:
            x (int or float):    One of the elements to be multiplied.
            y (int or float):    The other of the elements to be multplied.

        Returns:
            int or float:    x + y

        Raises:
            TypeError:  If x and y are not both ints or plus infinity.

        Examples:
            >>> from semigroups import MinPlusSemiring
            >>> MinPlusSemiring().prod(37, 73)
            110
        '''

        if not ((isinstance(x, int) or x == float('inf'))
                and (isinstance(y, int) or y == float('inf'))):
            raise TypeError

        return x + y

    @staticmethod
    def zero():
        '''
        A function to find the additive identity of the min plus
        semiring, which is plus infinity.

        Returns:
            float:   inf

        Raises:
            TypeError:  If any argument is given.

        Examples:
            >>> from semigroups import MinPlusSemiring
            >>> MinPlusSemiring().zero()
            inf
        '''

        return float('inf')

    @staticmethod
    def one():
        '''
        A function to find the multiplicative identity of the min plus
        semiring, which is 0.

        Returns:
            int:    0

        Raises:
            TypeError:  If any argument is given.

        Examples:
            >>> from semigroups import MinPlusSemiring
            >>> MinPlusSemiring().one()
            0
        '''

        return 0

class BooleanSemiring(SemiringABC):
    r'''
    The *boolean semiring* is a semiring comprising the set containing
    True and False, together with the operations or and and (the logical
    conjunctions).

    Returns:
        None

    Raises:
        TypeError:  If any argument is given.

    Examples:
        >>> from semigroups import BooleanSemiring
        >>> BooleanSemiring().plus(True, False)
        True
        >>> BooleanSemiring().prod(True, False)
        False
    '''

    @staticmethod
    def plus(x, y):
        '''
        A function which returns True if either element is True (the logical
        conjunction or), since this is the additive operation.

        Args:
            x (bool):    One of the elements to be added.
            y (bool):    The other of the elements to be added.

        Returns:
            bool:    The result of x or y.

        Raises:
            TypeError:  If x and y are not both bools.

        Examples:
            >>> from semigroups import BooleanSemiring
            >>> BooleanSemiring().plus(True, True)
            True
        '''

        if not (isinstance(x, type(True)) and isinstance(y, type(True))):
            raise TypeError

        return x or y

    @staticmethod
    def prod(x, y):
        '''
        A function which returns False if either element is False (the logical
        conjunction and), since this is the multiplicative operation.

        Args:
            x (bool):    One of the elements to be multiplied.
            y (bool):    The other of the elements to be multiplied.

        Returns:
            bool:    The result of x and y.

        Raises:
            TypeError:  If x and y are not both bools.

        Examples:
            >>> from semigroups import BooleanSemiring
            >>> BooleanSemiring().prod(True, True)
            True
        '''

        if not (isinstance(x, type(True)) and isinstance(y, type(True))):
            raise TypeError

        return x and y

    @staticmethod
    def zero():
        '''
        A function to find the additive identity of the boolean semiring, which
        is False.

        Returns:
            bool:   False

        Raises:
            TypeError:  If any argument is given.

        Examples:
            >>> from semigroups import BooleanSemiring
            >>> BooleanSemiring().zero()
            False
        '''
        return False

    @staticmethod
    def one():
        '''
        A function to find the mutliplicative identity of the boolean semiring,
        which is True.

        Returns:
            bool:   True

        Raises:
            TypeError:  If any argument is given.

        Examples:
            >>> from semigroups import BooleanSemiring
            >>> BooleanSemiring().one()
            True
        '''

        return True

class SemiringWithThresholdABC(SemiringABC):
    '''
    A *semiring with a threshold* is a semiring with a largest finite value,
    the *threshold*.

    This abstract class provides common methods for its subclasses.

    Returns:
        None

    Raises:
        TypeError:  If any argument is given.
    '''

    def threshold(self):
        '''
        A function to find the threshold of a semiring.

        Returns:
            The threshold of the semiring.

        Raises:
            TypeError:  If any argument is given.

        Examples:
            >>> from semigroups import TropicalMaxPlusSemiring, NaturalSemiring
            >>> TropicalMinPlusSemiring(3).threshold()
            3
            >>> NaturalSemiring(9, 27).threshold()
            9
        '''

        return self._threshold

class TropicalMaxPlusSemiring(SemiringWithThresholdABC):
    # pylint: disable = super-init-not-called
    r'''
    A *tropical max plus semiring* is a semiring comprising the set :math:`\{0,
    \ldots, t\} \cup\{-\infty\}`, for some value :math:`t\in\mathbb{N} \cup
    \{0\}`, the threshold of the semiring, together with an operation which
    returns the maximum of two elements, as the additive operation and addition
    of integers as the multiplicative operation.

    *Minus infinity* is a defined as smaller than all integers, and the integer
    sum of minus infinity and any element of the tropical max plus semiring is
    minus infinity.

    If the integer sum of any two elements is greater than the threshold, then
    the product is the threshold.

    Args:
        threshold (int):    The threshold of the semiring.

    Returns:
        None

    Raises:
        TypeError:  If threshold is not an int.
        ValueError: If threshold is negative.

    Examples:
        >>> from semigroups import TropicalMaxPlusSemiring
        >>> TropicalMaxPlusSemiring(26).plus(7, 25)
        25
        >>> TropicalMaxPlusSemiring(26).prod(7, 25)
        26
        >>> TropicalMaxPlusSemiring(26).threshold()
        26
    '''

    def __init__(self, threshold):
        if not isinstance(threshold, int):
            raise TypeError

        if threshold < 0:
            raise ValueError

        self._threshold = threshold

    def plus(self, x, y):
        '''
        A function to find the maximum of two elements of a tropical max plus
        semiring, since this is the addition operation of a tropical max plus
        semiring.

        Args:
            x (int or float):    One of the elements to be added.
            y (int or float):    The other of the elements to be added.

        Returns:
            int or float:   The maximum of x and y.

        Raises:
            TypeError:  If x and y are not both ints or minus infinity.
            ValueError: If either x or y is negative and not minus infinity, or
                        if x or y is greater than the threshold.

        Examples:
            >>> from semigroups import TropicalMaxPlusSemiring
            >>> TropicalMaxPlusSemiring(72).plus(-float('inf'), 25)
            25
        '''

        if not ((isinstance(x, int) or x == -float('inf'))
                and (isinstance(y, int) or y == -float('inf'))):
            raise TypeError
        if (x < 0 and x != -float('inf')) or (y < 0 and y != -float('inf')):
            raise ValueError
        if (x > self._threshold) or (y > self._threshold):
            raise ValueError

        return max(x, y)

    def prod(self, x, y):
        '''
        A function to find the integer sum of two elements of a tropical max
        plus semiring, since this is the mutliplicative operation of a tropical
        max plus semiring. If the integer sum is greater than :math:`t`, then
        the result is :math:`t`.

        Note that the if either value is minus infinity, then minus infinity
        will be returned.

        Args:
            x (int or float):    One of the elements to be multiplied.
            y (int or float):    The other of the elements to be multplied.

        Returns:
            int or float:    x + y

        Raises:
            TypeError:  If x and y are not both ints or minus infinity.
            ValueError: If either x or y is negative and not minus infinity, or
                        if x or y is greater than the threshold.

        Examples:
            >>> from semigroups import TropicalMaxPlusSemiring
            >>> TropicalMaxPlusSemiring(72).prod(-float('inf'), 25)
            -inf
        '''
        if not ((isinstance(x, int) or x == -float('inf'))
                and (isinstance(y, int) or y == -float('inf'))):
            raise TypeError
        if (x < 0 and x != -float('inf')) or (y < 0 and y != -float('inf')):
            raise ValueError
        if (x > self._threshold) or (y > self._threshold):
            raise ValueError

        return min(self._threshold, x + y)

    @staticmethod
    def zero():
        '''
        A function to find the additive identity of a tropical max plus
        semiring, which is minus infinity.

        Returns:
            float:   -inf

        Raises:
            TypeError:  If any argument is given.

        Examples:
            >>> from semigroups import TropicalMaxPlusSemiring
            >>> TropicalMaxPlusSemiring(72).zero()
            -inf
        '''

        return -float('inf')

    @staticmethod
    def one():
        '''
        A function to find the multiplicative identity of a tropical max plus
        semiring, which is 0.

        Returns:
            int:    0

        Raises:
            TypeError:  If any argument is given.

        Examples:
            >>> from semigroups import TropicalMaxPlusSemiring
            >>> TropicalMaxPlusSemiring(72).one()
            0
        '''

        return 0

class TropicalMinPlusSemiring(SemiringWithThresholdABC):
    # pylint: disable = super-init-not-called
    r'''
    A *tropical min plus semiring* is a semiring comprising the set :math:`\{0,
    \ldots, t\} \cup\{-\infty\}`, for some value :math:`t\in\mathbb{N} \cup
    \{0\}`, the threshold of the semiring, together with an operation which
    returns the maximum of two elements, as the additive operation and addition
    of integers as the multiplicative operation.

    *Plus infinity* is a defined as greater than all integers, and the integer
    sum of plus infinity and any element of the tropical min plus semiring is
    plus infinity.

    If the integer sum of any two elements is greater than the threshold, then
    the product is the threshold.

    Args:
        threshold (int):    The threshold of the semiring.

    Returns:
        None

    Raises:
        TypeError:  If threshold is not an int.
        ValueError: If threshold is negative.

    Examples:
        >>> from semigroups import TropicalMinPlusSemiring
        >>> TropicalMinPlusSemiring(81).plus(7, 37)
        7
        >>> TropicalMinPlusSemiring(81).prod(7, 37)
        44
        >>> TropicalMinPlusSemiring(10).threshold()
        10
    '''

    def __init__(self, threshold):
        if not isinstance(threshold, int):
            raise TypeError

        if threshold < 0:
            raise ValueError

        self._threshold = threshold

    def plus(self, x, y):
        '''
        A function to find the minimum of two elements of a tropical min plus
        semiring, since this is the additive operation of a tropical min plus
        semiring.

        Args:
            x (int or float):    One of the elements to be added.
            y (int or float):    The other of the elements to be added.

        Returns:
            int or float:   The minimum of x and y.

        Raises:
            TypeError:  If x and y are not both ints or plus infinity.
            ValueError: If either x or y is negative and not plus infinity, or
                        if x or y is greater than the threshold.

        Examples:
            >>> from semigroups import TropicalMinPlusSemiring
            >>> TropicalMinPlusSemiring(7).plus(float('inf'), 3)
            3
        '''

        if not ((isinstance(x, int) or x == float('inf'))
                and (isinstance(y, int) or y == float('inf'))):
            raise TypeError

        if x < 0 or y < 0:
            raise ValueError

        if ((x > self._threshold and x != float('inf')) or
                (y > self._threshold and y != float('inf'))):
            raise ValueError

        return min(x, y)

    def prod(self, x, y):
        '''
        A function to find the integer sum of two elements of a tropical min
        plus semiring, since this is the multiplicative operation of a tropical
        min plus semiring. If the integer sum is greater than :math:`t`, then
        the result is :math:`t`.

        Note that the if either value is plus infinity, then plus infinity will
        be returned.

        Args:
            x (int or float):    One of the elements to be multiplied.
            y (int or float):    The other of the elements to be multplied.

        Returns:
            int or float:    x + y

        Raises:
            TypeError:  If x and y are not both ints or plus infinity.
            ValueError: If either x or y is negative and not plus infinity, or
                        if x or y is greater than the threshold.

        Examples:
            >>> from semigroups import TropicalMinPlusSemiring
            >>> TropicalMinPlusSemiring(7).prod(float('inf'), 3)
            inf
        '''

        if not ((isinstance(x, int) or x == float('inf'))
                and (isinstance(y, int) or y == float('inf'))):
            raise TypeError
        if x < 0 or y < 0:
            raise ValueError
        if ((x > self._threshold and x != float('inf')) or
                (y > self._threshold and y != float('inf'))):
            raise ValueError
        if max(x, y) == float('inf'):
            return float('inf')

        return min(self._threshold, x + y)

    @staticmethod
    def zero():
        '''
        A function to find the additive identity of a tropical min plus
        semiring, which is plus infinity.

        Returns:
            float:   inf

        Raises:
            TypeError:  If any argument is given.

        Examples:
            >>> from semigroups import TropicalMinPlusSemiring
            >>> TropicalMinPlusSemiring(7).zero()
            inf
        '''

        return float('inf')

    @staticmethod
    def one():
        '''
        A function to find the multiplicative identity of a tropical min plus
        semiring, which is 0.

        Returns:
            int:    0

        Raises:
            TypeError:  If any argument is given.

                Examples:
            >>> from semigroups import TropicalMinPlusSemiring
            >>> TropicalMinPlusSemiring(7).one()
            0
        '''

        return 0

class NaturalSemiring(SemiringWithThresholdABC):
    # pylint: disable = super-init-not-called
    r'''
    Let :math:`t\in\mathbb{N} \cup \{0\}, \ p\in\mathbb{N}` and :math:`\equiv`
    be the congruence relation on :math:`\mathbb{N} \cup \{0\}` defined by
    :math:`t\equiv t + p`. A *natural semiring* is a semiring comprising the
    set :math:`\{0, \ldots, p + t - 1\}`, together with addition an
    multiplication of naturals modulo :math:`\equiv`. Then :math:`t` is called
    the *threshold* of the semiring and :math:`p` is the *period*.

    Args:
        threshold (int):    The threshold of the semiring.
        period (int):       The period of the semiring.

    Returns:
        None

    Raises:
        TypeError:  If the threshold and period are not both ints.
        ValueError: If the threshold is negative or the period is not positive.

    Examples:
        >>> from semigroups import NaturalSemiring
        >>> NaturalSemiring(3, 4).plus(2, 6)
        4
        >>> NaturalSemiring(3, 4).prod(2, 6)
        4
        >>> NaturalSemiring(3, 4).threshold()
        3
        >>> NaturalSemiring(3, 4).period()
        4
    '''
    def __init__(self, threshold, period):
        if not (isinstance(period, int) and isinstance(threshold, int)):
            raise TypeError
        if period < 1 or threshold < 0:
            raise ValueError

        self._period = period
        self._threshold = threshold

    def plus(self, x, y):
        r'''
        A function to find the integer sum modulo :math:`\equiv`, of two
        elements of a natural semiring. Here :math:`\equiv` is the congruence
        of the natural semiring.

        Args:
            x (int):    One of the elements to be added.
            y (int):    The other of the elements to be added.

        Returns:
            int:   The integer sum modulo :math:`\equiv`, of x and y.

        Raises:
            TypeError:  If x and y are not both ints.
            ValueError: If either x or y is negative, or greater than :math:`t
                        + p - 1`.

        Examples:
            >>> from semigroups import NaturalSemiring
            >>> NaturalSemiring(5, 7).plus(3, 10)
            6
        '''
        if not (isinstance(x, int) and isinstance(y, int)):
            raise TypeError
        if not ((0 <= x < self._threshold + self._period) and
                (0 <= y < self._threshold + self._period)):
            raise ValueError

        return (x + y - self._threshold) % self._period + self._threshold

    def prod(self, x, y):
        r'''
        A function to find the integer p modulo :math:`\equiv`, of two
        elements of a natural semiring, since this is the mutliplicative
        operation of a natural semiring. Here :math:`\equiv` is the congruence
        of the natural semiring.

        Args:
            x (int):    One of the elements to be added.
            y (int):    The other of the elements to be added.

        Returns:
            int:   The integer product modulo :math:`\equiv`, of x and y.

        Raises:
            TypeError:  If x and y are not both ints.
            ValueError: If either x or y is negative, or greater than :math:`t
                        + p - 1`.

        Examples:
            >>> from semigroups import NaturalSemiring
            >>> NaturalSemiring(5, 7).prod(3, 10)
            9
        '''
        if not (isinstance(x, int) and isinstance(y, int)):
            raise TypeError
        if not ((0 <= x < self._threshold + self._period) and
                (0 <= y < self._threshold + self._period)):
            raise ValueError

        return (x * y - self._threshold) % self._period + self._threshold

    def period(self):
        '''
        A function to find the period of a Natural Semiring instance.

        Returns:
            int:    period.

        Raises:
            TypeError:  If any argument is given.

        Examples:
            >>> from semigroups import NaturalSemiring
            >>> NaturalSemiring(5, 7).period()
            7
        '''
        return self._period

    @staticmethod
    def zero():
        '''
        A function to find the additive identity of a natural semiring, which
        is 0.

        Returns:
            int:    0

        Raises:
            TypeError:  If any argument is given.

        Examples:
            >>> from semigroups import NaturalSemiring
            >>> NaturalSemiring(5, 7).zero()
            0
        '''
        return 0

    @staticmethod
    def one():
        '''
        A function to find the multiplicative identity of a natural semiring,
        which is 1.

        Returns:
            int:    1

        Raises:
            TypeError:  If any argument is given.

        Examples:
            >>> from semigroups import NaturalSemiring
            >>> NaturalSemiring(5, 7).one()
            1
        '''
        return 1
