import unittest

from Arithmetic.curva_eliptica import CurvaEliptica


class TestCurvaEliptica(unittest.TestCase):

    def test_correct_construction(self):

        EC17 = CurvaEliptica(p=17, a=2, b=2)
        EC11 = CurvaEliptica(p=11, a=-18, b=27)

        self.assertEqual(EC17.p, 17)
        self.assertEqual(EC17.a, 2)
        self.assertEqual(EC17.b, 2)

        self.assertEqual(EC11.p, 11)
        self.assertEqual(EC11.a, -18)
        self.assertEqual(EC11.b, 27)

    def test_bad_construction(self):
        self.assertRaises(ValueError, CurvaEliptica, 3, -18, 27)
        self.assertRaises(ValueError, CurvaEliptica, 5, -18, 27)

    def test_isValid(self):
        EC17 = CurvaEliptica(p=17, a=2, b=2)

        pares = [
            [5, 1],
            [6, 3],
            [10, 6],
            [3, 1],
            [9, 16],
            [16, 13],
            [0, 6]
        ]

        for par in pares:
            self.assertEqual(EC17.isValid(par[0], par[1]), True)

    def test_addition(self):
        EC = CurvaEliptica(p=17, a=2, b=2)

        P = EC(5, 1)

        self.assertEqual(P.x.valor, 5)
        self.assertEqual(P.y.valor, 1)

        R = EC.add(P, P)

        self.assertEqual(R.x.valor, 6)
        self.assertEqual(R.y.valor, 3)

        Z = EC.add(P, R)

        self.assertEqual(Z.x.valor, 10)
        self.assertEqual(Z.y.valor, 6)

    def test_negatin(self):
        EC = CurvaEliptica(p=17, a=2, b=2)

        P = EC(5, 1)

        R = -P

        self.assertEqual(R.x.valor, 5)
        self.assertEqual(R.y.valor, 16)
