import libsemigroups


class FpSemigroup(libsemigroups.FpSemigroupNC):
    '''
    Class for finitely presented semigroups

    Examples:
        >>> FpSemigroup(['a', 'b'],
        ...             [['aa', 'a'], ['bbb', 'ab'], ['ab', 'ba']])

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
        '''
        Construct an FpSemigroup from generators and relations.

        Args:
            alphabet (list): the generators of the fp semigroup, must be
            either a list of ints or a list of strings of length 1.

            rels (list): the relations containing pairs of words which are
            equivalent in the given FpSemigroup, must be a list of length 2
            lists of lists of ints or a list of length 2 lists of strings.

        Raises:
            TypeError: If the alphabet is not a list of integers or strings,
            if the relations are not a double nested list of integers or a
            nested list strings.

            ValueError: If the alphabet contains repeated elements, if any of
            the lists which are supposed to contain pairs of words don't
            contain 2 elements or any of the words in relations use generators
            not in the given alphabet.
        '''
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
        '''
        Compute the size of a finitely presented semigroup.

        Examples:
            >>> FpSemigroup(['a','b'],[['aa','a'],['bbb','ab'],
            ...                                 ['ab','ba']]).size()
            5
            >>> FpMonoid(['a','b'],[['aa','a'],['bbb','ab'],
            ...                                      ['ab','ba']]).size()
            6
            >>> FpMonoid(['a','b'],[['aa','a'],['bbb','ab'],
            ...                                      ['ab','ba']]).size()
            6

        Returns:
            int: The size of the FpSemigroup.

        '''
        if not self.is_finite():
            return float('inf')
        return libsemigroups.FpSemigroupNC.size(self)

    def is_finite(self):
        '''
        Attempts to check if a finitely presented semigroup is finite.

        Examples:
            >>> S = FpSemigroup(['a', 'b'],
            ...                 [['aa', 'a'],['bbb', 'ab'], ['ab','ba']])
            >>> S.is_finite()
            True
            >>> FpSemigroup(['a', 'b'], []).is_finite()
            False

        Returns:
            bool: True for finite, False otherwise.
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
        '''
        returns the class index of a given word

        Examples:
        >>> FpS=FpSemigroup(['a', 'b'],
        ...                 [['aa', 'a'], ['bab', 'ab'], ['ab', 'ba']])
        >>> FpS.word_to_class_index('a')
        0
        >>> FpS.word_to_class_index('b')
        1

        Args:
            FpSemigroupElement:word whose class index is to be returned.

        Returns:
            int: class index of the given word.

        Raises:
            TypeError: if 1st argument is not an FpSemigroupElement.
            ValueError: if 1st argument is an FpSemigroupElement
            but not in this semigroup.
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
