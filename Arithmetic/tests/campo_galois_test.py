import unittest

from Arithmetic.campo_galois import CampoGalois


class TestCampoGalois(unittest.TestCase):

    def test_creation(self):
        A = CampoGalois(15)
        B = CampoGalois(20)

        self.assertEqual(A.p, 15)
        self.assertEqual(B.p, 20)

    def test_operatoria(self):
        A = CampoGalois(15)

        val1 = A(10) + A(20)
        val2 = A(10) + A(21)
        val3 = (A(7) * A(4)) / A(7)

        self.assertEqual(val1.valor, 0)
        self.assertEqual(val2.valor, 1)
        self.assertEqual(val3.valor, 4)
