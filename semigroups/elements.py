'''
This module contains classes for representing elements of semigroups.
'''
# pylint: disable = no-member, protected-access, invalid-name,
# pylint: disable = too-few-public-methods

import libsemigroups


class Transformation(libsemigroups.TransformationNC):
    '''
    A class for handling libsemigroups transformations.

    A transformation f is a function defined on the set {0, 1, ..., n - 1}
    for some integer n called the degree of f. A transformation is stored as a
    list of the images of {0, 1, ..., n - 1},
    i.e. [(0)f, (1)f, ..., (n - 1)f].

    Args:
        List (list): Image list of the Transformation when applied to
        [0, 1, ..., n]

    Raises:
        TypeError:  If the arg is not a list of ints, or if there is more than
                    one arg.
        ValueError: If the elements of the list are negative, or the max of the
                    list + 1 is greater than the length of the list.

    Example:
        >>> from semigroups import Transformation
        >>> Transformation([2, 1, 1])
        Transformation([2, 1, 1])
    '''
    def __init__(self, arg):
        if isinstance(arg, libsemigroups.ElementABC):
            # construct an uninitialised Transformation
            libsemigroups.ElementABC.__init__(self)
        elif not isinstance(arg, list):
            raise TypeError('<arg> must be a list, not a %s' % type(arg))
        elif not all(isinstance(x, int) and x >= 0 for x in arg):
            raise TypeError('<arg> must only contain non-negative ints')
        elif max(arg) + 1 > len(arg):
            raise ValueError('<arg> must not contain values exceeding %d'
                             % len(arg))
        else:
            libsemigroups.TransformationNC.__init__(self, arg)

    def __repr__(self):
        return 'Transformation(%s)' % str(list(self))


class PartialPerm(libsemigroups.PartialPermNC):

    '''
    A class for handles to libsemigroups partial perm.

    A partial permutation f is an injective partial transformation, which is
    stored as a list of the images of {0, 1, ..., n -1}, i.e.
    [(0)f, (1)f, ..., (n - 1)f] where the value -1 is used to indicate i(f) is
    undefined.

    Args:
        args (list):    Image list of the partial permutation when applied to
                        [0, 1, ..., n], -1 being used to indicate the image is
                        undefined.

        args (list):    List containing the domain, as a list of ints, then the
                        range, as a list of ints, then the degree.

    Raises:
        TypeError:  During the second arg format, if the domain or range are
                    not both lists, the degree is not an int, or the elements
                    of the domain and range are not ints.
        ValueError: If the domain and range are of different lengths, if the
                    degree is negative, if the domain or range contains an
                    element greater than or equal to the degree, or if the
                    domain or range have repeats.

    Example:
        >>> from semigroups import PartialPerm
        >>> PartialPerm([1, 2, 5], [2, 3, 5], 6)
        PartialPerm([1, 2, 5], [2, 3, 5], 6)
    '''

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], libsemigroups.ElementABC):
            # construct an uninitialised PartialPerm
            libsemigroups.ElementABC.__init__(self)
            self._domain = None
            self._range = None
            return
        elif not (isinstance(args[0], list)
                  and all(isinstance(x, int) and x >= 0 for x in args[0])):
            raise TypeError('the first argument (domain) must be a list '
                            + 'of integers')
        elif not (isinstance(args[1], list)
                  and all(isinstance(x, int) and x >= 0 for x in args[1])):
            raise TypeError('the second argument (range) must be a list '
                            + 'of integers')
        elif not isinstance(args[2], int) and args[2] >= len(args[0]):
            raise TypeError('the third argument (degree) must '
                            + 'be an integer')
        elif args[2] < 0:
            raise ValueError('the third argument (degree) must '
                             + 'be a non-negative integer')
        elif len(args[0]) != len(args[1]):
            raise ValueError('the first and second arguments must have '
                             + 'equal length')
        elif (len(args[0]) > 0
              and max(max(args[0]), max(args[1])) >= args[2]):
            raise ValueError('the max of the domain and range must '
                             + 'be strictly less than the degree')
        elif len(args[0]) > len(set(args[0])):
            raise ValueError('the first argument (domain) must not contain '
                             + 'duplicates')
        elif len(args[1]) > len(set(args[1])):
            raise ValueError('the second argument (range) must not contain '
                             + 'duplicates')

        if len(args[0]) == 0:
            self._domain, self._range = [], []
        else:
            self._domain, self._range = zip(*sorted(zip(args[0], args[1])))
            self._domain, self._range = list(self._domain), list(self._range)
        images = [65535] * args[2]

        for i in range(len(self._domain)):
            images[self._domain[i]] = self._range[i]
        libsemigroups.PartialPermNC.__init__(self, images)

    def _init_dom_ran(self):
        if self._domain is None or self._range is None:
            self._domain, self._range = [], []
            images = [i for i in self]
            for i in range(self.degree()):
                if images[i] != 65535 and images[i] != -1:
                    self._domain.append(i)
                    self._range.append(images[i])

    def __repr__(self):
        self._init_dom_ran()
        return ('PartialPerm(%s, %s, %s)'
                % (self._domain,
                   self._range,
                   self.degree())).replace('65535', '-')

    def domain(self):
        '''
        Function for finding the domain of the partial permutation, that
        maps to defined elements.

        Args:
            None

        Returns:
            list: The domain of the partial permutation

        Raises:
            TypeError:  If any argument is given.

        Example:
            >>> from semigroups import PartialPerm
            >>> PartialPerm([1, 2, 5], [2, 3, 5], 6).domain()
            [1, 2, 5]
        '''
        self._init_dom_ran()
        return self._domain

    def range(self):
        '''
        Function for finding the range of the partial permutation.

        Args:
            None

        Returns:
            list: The range of the partial permutation

        Raises:
            TypeError:  If any argument is given.

        Example:
            >>> from semigroups import PartialPerm
            >>> PartialPerm([1, 2, 5], [2, 3, 5], 6).range()
            [2, 3, 5]
        '''
        self._init_dom_ran()
        return self._range


class Bipartition(libsemigroups.BipartitionNC):
    r'''A class for bipartitions.

    A bipartition is a partition of the set :math:`\{-n, ..., -1, 1, ..., n\}`
    for some integer n. This can be stored as a list of blocks, the subsets
    of the bipartition

    Args:
        args (lists):   The blocks of the bipartition as lists.

    Raises:
        TypeError:  If any of the blocks are not lists
        ValueError: If the union of the blocks is not the set {-n, ..., -1}
                    union {1, ..., n}

    Example:
        >>> from semigroups import Bipartition
        >>> Bipartition([1, -1], [2, 3, -2], [-3])
        Bipartition([[1, -1], [2, 3, -2], [-3]])
    '''

    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], libsemigroups.ElementABC):
                # construct an uninitialised Bipartition
                libsemigroups.ElementABC.__init__(self)
                self._blocks = None
                return
            elif len(args[0]) > 0 and isinstance(args[0][0], list):
                self.__init__(*args[0])
                return

        if (not all(isinstance(x, list) for x in args)
                or not all(len(set(x)) == len(x) for x in args)):
            raise TypeError('the arguments must be duplicate-free lists')
        elif not all(isinstance(i, int) and i != 0 for x in args for i in x):
            raise TypeError('the arguments must be lists of non-zero integers')

        copy = set().union(*args)
        n = max(copy)

        if (len(copy) != 0
                and copy != set(range(1, n + 1)).
                union(set(range(-1, -1 * n - 1, -1)))):
            raise ValueError('the union of the arguments must be '
                             + '[-%s .. -1, 1 .. %s],' % (n, n))

        copy = [x[:] for x in args]
        for i in range(len(copy)):
            for j in range(len(copy[i])):
                if copy[i][j] < 0:
                    copy[i][j] = abs(copy[i][j]) + n

        copy = [sorted(x) for x in copy]
        copy.sort()

        lookup = [0] * 2 * n
        next_block = 0
        for i in range(len(copy)):
            for j in copy[i]:
                lookup[j - 1] = next_block
            next_block += 1

        for i in range(len(copy)):
            for j in range(len(copy[i])):
                if copy[i][j] > n:
                    copy[i][j] = -1 * copy[i][j] + n

        self._blocks = copy
        libsemigroups.BipartitionNC.__init__(self, lookup)

    def block(self, index):
        '''
        Function for finding the index of the block that a given element is in.

        The blocks are ordered by lowest element absolute value,
        where all negative elements are greater than all positive elements.

        Args:
            element (int): The element in question

        Returns:
            int: The index of the block that the element is in

        Raises:
            ValueError: If the element is not in the bipartition

        Example:
            >>> from semigroups import Bipartition
            >>> Bipartition([1, 2], [-2, -1, 3], [-3]).block(-2)
            1
        '''
        n = self.degree()
        if not isinstance(index, int):
            raise TypeError('the argument (index) must be an int')
        elif index > n or index < -n or index == 0:
            raise IndexError(('the argument (index = %s) must be in ' % index)
                             + ('[-%d .. -1, 1 .. %d],' % (n, n)))
        if index < 0:
            index = n - index - 1
        else:
            index -= 1
        return libsemigroups.BipartitionNC.block(self, index)

    def blocks(self):
        '''
        Function for finding the blocks of a bipartition

        Args:
            None

        Returns:
            list: The blocks of the bipartition

        Raises:
            TypeError:  If any argument is given.

        Example:
            >>> from semigroups import Bipartition
            >>> Bipartition([1, 2], [-2, -1, 3], [-3]).blocks()
            [[1, 2], [3, -1, -2], [-3]]
        '''
        if self._blocks is None:
            blocks = [[] for i in range(self.nr_blocks())]
            n = self.degree()
            for i in range(1, n + 1):
                val = self.block(i)
                assert val < len(blocks)
                blocks[val].append(i)
            for i in range(-1, - n - 1, -1):
                val = self.block(i)
                assert val < len(blocks)
                blocks[val].append(i)
            self._blocks = blocks
        return self._blocks

    def __repr__(self):
        return 'Bipartition(%s)' % self.blocks()


class BooleanMat(libsemigroups.BooleanMatNC):
    '''
    A class for handles to libsemigroups BooleanMat.

    A boolean matrix is a matrix with entries either True or False.

    Args:
        args (lists):   The rows of the matrix as lists.

    Raises:
        TypeError:  If any of the rows are not lists

        ValueError: If the number of lists given does not equal the length of
                    every list

    Example:
        >>> from semigroups import BooleanMat
        >>> BooleanMat([True, True], [False, True])
        BooleanMat([[1, 1], [0, 1]])
    '''

    def __init__(self, *args):
        if len(args) == 0:
            raise ValueError('there must be at least 1 argument')
        elif len(args) == 1:
            if isinstance(args[0], libsemigroups.ElementABC):
                libsemigroups.ElementABC.__init__(self)
                self._rows = None
                return
            elif len(args[0]) > 0 and isinstance(args[0][0], list):
                self.__init__(*args[0])
                return

        n = len(args)

        if not all(isinstance(row, list) for row in args):
            raise TypeError('the arguments must be lists')
        elif not all(len(row) == n for row in args):
            raise ValueError('the arguments (lists) must have equal '
                             + 'length')
        elif not (all(isinstance(x, bool) for row in args for x in row)
                  or all(isinstance(x, int) and x in [0, 1] for row in args
                         for x in row)):
            raise TypeError('the items in the arguments must all be '
                            ' bools or all be 0 or 1')

        if isinstance(args[0][0], int):
            self._rows = [[bool(x) for x in row] for row in args]
        else:
            self._rows = [row[:] for row in args]

        libsemigroups.BooleanMatNC.__init__(self, self._rows)

    def __getitem__(self, i):
        n = self.degree()
        if i >= n:
            IndexError('list index out of range')
        return self.rows()[i]

    def __repr__(self):
        return ('BooleanMat(%s)'
                % [[int(x) for x in row] for row in self.rows()])

    def rows(self):
        '''
        Function for finding the rows of a boolean matrix.

        Args:
            None

        Returns:
            list: The rows of the boolean matrix.

        Raises:
            TypeError:  If any argument is given.

        Example:
            >>> from semigroups import BooleanMat
            >>> BooleanMat([True, False], [True, True]).rows()
            [[True, False], [True, True]]
        '''
        if self._rows is None:
            n = self.degree()
            flat = [x for x in self]
            assert len(flat) == n ** 2
            self._rows = [flat[i:i + n] for i in range(0, n ** 2, n)]
        return self._rows


class PBR(libsemigroups.PBRNC):
    """
    A class for handles to libsemigroups PBR.

    A partitioned binary relation is a generalisation of a Bipartition, where
    elements are adjacent to some other elements, but a adjacent to b need not
    imply b adjacent to a.

    Args:
        args (lists):   The adjacencies of the negative elements as a list of
                        lists followed by the positive elements as a list of
                        lists

    Raises:
        TypeError:  If more less than two argments are given, if the given
                    arguments are not lists.

        ValueError: If there are a different number of positive and negative
                    elements included in the adjacencies, if any element is
                    adjacent to another element twice, if an element is
                    adjacent to an element not in the set.

    Example:
        >>> from semigroups import PBR
        >>> PBR([[1], [1, 2, -1]], [[1], [2, -1, 1]])
        PBR([[1], [-1, 1, 2]], [[1], [-1, 1, 2]])
    """

    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], libsemigroups.ElementABC):
                libsemigroups.ElementABC.__init__(self)
                self.__pos_out_neighbours = None
                self.__neg_out_neighbours = None
                return
            elif len(args[0]) > 0 and isinstance(args[0][0], list):
                self.__init__(*args[0])
                return
        elif len(args) != 2:
            raise ValueError('expected two arguments (negative and ' +
                             'positive out-neighbours) received %d'
                             % len(args))
        elif not all(isinstance(x, list) for x in args):
            raise TypeError('the arguments must be lists')
        elif len(args[0]) != len(args[1]):
            raise ValueError('the arguments (lists) must be of equal length')

        n = len(args[0])
        for adj in args[0] + args[1]:
            if not all(isinstance(v, int) and v != 0 and abs(v) <= n
                       for v in adj):
                raise ValueError('the arguments must consist of integers in '
                                 + 'the range [-%d .. -1, 1 .. %d]' % (n, n))
            elif len(adj) != len(set(adj)):
                raise ValueError('the arguments must consist of '
                                 'duplicate-free lists')

        self.__pos_out_neighbours = [sorted(adj) for adj in args[0]]
        self.__neg_out_neighbours = [sorted(adj) for adj in args[1]]

        def _convert_to_internal_rep(outnbs):
            int_rep = []
            for adj in outnbs:
                copy = adj[:]
                for j, v in enumerate(copy):
                    if v < 0:
                        copy[j] = n - v - 1
                    else:
                        copy[j] = v - 1
                int_rep.append(sorted(copy))
            return int_rep

        int_rep = (_convert_to_internal_rep(args[0]) +
                   _convert_to_internal_rep(args[1]))

        libsemigroups.PBRNC.__init__(self, int_rep)

    def __repr__(self):
        if (self.__neg_out_neighbours is None or
                self.__pos_out_neighbours is None):
            n = self.degree()
            self.__neg_out_neighbours, self.__pos_out_neighbours = [], []
            for i, adj in enumerate(self):
                copy = []
                for v in adj:
                    if v < n:
                        copy.append(v + 1)
                    else:
                        copy.append(n - v - 1)
                if i < n:
                    self.__pos_out_neighbours.append(sorted(copy))
                else:
                    self.__neg_out_neighbours.append(sorted(copy))
        return ('PBR(%s, %s)'
                % (self.__pos_out_neighbours, self.__neg_out_neighbours))
