# pylint: disable = C0103,E0611,C0111,W0104,R0201
import unittest
import sys
import os

path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from semigroups import FpSemigroup
from semigroups import FpSemigroupElement
from semigroups import FpMonoid
from semigroups import FpMonoidElement

class TestFpSemigroup(unittest.TestCase):

    def test_valid_init(self):
        FpSemigroup([0, 1], [])
        FpSemigroup([0, 1], [[[0], [0, 0]]])
        FpSemigroup([0, 1, 2], [[[1], [0, 0]]])

        FpSemigroup(["a"], [])
        FpSemigroup(["a"], [["a", "aa"]])
        FpSemigroup(["a", "b"], [["b", "aa"]])

    def test_alphabet_str(self):
        with self.assertRaises(ValueError):
            FpSemigroup([], [["a", "aa"]])
        with self.assertRaises(ValueError):
            FpSemigroup(["a"], [["b", "aa"]])
        with self.assertRaises(ValueError):
            FpSemigroup(["a", "a"], [["b", "aa"]])

    def test_alphabet_int(self):
        with self.assertRaises(ValueError):
            FpSemigroup([], [[[1], [0, 0]]])
        with self.assertRaises(TypeError):
            FpSemigroup(1, [[[1], [0, 0]]])

    def test_rels_str(self):
        with self.assertRaises(TypeError):
            FpSemigroup(["a", "b"], "[\"a\", \"aa\"]")
        with self.assertRaises(TypeError):
            FpSemigroup(["a", "b"], ["\"b", "aa\""])
        with self.assertRaises(ValueError):
            FpSemigroup(["a", "b"], [["a", "aa", "b"]])
        with self.assertRaises(TypeError):
            FpSemigroup(["a", "b"], [["b", ["a", "a"]]])
        with self.assertRaises(ValueError):
            FpSemigroup(["a", "b"], [["b", "ca"]])

    def test_rels_int(self):
        with self.assertRaises(TypeError):
            FpSemigroup([0, 1], "[[1], [0, 0]]")
        with self.assertRaises(TypeError):
            FpSemigroup([0, 1], ["[1], [0, 0]"])
        with self.assertRaises(ValueError):
            FpSemigroup([0, 1], [[[1], [0, 0], [1]]])
        with self.assertRaises(TypeError):
            FpSemigroup([0, 1], [[[1], "0, 0"]])
        with self.assertRaises(TypeError):
            FpSemigroup([0, 1], [[["1"], [0, 0]]])
        with self.assertRaises(ValueError):
            FpSemigroup([0, 1], [[[1], [2, 0]]])

    def test_set_report_str(self):
        S = FpSemigroup(["a"], [["a", "aa"]])
        S.set_report(True)
        S.set_report(False)
        with self.assertRaises(TypeError):
            S.set_report("False")

    def test_set_report_int(self):
        S = FpSemigroup([0], [[[0], [0, 0]]])
        S.set_report(True)
        S.set_report(False)
        with self.assertRaises(TypeError):
            S.set_report("False")

    def test_size_str(self):
        S = FpSemigroup(["a"], [["a", "aa"]])
        self.assertEqual(S.size(), 1)
        S = FpSemigroup(["a", "b"], [["a", "aa"], ["b", "bb"], ["ab", "ba"]])
        self.assertEqual(S.size(), 3)

    def test_size_int(self):
        S = FpSemigroup([0], [[[0], [0, 0]]])
        self.assertEqual(S.size(), 1)
        S = FpSemigroup([0, 1], [[[0], [0, 0]], [[1], [1, 1]], [[0, 1], [1, 0]]])
        self.assertEqual(S.size(), 3)

    def test_word_to_class_index_str(self):
        S = FpSemigroup(["a", "b"], [["a", "aa"], ["b", "bb"], ["ab", "ba"]])
        T = FpSemigroup([], [])
        aba = FpSemigroupElement(S, "aba")

        self.assertIsInstance(S.word_to_class_index(aba), int)

        with self.assertRaises(TypeError):
            S.word_to_class_index("a")

        with self.assertRaises(TypeError):
            S.word_to_class_index([1, "0"])

        with self.assertRaises(ValueError):
            S.word_to_class_index(FpSemigroupElement(T, "aba"))

        abaaabb = FpSemigroupElement(S, "abaaabb")
        self.assertEqual(S.word_to_class_index(aba),
                         S.word_to_class_index(abaaabb))

    def test_word_to_class_index_int(self):
        S = FpSemigroup([1, 2],
                        [[[1], [1, 1]], [[2], [2, 2]], [[1, 2], [2, 1]]])
        T = FpSemigroup([], [])
        aba = FpSemigroupElement(S, [1, 2, 1])

        self.assertIsInstance(S.word_to_class_index(aba), int)

        with self.assertRaises(TypeError):
            S.word_to_class_index(1)

        with self.assertRaises(TypeError):
            S.word_to_class_index([1, "0"])

        with self.assertRaises(ValueError):
            S.word_to_class_index(FpSemigroupElement(T, [1, 2, 1]))

        abaaba = FpSemigroupElement(S, [1, 2, 1, 1, 2, 1])
        self.assertEqual(S.word_to_class_index(aba),
                         S.word_to_class_index(abaaba))

    def test_repr(self):
        S = FpSemigroup([1, 2],
                        [[[1, 1], [1]], [[2, 2, 2], [2]], [[1, 2], [2, 1]]])
        self.assertEqual(S.__repr__(),
                         "<fp semigroup with 2 generators and 3 relations>")

        S = FpSemigroup(["a", "b"], [["aa", "a"], ["bbb", "ab"], ["ab", "ba"]])
        self.assertEqual(S.__repr__(),
                         "<fp semigroup with 2 generators and 3 relations>")

class TestFpSemigroupElement(unittest.TestCase):

    def test_valid_init_str(self):
        FpS = FpSemigroup(["a", "b"], [["aa", "a"], ["bbb", "b"], ["ba", "ab"]])
        FpSemigroupElement(FpS, "aba")
        FpSemigroupElement(FpS, "a")
        FpS = FpSemigroup(["m", "o"], [["ooo", "o"]])
        FpSemigroupElement(FpS, "moo")
        FpSemigroupElement(FpS, "ooo")
        FpS = FpSemigroup(list("cowie"), [])
        FpSemigroupElement(FpS, "cowie")
        with self.assertRaises(ValueError):
            FpSemigroupElement(FpS, "")
        with self.assertRaises(TypeError):
            FpSemigroupElement("aba", "aba")
        with self.assertRaises(TypeError):
            FpSemigroupElement(FpS, FpS)
        with self.assertRaises(ValueError):
            FpSemigroupElement(FpS, "abc")

    def test_valid_init_int(self):
        FpS = FpSemigroup([1, 2], [[[1, 1], [1]], [[2, 2, 2], [2]], [[2, 1], [1, 2]]])
        FpSemigroupElement(FpS, [1, 2, 1])
        FpSemigroupElement(FpS, [1])
        with self.assertRaises(ValueError):
            FpSemigroupElement(FpS, "")
        with self.assertRaises(TypeError):
            FpSemigroupElement([1, 2, 1], [1, 2, 1])
        with self.assertRaises(TypeError):
            FpSemigroupElement(FpS, FpS)
        with self.assertRaises(ValueError):
            FpSemigroupElement(FpS, [1, 2, 3])

    def test_mul_str(self):
        FpS = FpSemigroup(["a", "b"], [["aa", "a"], ["bbb", "b"], ["ba", "ab"]])
        other = "aa"
        a = FpSemigroupElement(FpS, "aba")
        a*a
        with self.assertRaises(TypeError):
            a*other
        with self.assertRaises(TypeError):
            FpSemigroupElement(FpSemigroup(["a", "b"], []), "aba")*a
        self.assertEqual((a*a).word_to_class_index(),
                         FpS.word_to_class_index(FpSemigroupElement(FpS, "abaaba")))

    def test_mul_int(self):
        FpS = FpSemigroup([1, 2],
                          [[[1, 1], [1]], [[2, 2, 2], [2]], [[2, 1], [1, 2]]])
        other = [1, 1]
        a = FpSemigroupElement(FpS, [1, 2, 1])
        a*a
        with self.assertRaises(TypeError):
            a*other
        with self.assertRaises(TypeError):
            FpSemigroupElement(FpSemigroup([1, 2], []), [1, 2, 1])*a
        abaaba = FpSemigroupElement(FpS, [1, 2, 1, 1, 2, 1])
        self.assertEqual((a*a).word_to_class_index(),
                         abaaba.word_to_class_index())

    def test_repr(self):
        S = FpSemigroup([1, 2], [[[1, 1], [1]], [[2, 2, 2], [2]]])
        self.assertEqual(FpSemigroupElement(S, [1, 2]).__repr__(),
                         "<FpSemigroup Element [1, 2]>")

        S = FpSemigroup(["a", "b"], [["aa", "a"], ["bbb", "b"], ["ab", "ba"]])
        self.assertEqual(FpSemigroupElement(S, "ab").__repr__(),
                         "<FpSemigroup Element ab>")

    def test_word_to_class_index_str(self):
        S = FpSemigroup(["a", "b"],
                        [["aa", "a"], ["bbb", "b"], ["ab", "ba"]])
        a = FpSemigroupElement(S, "a")
        aa = FpSemigroupElement(S, "aa")
        self.assertIsInstance(a.word_to_class_index(), int)
        self.assertEqual(a.word_to_class_index(), aa.word_to_class_index())

        b = FpSemigroupElement(S, "b")
        bbb = FpSemigroupElement(S, "bbb")
        self.assertEqual(b.word_to_class_index(),
                         bbb.word_to_class_index())
        self.assertIsInstance(b.word_to_class_index(), int)
        self.assertNotEqual(b.word_to_class_index(),
                            a.word_to_class_index())

        ab = FpSemigroupElement(S, "ab")
        self.assertNotEqual(ab.word_to_class_index(),
                            b.word_to_class_index())

        T = FpMonoid(["a", "b"],
                     [["aa", "a"], ["bbb", "b"], ["ab", "ba"]])
        e = FpMonoidElement(T, "")
        self.assertIsInstance(e.word_to_class_index(), int)

        a = FpMonoidElement(T, "a")
        aa = FpMonoidElement(T, "aa")
        self.assertEqual(a.word_to_class_index(),
                         aa.word_to_class_index())

        b = FpMonoidElement(T, "b")
        bb = FpMonoidElement(T, "bb")
        self.assertNotEqual(b.word_to_class_index(),
                            bb.word_to_class_index())

    def test_word_to_class_index_int(self):
        A = FpSemigroupElement(FpSemigroup([1, 2], [[[1, 1], [1]], [[2, 2, 2], [2]],
                                    [[1, 2], [2, 1]]]), [1])
        self.assertEqual(A.word_to_class_index(), 0)
        B = FpSemigroupElement(A.semigroup(), [2])
        self.assertEqual(B.word_to_class_index(), 1)
        AB = FpSemigroupElement(A.semigroup(), [1, 2])
        BA = FpSemigroupElement(A.semigroup(), [2, 1])
        self.assertEqual(AB.word_to_class_index(), BA.word_to_class_index())


        ab = FpMonoidElement(FpMonoid([1, 2],
                                      [[[1, 1], [1]],
                                       [[2, 2, 2], [2]],
                                       [[1, 2], [2, 1]]]), [1, 2])
        ba = FpMonoidElement(ab.monoid(), [2, 1])
        self.assertEqual(ab.word_to_class_index(),
                         ba.word_to_class_index())
        A = FpMonoidElement(ab.monoid(), [1])
        AA = FpMonoidElement(ab.monoid(), [1, 1])
        self.assertEqual(A.word_to_class_index(), AA.word_to_class_index())
        B = FpMonoidElement(ab.monoid(), [2])
        BBB = FpMonoidElement(ab.monoid(), [2, 2, 2])
        self.assertEqual(B.word_to_class_index(), BBB.word_to_class_index())

class TestFpMonoid(unittest.TestCase):

    def test_valid_init(self):
        FpMonoid([1, 2], [])
        FpMonoid([1, 2], [[[1], [1, 1]]])
        FpMonoid([1, 2, 3], [[[2], [1, 1]]])
        FpMonoid([1, 2, 3], [[[0], [1, 1]]])

        FpMonoid([], [])
        FpMonoid(["a"], [])
        FpMonoid(["a"], [["a", "aa"]])
        FpMonoid(["a", "b"], [["b", "aa"]])
        FpMonoid(["a", "b"], [["e", "aa"]])

    def test_alphabet_str(self):
        with self.assertRaises(ValueError):
            FpMonoid([], [["a", "aa"]])
        with self.assertRaises(ValueError):
            FpMonoid(["a"], [["b", "aa"]])
        with self.assertRaises(ValueError):
            FpMonoid(["a", "a"], [["b", "aa"]])

    def test_alphabet_int(self):
        with self.assertRaises(ValueError):
            FpMonoid([], [[[1], [2, 2]]])
        with self.assertRaises(TypeError):
            FpMonoid(1, [[[1], [2, 2]]])

    def test_rels_str(self):
        with self.assertRaises(TypeError):
            FpMonoid(["a", "b"], "[\"a\", \"aa\"]")
        with self.assertRaises(TypeError):
            FpMonoid(["a", "b"], ["\"b\", \"aa\""])
        with self.assertRaises(ValueError):
            FpMonoid(["a", "b"], [["a", "aa", "b"]])
        with self.assertRaises(TypeError):
            FpMonoid(["a", "b"], [["b", ["a", "a"]]])
        with self.assertRaises(ValueError):
            FpMonoid(["a", "b"], [["b", "ca"]])

    def test_rels_int(self):
        with self.assertRaises(TypeError):
            FpMonoid([1, 2], "[[1], [2, 2]]")
        with self.assertRaises(TypeError):
            FpMonoid([1, 2], ["[1], [2, 2]"])
        with self.assertRaises(ValueError):
            FpMonoid([1, 2], [[[1], [2, 2], [1]]])
        with self.assertRaises(TypeError):
            FpMonoid([1, 2], [[[1], "2, 2"]])
        with self.assertRaises(TypeError):
            FpMonoid([1, 2], [[["1"], [2, 2]]])
        with self.assertRaises(ValueError):
            FpMonoid([1, 2], [[[1], [3, 2]]])

    def test_set_report_str(self):
        M = FpMonoid(["a"], [["a", "aa"]])
        M.set_report(True)
        M.set_report(False)
        with self.assertRaises(TypeError):
            M.set_report("False")

    def test_set_report_int(self):
        M = FpMonoid([1], [[[1], [1, 1]]])
        M.set_report(True)
        M.set_report(False)
        with self.assertRaises(TypeError):
            M.set_report("False")

    def test_size(self):
        self.assertEqual(FpMonoid(["a"], [["a", "aa"]]).size(), 2)
        self.assertEqual(FpMonoid(["a", "b"], [["a", "aa"], ["b", "bb"],
        ["ab", "ba"]]).size(), 4)
        self.assertEqual(FpMonoid([1], [[[1], [1, 1]]]).size(), 2)
        self.assertEqual(FpMonoid([1, 2], [[[2], [2, 2]], [[1], [1, 1]],
        [[2, 1], [1, 2]]]).size(), 4)

    def test_word_to_class_index_str(self):
        M = FpMonoid(["a", "b"], [["a", "aa"], ["b", "bb"], ["ab", "ba"]])
        a = FpMonoidElement(M, "a")
        aa = FpMonoidElement(M, "aa")
        bb = FpMonoidElement(M, "bb")
        self.assertEqual(a.word_to_class_index(),
                         aa.word_to_class_index())
        self.assertNotEqual(a.word_to_class_index(),
                            bb.word_to_class_index())

        aba = FpMonoidElement(M, "aba")
        self.assertIsInstance(aba.word_to_class_index(), int)

        b = FpMonoidElement(M, "b")
        abaaabb = FpMonoidElement(M, "abaaabb")
        self.assertEqual((a*b*a*a*b*a).word_to_class_index(),
                         abaaabb.word_to_class_index())

    def test_word_to_class_index_int(self):
        M = FpMonoid([1, 2], [[[1], [1, 1]], [[2], [2, 2]], [[1, 2], [2, 1]]])

        a = FpMonoidElement(M, [1])
        aa = FpMonoidElement(M, [1, 1])
        self.assertEqual(a.word_to_class_index(), aa.word_to_class_index())

        a = FpMonoidElement(M, [1])
        bb = FpMonoidElement(M, [2, 2])
        self.assertNotEqual(a.word_to_class_index(), bb.word_to_class_index())

        aba = FpMonoidElement(M, [1, 2, 1])
        self.assertIsInstance(aba.word_to_class_index(), int)

        a = FpMonoidElement(M, [1])
        b = FpMonoidElement(M, [2])
        w = (a * b * a) ** 2
        abaaba = FpMonoidElement(M, [1, 2, 1, 1, 2, 1])
        self.assertEqual(abaaba.word_to_class_index(),
                         w.word_to_class_index())

    def test_repr(self):
        M = FpMonoid([1,2],[[[1,1],[1]],[[2,2,2],[2]], [[1,2],[2,1]]])
        self.assertEqual(M.__repr__(),
                         "<fp monoid with 2 generators and 3 relations>")

        M = FpMonoid(["a", "b"], [["aa", "a"], ["bbb", "ab"], ["ab", "ba"]])
        self.assertEqual(M.__repr__(),
                         "<fp monoid with 2 generators and 3 relations>")

class TestFpMonoidElement(unittest.TestCase):

    def test_valid_init(self):
        FpM = FpMonoid(["a", "b"], [["aa", "a"], ["bbb", "b"], ["ba", "ab"]])
        FpMonoidElement(FpM, "aba")
        FpMonoidElement(FpM, "a")
        FpM = FpMonoid(["m", "o"], [["ooo", "o"]])
        FpMonoidElement(FpM, "moo")
        FpMonoidElement(FpM, "")
        with self.assertRaises(TypeError):
            FpMonoidElement("aba", "aba")
        with self.assertRaises(TypeError):
            FpMonoidElement(FpM, FpM)
        with self.assertRaises(ValueError):
            FpMonoidElement(FpM, "abc")
        with self.assertRaises(ValueError):
            FpMonoidElement(FpM, [])

    def test_valid_init_int(self):
        FpM = FpMonoid([1, 2], [[[1, 1], [1]], [[2, 2, 2], [2]], [[2, 1], [1, 2]]])
        FpMonoidElement(FpM, [1, 2, 1])
        FpMonoidElement(FpM, [1])
        FpMonoidElement(FpM, [])
        with self.assertRaises(TypeError):
            FpMonoidElement([1, 2, 1], [1, 2, 1])
        with self.assertRaises(TypeError):
            FpMonoidElement(FpM, FpM)
        with self.assertRaises(ValueError):
            FpMonoidElement(FpM, [1, 2, 3])
        with self.assertRaises(ValueError):
            FpMonoidElement(FpM, "")

    def test_mul(self):
        M = FpMonoid(["a", "b"], [["aa", "a"], ["bbb", "b"], ["ba", "ab"]])

        string = "aa"
        aba = FpMonoidElement(M, "aba")
        with self.assertRaises(TypeError):
            aba * string
        with self.assertRaises(TypeError):
            MM = FpMonoid(["a", "b"], [])
            aba = FpMonoidElement(MM, "aba") * aba

        aba = FpMonoidElement(M, "aba")
        abaaba = FpMonoidElement(M, "abaaba")
        self.assertEqual((aba * aba).word_to_class_index(),
                         abaaba.word_to_class_index())

        e = FpMonoidElement(M, "")
        self.assertEqual((aba * e).word_to_class_index(),
                         aba.word_to_class_index())

    def test_mul_int(self):
        FpM = FpMonoid([1, 2], [[[1, 1], [1]], [[2, 2, 2], [2]], [[2, 1], [1, 2]]])
        other = [1, 1]
        a = FpMonoidElement(FpM, [1, 2, 1])
        e = FpMonoidElement(FpM, [])
        with self.assertRaises(TypeError):
            a * other
        with self.assertRaises(TypeError):
            FpMonoidElement(FpMonoid([1, 2], []), [1, 2, 1])*a
        self.assertEqual((a*a).word_to_class_index(),
            FpMonoidElement(FpM, [1, 2, 1, 1, 2, 1]).word_to_class_index())
        self.assertEqual((a*e).word_to_class_index(), a.word_to_class_index())

if __name__ == "__main__":
    unittest.main()
