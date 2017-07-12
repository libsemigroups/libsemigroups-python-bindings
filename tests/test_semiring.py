import unittest
import sys
import os
from semigroups import (SemiringABC, Integers, MaxPlusSemiring,
                        MinPlusSemiring)

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

class TestIntegers(unittest.TestCase):
    def test_init(self):
        self.assertEqual(Integers().__init__(), None)

        with self.assertRaises(TypeError):
            Integers(10)

    def test_plus(self):
        self.assertEqual(Integers().plus(7, 3), 10)
        self.assertEqual(Integers().plus(-2000, 5), -1995)
        self.assertEqual(Integers().plus(0, 20), 20)

        with self.assertRaises(TypeError):
            Integers().plus(10)
        with self.assertRaises(TypeError):
            Integers().plus(10.0, 1)
        with self.assertRaises(TypeError):
            Integers().plus(0, '2')
        with self.assertRaises(TypeError):
            Integers().prod(0, -float('inf'))

    def test_prod(self):
        self.assertEqual(Integers().prod(7, 3), 21)
        self.assertEqual(Integers().prod(-2000, 5), -10000)
        self.assertEqual(Integers().prod(0, 20), 0)

        with self.assertRaises(TypeError):
            Integers().prod(10)
        with self.assertRaises(TypeError):
            Integers().prod(10.0, 1)
        with self.assertRaises(TypeError):
            Integers().prod(0, '2')
        with self.assertRaises(TypeError):
            Integers().prod(0, float('inf'))

    def test_zero(self):
        self.assertEqual(Integers().zero(), 0)

        with self.assertRaises(TypeError):
            Integers().zero(26)

    def test_one(self):
        self.assertEqual(Integers().one(), 1)

        with self.assertRaises(TypeError):
            Integers().one(26)

class TestMaxPlusSemiring(unittest.TestCase):
    def test_init(self):
        MaxPlusSemiring()

        with self.assertRaises(TypeError):
            MaxPlusSemiring(10)

    def test_plus(self):
        self.assertEqual(MaxPlusSemiring().plus(7, 3), 7)
        self.assertEqual(MaxPlusSemiring().plus(-2000, 5), 5)
        self.assertEqual(MaxPlusSemiring().plus(0, 20), 20)
        self.assertEqual(MaxPlusSemiring().plus(-float('inf'), 20), 20)

        with self.assertRaises(TypeError):
            MaxPlusSemiring().plus(10)
        with self.assertRaises(TypeError):
            MaxPlusSemiring().plus(10.0, 1)
        with self.assertRaises(TypeError):
            MaxPlusSemiring().plus(0, '2')
        with self.assertRaises(TypeError):
            MaxPlusSemiring().plus(0, float('inf'))

    def test_prod(self):
        self.assertEqual(MaxPlusSemiring().prod(7, 3), 10)
        self.assertEqual(MaxPlusSemiring().prod(-2000, 5), -1995)
        self.assertEqual(MaxPlusSemiring().prod(0, 20), 20)
        self.assertEqual(MaxPlusSemiring().prod(-float('inf'), 20),
                         -float('inf'))

        with self.assertRaises(TypeError):
            MaxPlusSemiring().prod(10)
        with self.assertRaises(TypeError):
            MaxPlusSemiring().prod(10.0, 1)
        with self.assertRaises(TypeError):
            MaxPlusSemiring().prod(0, '2')
        with self.assertRaises(TypeError):
            MaxPlusSemiring().prod(0, float('inf'))

    def test_zero(self):
        self.assertEqual(MaxPlusSemiring().zero(), -float('inf'))

        with self.assertRaises(TypeError):
            MaxPlusSemiring().zero(26)

    def test_one(self):
        self.assertEqual(MaxPlusSemiring().one(), 0)

        with self.assertRaises(TypeError):
            MaxPlusSemiring().one(26)

class TestMinPlusSemiring(unittest.TestCase):
    def test_init(self):
        MinPlusSemiring()

        with self.assertRaises(TypeError):
            MinPlusSemiring(10)

    def test_plus(self):
        self.assertEqual(MinPlusSemiring().plus(7, 3), 3)
        self.assertEqual(MinPlusSemiring().plus(-2000, 5), -2000)
        self.assertEqual(MinPlusSemiring().plus(0, 20), 0)
        self.assertEqual(MinPlusSemiring().plus(float('inf'), 20), 20)

        with self.assertRaises(TypeError):
            MinPlusSemiring().plus(10)
        with self.assertRaises(TypeError):
            MinPlusSemiring().plus(10.0, 1)
        with self.assertRaises(TypeError):
            MinPlusSemiring().plus(0, '2')
        with self.assertRaises(TypeError):
            MinPlusSemiring().plus(0, -float('inf'))

    def test_prod(self):
        self.assertEqual(MinPlusSemiring().prod(7, 3), 10)
        self.assertEqual(MinPlusSemiring().prod(-2000, 5), -1995)
        self.assertEqual(MinPlusSemiring().prod(0, 20), 20)
        self.assertEqual(MinPlusSemiring().prod(float('inf'), 20),
                         float('inf'))

        with self.assertRaises(TypeError):
            MinPlusSemiring().prod(10)
        with self.assertRaises(TypeError):
            MinPlusSemiring().prod(10.0, 1)
        with self.assertRaises(TypeError):
            MinPlusSemiring().prod(0, '2')
        with self.assertRaises(TypeError):
            MinPlusSemiring().prod(0, -float('inf'))

    def test_zero(self):
        self.assertEqual(MinPlusSemiring().zero(), float('inf'))

        with self.assertRaises(TypeError):
            MinPlusSemiring().zero(26)

    def test_one(self):
        self.assertEqual(MinPlusSemiring().one(), 0)

        with self.assertRaises(TypeError):
            MinPlusSemiring().one(26)

if __name__ == '__main__':
    unittest.main()
