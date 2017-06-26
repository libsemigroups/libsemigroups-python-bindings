'''
This module contains the classes FpSemigroup and FpMonoid.
'''
# pylint: disable = no-member, len-as-condition, invalid-name
import libsemigroups
from semigroups.semigrp import Semigroup

class FpSemigroup(libsemigroups.FpSemigroupNC, Semigroup):
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
         edit normal_form method
    '''
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

        self._pure_letter_alphabet = True
        for i in alphabet:
            if not i in ('abcdefghijklmnopqrstuvwxyz1' +
                         'ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
                pure_letter_alphabet = False
                break

        for i, rel in enumerate(rels):
            for j, word in enumerate(rel):
                rels[i][j] = self._parse_word(word)

        self.alphabet = alphabet
        self.relations = rels

        for rel in rels:
            for word in rel:
                self.check_word(word)

        libsemigroups.FpSemigroupNC.__init__(self, len(alphabet), rels)
        if not self.is_obviously_infinite():
            Semigroup.__init__(self, *[FPSOME(self, i) for i in self.alphabet])

    def _parse_word(self, word):
        '''
        Removes ^ and () from a given word.
        '''
        if self._pure_letter_alphabet:
            return _remove_powers(_remove_brackets(word))
        return word

    def check_word(self, word):
        '''
        Check if word is a valid word over the alphabet of this.
        '''
        if not isinstance(word, str):
            raise TypeError('the argument must be a string')
        for letter in word:
            if letter not in self.alphabet:
                raise ValueError('the letter %s' % letter
                                 + ' does not belong to the alphabet \'%s\''
                                 % self.alphabet)

    def __repr__(self):
        return ('<fp semigroup with %d generators and %d relations>'
                % (len(self.alphabet), len(self.relations)))

    def factorisation(self, word):
        '''
        Factorises a given word into a list of generators each represented by
        an integer starting at 0.

        Args:
            word (str): word to be factorised.

        Returns:
            list: factorisation into generators.

        Examples:
            >>> S = FpSemigroup('ab',[['a', 'aa'], ['b', 'bbb'], ['ab', 'ba']])
            >>> S.factorisation('b')
            [1]
            >>> S.factorisation('aaabb')
            [0, 1, 1]
        '''
        if self.is_obviously_infinite():
            raise ValueError('given semigroup is infinite')
        word = self._parse_word(word)
        self.check_word(word)
        Pyword = libsemigroups.PythonElementNC(FPSOME(self, word))
        return Semigroup.factorisation(self, Pyword)

    def normal_form(self, word):
        #TODO change the way this works to not use factorisation.
        '''
        Converts a given word to a simple form which it is equivalent to in
        in semigroup.

        Args:
            word (str): word to be converted.

        Returns:
            string: normal for m of the given word.

        Examples:
            >>> S = FpSemigroup('ab',[['a', 'aa'], ['b', 'bbb'], ['ab', 'ba']])
            >>> S.normal_form('b')
            'b'
            >>> S.normal_form('aaabb')
            'abb'
            >>> S.normal_form('(a^1000)bb')
            'abb'
        '''
        Factors = self.factorisation(word)
        return ''.join(self.alphabet[i] for i in Factors)

    def size(self):
        '''
        Computes the number of elements of the finitely presented semigroup.

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

    def __contains__(self, word):
        if not isinstance(word, str):
            raise ValueError('word should be a string')
        word = self._parse_word(word)
        if word == '':
            return isinstance(self, FpMonoid)
        for letter in word:
            if letter not in self.alphabet:
                return False
        return True

    def equal(self, word1, word2):
        '''
        Checks if 2 words in a finitely presented semigroup are equivalent.

        Args:
            word1 (str): 1st word to be compared.
            word2 (str): 2nd word to be compared.

        Returns:
            bool: ``True`` if equivalent, ``False`` otherwise.

        Examples:
            >>> S = FpSemigroup('ab',[['a', 'aa'], ['b', 'bbb'], ['ab', 'ba']])
            >>> S.equal('b', 'b')
            True
            >>> S.equal('b', 'bb')
            False
            >>> S.equal('a', 'aa')
            True
            >>> S.equal('ab', 'ba^1000')
            True
        '''
        if not self.is_finite():
            raise ValueError('given semigroup is infinite')
        return FPSOME(self, word1) == FPSOME(self, word2)

    def is_obviously_infinite(self):
        '''Attempts to check if a finitely presented semigroup is obviously
        infinite.

        Returns:
            bool: ``True`` if obviously infinite, ``False`` otherwise.

        Examples:
            >>> S = FpSemigroup('ab',
            ...                 [['aa', 'a'],['bbb', 'ab'], ['ab', 'ba']])
            >>> S.is_obviously_infinite()
            False
            >>> FpSemigroup('ab', []).is_obviously_infinite()
            True
        '''
        # Check if number of generators exceeds number of relations
        if len(self.relations) < len(self.alphabet):
            return True

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
                return True
        return False

    def enumerate(self, limit):
        if not self.is_finite():
            raise ValueError('given semigroup is infinite')
        return Semigroup.enumerate(self, limit)

    def nridempotents(self):
        if not self.is_finite():
            raise ValueError('given semigroup is infinite')
        return Semigroup.nridempotents(self)

    def is_finite(self):
        '''Attempts to check if a finitely presented semigroup is finite.

        Returns:
            bool: ``True`` if finite, ``False`` otherwise.

        Examples:
            >>> S = FpSemigroup('ab',
            ...                 [['aa', 'a'],['bbb', 'ab'], ['ab', 'ba']])
            >>> S.is_finite()
            True
            >>> FpSemigroup('ab', []).is_finite()
            False
        '''
        if self.is_obviously_infinite():
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
        if not self.is_finite():
            raise ValueError('given semigroup is infinite')
        if not isinstance(word, str):
            raise TypeError('given word is not a string')
        word = self._parse_word(word)
        self.check_word(word)
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

    def is_obviously_infinite(self):
        # Check if number of generators exceeds number of relations
        #(adjusted to ignore identity relations)
        if len(self.relations) + 2 < len(self.alphabet) * 3:
            return True
        FpSemigroup.is_obviously_infinite(self)

    def __repr__(self):
        nrgens = len(self.alphabet) - 1
        nrrels = len(self.relations) - 2 * nrgens - 1
        return ('<fp monoid with %d generators and %d relations>'
                % (nrgens, nrrels))

class FPSOME(libsemigroups.ElementABC):
    '''FpSemigroupElement Object
    Examples:
        >>> FpS = FpSemigroup('ab',[['aa','a'],['bbb','ab'],['ab','ba']])
        >>> FPSOME(FpS,'a')
        'a'
        >>> FPSOME(FpS,'bab')
        'bab'
    '''

    def __init__(self, FpS, word):
        '''
        Construct an FpSemigroup element from an FpSemigroup and a string.

        Args:
            FpS (FpSemigroup):  The FpSemigroup of which the given word is
                                an element.
            word (string):      a string containg generators of
                                the given semigroup.
        Raises:
            TypeError:  If 1st argument is not an FpSemigroup object or the
                        second argument is not a string or a list.
            ValueError: If the word contains a generator not n the alphabet
                        of the given semigroup.
        '''
        if not isinstance(FpS, FpSemigroup):
            raise TypeError('given Semigroup is not a valid FpSemigroup')
        if not isinstance(word, str):
            raise TypeError('given word must be a string')
        self.FpS = FpS
        self._Repword = word

        if word == '':
            if isinstance(FpS, FpMonoid):
                self.word = '1'
                self._Repword = '1'
            else:
                self.word = ''
        else:
            self.word = _remove_powers(_remove_brackets(word))

        self.FpS.check_word(self.word)

    def __eq__(self, other):
        if not (isinstance(other, FPSOME) and
                self.FpS is other.FpS):
            return False
        elif self.word == '' or other.word == '':
            return self.word == other.word
        return (self.word_to_class_index() ==
                other.word_to_class_index())

    def __ne__(self, other):
        return not self.__eq__(other)

    def word_to_class_index(self):
        return self.FpS.word_to_class_index(self.word)

    def __hash__(self):
        return self.word_to_class_index()

    @staticmethod
    def degree():
        return 0

    def identity(self):
        return FPSOME(self.FpS, '')

    def __mul__(self, other):
        if self.word == '' and other.word == '':
            raise ValueError('no empty word in this semigroup')
        if not (isinstance(other, FPSOME) and
                self.FpS is other.FpS):
            raise TypeError('given words are not members'+
                            ' of the same FpSemigroup')

        return FPSOME(self.FpS, self.word + other.word)

    def __repr__(self):
        return '\'' + self._Repword + '\''

def _remove_brackets(word):
    # pylint: disable = too-many-branches
    if word == '':
        return ''

    #if the number of left brackets is different from the number of right
    #brackets they can't possibly pair up
    if not word.count('(') == word.count(')'):
        raise ValueError('invalid bracket structue')

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
                raise ValueError('invalid bracket structure')

            #if rbracket is not followed by ^ then the value inside the
            #bracket is appended (recursion is used to remove any brackets
            #in this value)
            if rbracket + 1 == len(word):
                newword += _remove_brackets(word[lbracket + 1:
                                                 rbracket])
            elif word[rbracket + 1] != '^':
                newword += _remove_brackets(word[lbracket + 1:
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
                newword += (_remove_brackets(word[lbracket + 1:
                                                  rbracket])
                            * int(word[rbracket + 2:i]))
                i -= 1
        i += 1

    return newword

def _remove_powers(word):
    if word == '':
        return ''

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
