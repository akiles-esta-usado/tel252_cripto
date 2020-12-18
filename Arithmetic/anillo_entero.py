from Arithmetic.teoria_numeros import algoritmo_euclides_extendido


class AnilloEntero:
    def __init__(self, m):
        if (type(m) != int):
            raise TypeError("m debe ser un entero")

        if (m <= 0):
            raise ValueError("m debe ser positivo entero")

        self._m = m

    def __call__(self, valor):
        return self._Element(anillo=self, valor=valor)

    def __str__(self):
        return "Z_{0}".format(self._m)

    class _Element:

        def __init__(self, anillo, valor):
            if (type(anillo) != AnilloEntero):
                raise TypeError("anillo debe ser de tipo AnilloEntero")

            if (type(valor) == int):
                self._anillo = anillo
                self._valor = valor % anillo._m

            elif (type(valor) == AnilloEntero._Element):
                self._anillo = anillo
                self._valor = valor._valor % anillo._m

            else:
                raise TypeError("valor debe ser entero")

        def __add__(self, other):
            res = self._anillo(self._valor + self._extract_value(other))
            return res

        def __sub__(self, other):
            res = self._anillo(self._valor - self._extract_value(other))
            return res

        def __mul__(self, other):
            res = self._anillo(self._valor * self._extract_value(other))
            return res

        def __pow__(self, exp):
            if (type(exp) != int):
                raise TypeError("exponente debe ser un entero")

            elif (exp < 0):
                raise ValueError("exponente debe ser positivo o cero")

            elif (exp == 0):
                return self._anillo(1)

            res = self._valor
            binary = "{0:b}".format(exp)

            for char in binary[1:]:
                print(res)
                res *= res

                if (char == "1"):
                    res *= self._valor

            return self._anillo(res)

        def __truediv__(self, other):
            val = self._extract_value(other)

            gcd, _, inv_val = algoritmo_euclides_extendido(
                self._anillo._m, val)

            if (gcd == 1):
                inv_val %= self._anillo._m
                return self._anillo(self._valor * inv_val)

            else:
                raise ValueError(
                    "divisor {0} no invertible en el anillo {1}".format(val, self._anillo._m))

        def _extract_value(self, other):
            if (type(other) == int):
                return other

            elif ((type(other) == AnilloEntero._Element) and
                  (self._anillo._m == other._anillo._m)):
                return other._valor

            else:
                raise TypeError(
                    "Otro operando debe ser un elemento del anillo o un entero"
                )

        def __neg__(self):
            return self._anillo(self._anillo._m - self._valor)

        def __eq__(self, other):
            return self._valor == self._extract_value(other)

        def __neq__(self, other):
            return self._valor != self._extract_value(other)

        def __str__(self):
            return "{0} in Z_{1}".format(self._valor, self._anillo._m)
