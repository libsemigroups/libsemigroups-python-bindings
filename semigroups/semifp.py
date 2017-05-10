import libsemigroups


class FpSemigroup(libsemigroups.FpSemigroupNC):
    '''
    A class for finitely presented semigroups.

    Args:
        alphabet (list): the generators of the finitely presented semigroup,
            must be a list of strings of length 1.

        rels (list): the relations containing pairs of string which are
            equivalent in the finitely presented semigroup

    Raises:
        TypeError: if TODO

        ValueError: if TODO

    Examples:
        >>> FpSemigroup(['a', 'b'],
        ...             [['aa', 'a'], ['bbb', 'ab'], ['ab', 'ba']])
        <fp semigroup with 2 generators and 3 relations>

    TODO:
         write == method
         write normal_form method
         test compatability with existing semigroup member functions
         add link to documentation for functions when it becomes available.
    '''

    def __check_word(self, word):
        '''
        Check if word is a valid word over the alphabet of this.
        '''
        if not isinstance(word, str):
            raise TypeError('the argument must be a string')
        for letter in word:
            if letter not in self.alphabet:
                raise ValueError('the letter %s ' % letter
                                 + ' does not belong to the alphabet %s'
                                 % self.alphabet)

    def __init__(self, alphabet, rels):
        # Check the alphabet
        if not isinstance(alphabet, list):
            raise TypeError('the first argument (alphabet) must be a list')
        elif not all(isinstance(x, str) or alphabet.count(x) > 1
                     for x in alphabet):
            raise ValueError('the first argument (alphabet) must be a '
                             'duplicate-free list of strings')

        # Corner case
        if len(alphabet) == 0 and not len(rels) == 0:
            raise ValueError('the empty semigroup must not have'
                             + ' any relations')
        # Check the relations
        if not (isinstance(rels, list)
                and all(isinstance(rel, list) for rel in rels)):
            raise TypeError('the second argument (relations) must be a ' +
                            'list of lists')
        elif not all(len(rel) == 2 and isinstance(rel[0], str)
                     and isinstance(rel[1], str) for rel in rels):
            raise TypeError('the second argument (relations) must be a ' +
                            'list of pairs of strings')

        # TODO parse relations using ^ etc here, as per in ParseRelators in GAP
        self.alphabet = alphabet
        self.relations = rels

        for rel in rels:
            for word in rel:
                self.__check_word(word)

        libsemigroups.FpSemigroupNC.__init__(self, len(alphabet), rels)

    def __repr__(self):
        return ("<fp semigroup with %d generators and %d relations>"
                % (len(self.alphabet), len(self.relations)))

    def size(self):
        '''Attempt to compute the size of the finitely presented semigroup.

        Returns:
            int: the size of the finitely presented semigroup.

        Examples:
            >>> FpSemigroup(['a', 'b'],
            ...             [['aa', 'a'], ['bbb', 'ab'], ['ab', 'ba']]).size()
            5
            >>> FpMonoid(['a', 'b'],
            ...          [['aa', 'a'], ['bbb', 'ab'], ['ab', 'ba']]).size()
            6
            >>> FpMonoid(['a', 'b'],
            ...          [['aa', 'a'], ['bbb', 'ab'], ['ab', 'ba']]).size()
            6
        '''
        if not self.is_finite():
            return float('inf')
        return libsemigroups.FpSemigroupNC.size(self)

    def is_finite(self):
        '''Attempts to check if a finitely presented semigroup is finite.

        Returns:
            bool: ``True`` if finite, ``False`` otherwise.

        Examples:
            >>> S = FpSemigroup(['a', 'b'],
            ...                 [['aa', 'a'],['bbb', 'ab'], ['ab','ba']])
            >>> S.is_finite()
            True
            >>> FpSemigroup(['a', 'b'], []).is_finite()
            False
        '''
        # Check if number of generators exceeds number of relations
        if len(self.relations) < len(self.alphabet):
            return False

        # Check if any generator belongs to no relation
        for letter in self.alphabet:
            for rel in self.relations:
                for word in rel:
                    if letter in word:
                        stop = True
                        break
                if stop:
                    break
            else:
                return False

        return (isinstance(libsemigroups.FpSemigroupNC.size(self), int) or
                isinstance(libsemigroups.FpSemigroupNC.size(self), long))

    def word_to_class_index(self, word):
        '''Returns the class index of a given word.

        Args:
            word (str): word whose class index is to be returned.

        Returns:
            int: class index of the given word.

        Raises:
            TypeError: if TODO
            ValueError: if TODO

        Examples:
            >>> S = FpSemigroup(['a', 'b'],
            ...                 [['aa', 'a'], ['bbb', 'ab'], ['ab', 'ba']])
            >>> S.word_to_class_index('a')
            0
            >>> S.word_to_class_index('b')
            1
        '''

        self.__check_word(word)
        return libsemigroups.FpSemigroupNC.word_to_class_index(self, word)


class FpMonoid(FpSemigroup):
    def __init__(self, alphabet, rels):
        '''
        Construct a finitely presented monoid from generators and relations.
        '''
        if '1' in alphabet:
            raise ValueError('the first argument (alphabet) must '
                             + 'not contain 1')
        alphabet = alphabet[:]
        rels = rels[:] + [['11', '1']]
        for letter in alphabet:
            rels.append([letter + '1', letter])
            rels.append(['1' + letter, letter])
        alphabet.append('1')
        FpSemigroup.__init__(self, alphabet, rels)

    def __repr__(self):
        nrgens = len(self.alphabet) - 1
        nrrels = len(self.relations) - 2 * nrgens - 1
        return ("<fp monoid with %d generators and %d relations>"
                % (nrgens, nrrels))
