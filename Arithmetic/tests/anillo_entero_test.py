import unittest

from Arithmetic.anillo_entero import AnilloEntero


class CheckBadInputs(unittest.TestCase):
    def test_string(self):
        self.assertRaises(TypeError, AnilloEntero, "Tonto")

    def test_float(self):
        self.assertRaises(TypeError, AnilloEntero, 10.2)

    def test_negative(self):
        self.assertRaises(ValueError, AnilloEntero, -24)

    def test_zero(self):
        self.assertRaises(ValueError, AnilloEntero, 0)

    def test_anillo(self):
        A = AnilloEntero(10)
        self.assertRaises(TypeError, AnilloEntero, A)


class CheckGoodInputs(unittest.TestCase):
    def test_int(self):
        A = AnilloEntero(10)
        self.assertEqual(A._m, 10)


class CheckGoodElementInput(unittest.TestCase):
    def setUp(self):
        self.A = AnilloEntero(10)

    def test_int(self):
        self.assertEqual(self.A(1)._valor, 1)
        self.assertEqual(self.A(11)._valor, 1)
        self.assertEqual(self.A(21)._valor, 1)

    def test_negative(self):
        self.assertEqual(self.A(-1)._valor, 9)
        self.assertEqual(self.A(-9)._valor, 1)

    def test_element_same_ring(self):
        a = self.A(21)
        self.assertEqual(self.A(a)._valor, 1)

    def test_element_other_ring(self):
        B = AnilloEntero(45)
        b = B(23)

        # 23 % 45 = 23
        self.assertEqual(b._valor, 23)

        # 23 % 10 = 3
        self.assertEqual(self.A(b)._valor, 3)


class CheckBadElementInputs(unittest.TestCase):
    def setUp(self):
        self.A = AnilloEntero(10)

    def test_string(self):
        self.assertRaises(TypeError, self.A.__call__, "Tonto")

    def test_float(self):
        self.assertRaises(TypeError, self.A.__call__, 10.2)


class CheckArithmetic(unittest.TestCase):
    def setUp(self):
        A = AnilloEntero(10)
        self.a = A(3)
        self.b = A(7)
        self.c = A(35)  # 5

    def test_add_int(self):
        self.assertEqual((self.a + 7)._valor, 0)
        self.assertEqual((self.a + 35)._valor, 8)

    def test_add_element_same_ring(self):
        self.assertEqual((self.a + self.b)._valor, 0)
        self.assertEqual((self.a + self.c)._valor, 8)

    def test_sub_int(self):
        self.assertEqual((self.a - 7)._valor, 6)
        self.assertEqual((self.a - 35)._valor, 8)

    def test_sub_element_same_ring(self):
        self.assertEqual((self.a - self.b)._valor, 6)
        self.assertEqual((self.a - self.c)._valor, 8)

    def test_mul_int(self):
        self.assertEqual((self.a * 7)._valor, 1)
        self.assertEqual((self.a * 35)._valor, 5)

    def test_mul_element_same_ring(self):
        self.assertEqual((self.a * self.b)._valor, 1)
        self.assertEqual((self.a * self.c)._valor, 5)

    def test_pow_int(self):
        self.assertEqual((self.a ** 7)._valor, 7)
        self.assertEqual((self.a ** 16)._valor, 1)
        self.assertEqual((self.a ** 21)._valor, 3)
        self.assertEqual((self.a ** 35)._valor, 7)

    def test_div_int(self):
        self.assertEqual((self.a / 7)._valor, 9)
        self.assertEqual((self.a / 9)._valor, 7)

    def test_div_element(self):
        d = self.a._anillo(9)

        self.assertEqual((self.a / self.b)._valor, 9)
        self.assertEqual((self.a / d)._valor, 7)

    def test_inv(self):
        m = self.a._anillo._m
        a = self.a._valor
        menos_a = (- self.a)._valor

        self.assertEqual(menos_a, m - a)


class CheckBadArithmeticInputs(unittest.TestCase):
    def setUp(self):
        A = AnilloEntero(10)
        B = AnilloEntero(35)
        self.a = A(3)
        self.b = B(17)

    def test_float(self):
        self.assertRaises(TypeError, self.a._extract_value, 10.2)

    def test_string(self):
        self.assertRaises(TypeError, self.a._extract_value, "Hello")

    def test_other_ring(self):
        self.assertRaises(TypeError, self.a._extract_value, self.b)

    def test_pow_element(self):
        self.assertRaises(TypeError, self.a.__pow__, self.b)
        self.assertRaises(ValueError, self.a.__pow__, -10)

    def test_div_int(self):
        self.assertRaises(ValueError, self.a.__truediv__, 35)

    def test_div_element(self):
        self.assertRaises(ValueError, self.a.__truediv__, self.a._anillo(35))


if __name__ == "__main__":
    unittest.main()
