'''
This module contains the classes FpSemigroup and FpMonoid.
'''
# pylint: disable = no-member, len-as-condition
import libsemigroups

class FpSemigroup(libsemigroups.FpSemigroupNC):
    '''
    A *finitely presented semigroup* is a quotient of a free semigroup on
    a finite number of generators by a finitely generated congruence.

    Args:
        alphabet (string): the generators of the finitely presented semigroup,
            must be a string of distinct characters.

        rels (list): the relations containing pairs of string which are
            equivalent in the finitely presented semigroup

    Raises:
        TypeError: if the first argument is not a string or the second
                   argument is not a list of pairs of strings.

        ValueError: if the first arugment contains duplicates or the relations
                    in the second argument reference a character not in the
                    alphabet.

    Examples:
        >>> FpSemigroup('ab',
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

    def __remove_brackets(self, word):
        # pylint: disable = too-many-branches
        if word == '':
            return ''

        #if the number of left brackets is different from the number of right
        #brackets they can't possibly pair up
        if not word.count('(') == word.count(')'):
            raise ValueError('unmatched bracket')

        #if the ^ is at the end of the string there is no exponent.
        #if the ^ is at the start of the string there is no base.
        if word[0] == '^' or word[-1] == '^':
            raise ValueError('invalid power structure')

        #checks that all ^s have an exponent.
        for index, element in enumerate(word):
            if element == '^':
                if not word[index + 1] in '0123456789':
                    raise ValueError('invalid power structure')

        #i acts as a pointer to positions in the string.
        newword = ''
        i = 0
        while i < len(word):
            #if there are no brackets the character is left as it is.
            if word[i] != '(':
                newword += word[i]
            else:
                lbracket = i
                rbracket = -1
                #tracks how 'deep' the position of i is in terms of nested
                #brackets
                nestcount = 0
                i += 1
                while i < len(word):
                    if word[i] == '(':
                        nestcount += 1
                    elif word[i] == ')':
                        if nestcount == 0:
                            rbracket = i
                            break
                        else:
                            nestcount -= 1
                    i += 1

                #as i is always positive, if rbracket is -1 that means that
                #the found left bracket has no corresponding right bracket.
                #note: if this never occurs then every left bracket has a
                #corresponding right bracket and as the number of each bracket
                #is equal every right bracket has a corresponding left bracket
                #and the bracket structure is valid.
                if rbracket == -1:
                    raise ValueError('unmatched bracket')

                #if rbracket is not followed by ^ then the value inside the
                #bracket is appended (recursion is used to remove any brackets
                #in this value)
                if rbracket + 1 == len(word):
                    newword += self.__remove_brackets(word[lbracket + 1:
                                                           rbracket])
                elif word[rbracket + 1] != '^':
                    newword += self.__remove_brackets(word[lbracket + 1:
                                                           rbracket])
                #if rbracket is followed by ^ then the value inside the
                #bracket is appended the given number of times
                else:
                    i += 2
                    while i < len(word):
                        if word[i] in '0123456789':
                            i += 1
                        else:
                            break
                    newword += (self.__remove_brackets(word[lbracket + 1:
                                                            rbracket])
                                * int(word[rbracket + 2:i]))
                    i -= 1
            i += 1

        return newword

    @staticmethod
    def __remove_powers(word):
        if word == '':
            return ''

        #if the ^ is at the end of the string there is no exponent.
        #if the ^ is at the start of the string there is no base.
        if word[0] == '^' or word[-1] == '^':
            raise ValueError('invalid power structure')

        #checks that all ^s have an exponent.
        for index, element in enumerate(word):
            if element == '^':
                if not word[index + 1] in '0123456789':
                    raise ValueError('invalid power structure')

        newword = ''
        i = 0
        while i < len(word):
            #if last character reached there is no space for exponentiation.
            if i == len(word) - 1:
                newword += word[i]
                i += 1
            #if the character is not being powered then it is left as it is.
            elif word[i + 1] != '^':
                newword += word[i]
                i += 1
            else:
                base_position = i
                i += 2
                if i < len(word):
                    #extracts the exponent from the string.
                    while word[i] in '0123456789':
                        i += 1
                        if i >= len(word):
                            break
                newword += (word[base_position] *
                            int(word[base_position + 2:i]))
        return newword

    def __remove_powers_and_brackets(self, word):
        '''
        Removes ^ and () from a given word.
        '''
        return self.__remove_powers(self.__remove_brackets(word))

    def __init__(self, alphabet, rels):
        # Check the alphabet
        if not isinstance(alphabet, str):
            raise TypeError('the first argument (alphabet) must be a string')
        elif not all(alphabet.count(i) == 1 for i in alphabet):
            raise ValueError('the first argument (alphabet) must be a '
                             'duplicate-free string')

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

        pure_letter_alphabet = True
        for i in alphabet:
            if not i in ('abcdefghijklmnopqrstuvwxyz1' +
                         'ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
                pure_letter_alphabet = False
                break

        if pure_letter_alphabet:
            for i, rel in enumerate(rels):
                for j, word in enumerate(rel):
                    rels[i][j] = self.__remove_powers_and_brackets(word)

        self.alphabet = alphabet
        self.relations = rels

        for rel in rels:
            for word in rel:
                self.__check_word(word)

        libsemigroups.FpSemigroupNC.__init__(self, len(alphabet), rels)

    def __repr__(self):
        return ('<fp semigroup with %d generators and %d relations>'
                % (len(self.alphabet), len(self.relations)))

    def size(self):
        '''
        Attempts to compute the number of elements of the finitely
        presented semigroup.

        Returns:
            int: the size of the finitely presented semigroup.

        Examples:
            >>> FpSemigroup('ab',
            ...             [['aa', 'a'], ['bbb', 'ab'], ['ab', 'ba']]).size()
            5
            >>> FpMonoid('ab',
            ...          [['aa', 'a'], ['bbb', 'ab'], ['ab', 'ba']]).size()
            6
            >>> FpMonoid('ab',
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
            >>> S = FpSemigroup('ab',
            ...                 [['aa', 'a'],['bbb', 'ab'], ['ab','ba']])
            >>> S.is_finite()
            True
            >>> FpSemigroup('ab', []).is_finite()
            False
        '''
        # Check if number of generators exceeds number of relations
        if len(self.relations) < len(self.alphabet):
            return False

        # Check if any generator belongs to no relation
        for letter in self.alphabet:
            stop = False
            for rel in self.relations:
                for word in rel:
                    if letter in word:
                        stop = True
                        break
                if stop:
                    break
            if not stop:
                return False

        return isinstance(libsemigroups.FpSemigroupNC.size(self), int)

    def word_to_class_index(self, word):
        '''Returns the class index of a given word.

        The class index of a word is a number used to represent the set
        of words equivalent to that word in the semigroup.

        Args:
            word (str): word whose class index is to be returned.

        Returns:
            int: class index of the given word.

        Raises:
            TypeError: if the argument is not a string.
            ValueError: if the argument contains a character not in the
                        alphabet of the FpSemigroup.

        Examples:
            >>> S = FpSemigroup('ab',
            ...                 [['aa', 'a'], ['bbb', 'ab'], ['ab', 'ba']])
            >>> S.word_to_class_index('a')
            0
            >>> S.word_to_class_index('b')
            1
        '''
        self.__check_word(word)
        return libsemigroups.FpSemigroupNC.word_to_class_index(self, word)


class FpMonoid(FpSemigroup):
    '''
    A *finitely presented monoid* is a quotient of a free monoid on a
    finite number of generators over a finitely generated congruence
    on the free monoid.

    Args:
        alphabet (string): the generators of the finitely presented semigroup,
            must be a string of distinct characters.

        rels (list): the relations containing pairs of string which are
            equivalent in the finitely presented semigroup

    Raises:
        TypeError: if the first argument is not a string or the second
                   argument is not a list of pairs of strings.

        ValueError: if the first arugment contains duplicates, if the first
                    argument contains a 1 or if the relations in the second
                    argument reference a character not in the alphabet.

    Examples:
        >>> FpMonoid('ab',
        ...             [['aa', 'a'], ['bbb', 'ab'], ['ab', 'ba']])
        <fp monoid with 2 generators and 3 relations>
    '''

    def __init__(self, alphabet, rels):
        if '1' in alphabet:
            raise ValueError('the first argument (alphabet) must '
                             + 'not contain 1')
        alphabet = alphabet[:]
        rels = rels[:] + [['11', '1']]
        for letter in alphabet:
            rels.append([letter + '1', letter])
            rels.append(['1' + letter, letter])
        alphabet += '1'
        FpSemigroup.__init__(self, alphabet, rels)

    def __repr__(self):
        nrgens = len(self.alphabet) - 1
        nrrels = len(self.relations) - 2 * nrgens - 1
        return ('<fp monoid with %d generators and %d relations>'
                % (nrgens, nrrels))
