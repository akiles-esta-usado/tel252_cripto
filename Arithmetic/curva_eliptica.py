from Arithmetic.campo_galois import CampoGalois


class CurvaEliptica:

    def __init__(self, p, a, b):
        self.p = p
        self.a = a
        self.b = b

        self.campo = CampoGalois(p)

        self.__verify_ab()

    def __str__(self):
        desc = "EC{0}:\n".format(self.p)
        desc += "  (a, b, p) = ({0}, {1}, {2})\n".format(self.a,
                                                         self.b,
                                                         self.p)
        desc += "  y**2 = x**3 + {0}x + {1} mod {2}".format(
            self.a, self.b, self.p)

        return desc

    def __verify_ab(self):
        discriminant = 4 * self.a**3 + 27 * self.b**2
        discriminant %= self.p

        if discriminant == 0:
            raise ValueError(
                "'a' y 'b' no cumplen el criterio del discriminante.")

        else:
            return discriminant

    def isValid(self, x, y):
        if (y**2 % self.p) == (x**3 + self.a * x + self.b) % self.p:
            return True

        return False

    def add(self, P, R):

        if (type(P) != CurvaEliptica.__Element) | (type(R) != CurvaEliptica.__Element):
            raise ValueError("P o R no son objetos de la curva")

        GF = self.campo

        x1, y1 = P.x, P.y
        x2, y2 = R.x, R.y

        #print("\nadd: x1, y1 = {0}, {1}".format(x1, y1))

        # Point Doubling
        if (R == P):
            #print("\nadd: x2, y2 = {0}, {1}".format(x2, y2))

            s = (x1**2 * 3 + self.a) / (y1 * 2)

            #print("add: s = {0}, type: {1}".format(s, type(s)))

        # Point Adding
        else:
            #print("\add: x2, y2 = {0}, {1}".format(x2, y2))
            s = (y2 - y1) / (x2 - x1)

        #print("add: s**2 = ", s**2)

        x3 = s**2 - x1 - x2
        #print("add: x1, x2, x3 = {0}, {1}".format(x1, x2, x3))

        y3 = (x1 - x3) * s - y1

        return self(x3.valor, y3.valor)

    def __call__(self, x, y):
        return self.__Element(self, x, y)

    class __Element:
        def __init__(self, ec, x, y):
            self.ec = ec
            self.x = ec.campo(x)
            self.y = ec.campo(y)

        def __eq__(self, other):

            return ((self.x.valor == other.x.valor) &
                    (self.y.valor == other.y.valor) &
                    (self.ec.p == other.ec.p))
            pass

        def __add__(self, other):
            # Me habría gustado poner la suma acá, pero el tiempo no da para eso.
            pass

        def __str__(self):
            desc = "({0}, {1}) in Z{2}".format(
                self.x.valor, self.y.valor, self.ec.campo.p
            )

            return desc

        def __neg__(self):
            return self.ec(
                self.x.valor,
                self.ec.campo.p - self.y.valor
            )

        # Esta es la operación de la tarea.
        def __mul__(self, integer):
            if type(integer) != int:
                raise TypeError("El par debe multiplicarse por un entero.")

            if integer <= 0:
                raise ValueError("No se puede multiplicar por un negativo o 0")

            binary = "{0:b}".format(integer)

            R = self.ec(self.x.valor, self.y.valor)  # Es necesaria una copia

            # print(binary)

            for char in binary[1:]:
                # print(char)
                R = self.ec.add(R, R)

                if char == '1':
                    R = self.ec.add(R, self)

            return R


if __name__ == "__main__":

    EC17 = CurvaEliptica(p=17, a=2, b=2)
    print(EC17)

    P = EC17(5, 1)
    R = EC17.add(P, P)
    Z = EC17.add(P, R)

    print("P: {0}".format(P))
    print("R = 2P: {0}".format(R))
    print("Z = R+Z: {0}".format(Z))
    print("-P: {0}".format(-P))

    # Tarea 10

    for i in range(1, 30):
        print(i, P*i)

    # Lista la tarea 10, no supe como marcar el elemento neutro O, que corresponde a (7,1)
