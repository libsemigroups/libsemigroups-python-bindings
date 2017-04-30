# pylint: disable = C0103,E0611,C0111,W0104,R0201
import unittest
import sys
import os
from semigroups import FpSemigroup, FpMonoid

path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if path not in sys.path:
    sys.path.insert(1, path)
del path


class TestFpSemigroup(unittest.TestCase):

    def test_valid_init(self):
        FpSemigroup(['a'], [])
        FpSemigroup(['a'], [['a', 'aa']])
        FpSemigroup(['a', 'b'], [['b', 'aa']])

    def test_alphabet_str(self):
        with self.assertRaises(ValueError):
            FpSemigroup([], [['a', 'aa']])
        with self.assertRaises(ValueError):
            FpSemigroup(['a'], [['b', 'aa']])
        with self.assertRaises(ValueError):
            FpSemigroup(['a', 'a'], [['b', 'aa']])

    def test_rels_str(self):
        with self.assertRaises(TypeError):
            FpSemigroup(["a", "b"], "[\"a\", \"aa\"]")
        with self.assertRaises(TypeError):
            FpSemigroup(["a", "b"], ["\"b", "aa\""])
        with self.assertRaises(TypeError):
            FpSemigroup(["a", "b"], [["a", "aa", "b"]])
        with self.assertRaises(TypeError):
            FpSemigroup(["a", "b"], [["b", ["a", "a"]]])
        with self.assertRaises(ValueError):
            FpSemigroup(["a", "b"], [["b", "ca"]])

    def test_set_report_str(self):
        S = FpSemigroup(["a"], [["a", "aa"]])
        S.set_report(True)
        S.set_report(False)
        with self.assertRaises(TypeError):
            S.set_report("False")

    def test_size_str(self):
        S = FpSemigroup(["a"], [["a", "aa"]])
        self.assertEqual(S.size(), 1)
        S = FpSemigroup(["a", "b"], [["a", "aa"], ["b", "bb"], ["ab", "ba"]])
        self.assertEqual(S.size(), 3)

    def test_word_to_class_index_str(self):
        S = FpSemigroup(["a", "b"], [["a", "aa"], ["b", "bb"], ["ab", "ba"]])

        self.assertIsInstance(S.word_to_class_index("aba"), int)

        with self.assertRaises(TypeError):
            S.word_to_class_index([1, "0"])

        with self.assertRaises(TypeError):
            S.word_to_class_index(["aba"])

        self.assertEqual(S.word_to_class_index("aba"),
                         S.word_to_class_index("abaaabb"))

    def test_repr(self):
        S = FpSemigroup(["a", "b"], [["aa", "a"], ["bbb", "ab"], ["ab", "ba"]])
        self.assertEqual(S.__repr__(),
                         "<fp semigroup with 2 generators and 3 relations>")

class TestFpMonoid(unittest.TestCase):

    def test_valid_init(self):
        FpMonoid([], [])
        FpMonoid(["a"], [])
        FpMonoid(["a"], [["a", "aa"]])
        FpMonoid(["a", "b"], [["b", "aa"]])
        FpMonoid(["a", "b"], [["1", "aa"]])

    def test_alphabet_str(self):
        with self.assertRaises(ValueError):
            FpMonoid([], [["a", "aa"]])
        with self.assertRaises(ValueError):
            FpMonoid(["a"], [["b", "aa"]])
        with self.assertRaises(ValueError):
            FpMonoid(["a", "a"], [["b", "aa"]])

    def test_rels_str(self):
        with self.assertRaises(TypeError):
            FpMonoid(["a", "b"], "[\"a\", \"aa\"]")
        with self.assertRaises(TypeError):
            FpMonoid(["a", "b"], ["\"b\", \"aa\""])
        with self.assertRaises(TypeError):
            FpMonoid(["a", "b"], [["a", "aa", "b"]])
        with self.assertRaises(TypeError):
            FpMonoid(["a", "b"], [["b", ["a", "a"]]])
        with self.assertRaises(ValueError):
            FpMonoid(["a", "b"], [["b", "ca"]])

    def test_set_report_str(self):
        M = FpMonoid(["a"], [["a", "aa"]])
        M.set_report(True)
        M.set_report(False)
        with self.assertRaises(TypeError):
            M.set_report("False")

    def test_size(self):
        self.assertEqual(FpMonoid(["a"], [["a", "aa"]]).size(), 2)
        self.assertEqual(FpMonoid(["a", "b"], [["a", "aa"], ["b", "bb"],
        ["ab", "ba"]]).size(), 4)

    def test_word_to_class_index_str(self):
        M = FpMonoid(["a", "b"], [["a", "aa"], ["b", "bb"], ["ab", "ba"]])
        self.assertEqual(M.word_to_class_index('a'),
                         M.word_to_class_index('aa'))
        self.assertNotEqual(M.word_to_class_index('a'),
                            M.word_to_class_index('bb'))

        self.assertIsInstance(M.word_to_class_index('aba'), int)

    def test_repr(self):
        M = FpMonoid(["a", "b"], [["aa", "a"], ["bbb", "ab"], ["ab", "ba"]])
        self.assertEqual(M.__repr__(),
                         "<fp monoid with 2 generators and 3 relations>")

if __name__ == "__main__":
    unittest.main()
