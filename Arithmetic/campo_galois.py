from Arithmetic.teoria_numeros import algoritmo_euclides_extendido


class CampoGalois:

    """
    No se ha programado que un campo interactue con otro campo, por favor no se ponga ingenioso.
    """

    def __init__(self, p) -> None:
        self.p = p

    def __str__(self):
        desc = "Z_{0}".format(self.p)
        return desc

    def __call__(self, valor):
        return self.__FieldElement(self, valor)

    class __FieldElement:
        def __init__(self, campo, valor) -> None:
            self.campo = campo
            self.valor = valor % campo.p

        def __add__(self, other):
            if type(other) == type(self):
                return self.campo((self.valor + other.valor) % self.campo.p)

            return self.campo((self.valor + other) % self.campo.p)

        def __sub__(self, other):
            if type(other) == type(self):
                return self.campo((self.valor - other.valor) % self.campo.p)

            return self.campo((self.valor - other) % self.campo.p)

        def __mul__(self, other):
            if type(other) == type(self):
                return self.campo((self.valor * other.valor) % self.campo.p)

            return self.campo((self.valor * other) % self.campo.p)

        def __truediv__(self, other):
            if type(other) == type(self):
                (_, _, inv_other) = algoritmo_euclides_extendido(
                    other.campo.p, other.valor
                )
                return self.campo((self.valor * inv_other) % self.campo.p)

            (_, _, inv_other) = algoritmo_euclides_extendido(
                self.campo.p, other)
            return self.campo((self.valor * inv_other) % self.campo.p)

        def __pow__(self, other):
            if type(other) == type(self):
                return self.campo((self.valor ** other.valor) % self.campo.p)

            return self.campo((self.valor ** other) % self.campo.p)

        def __neg__(self):
            return self.campo((- self.valor) % self.campo.p)

        def __str__(self):
            desc = "{0} in Z_{1}".format(self.valor, self.campo.p)
            return desc

        def __eq__(self, other):
            return self.valor == other.valor

        def __neq__(self, other):
            return self.valor != other.valor


if __name__ == "__main__":
    GF = CampoGalois(11)
    print(GF)

    A = GF(15)
    print(A)
    B = GF(12)
    print(B)

    N_mult = GF(1)

    N_add = GF(0)

    #print("A^-1: {0}".format(Neutro_mult / A))

    print("A+1: {0}".format(A+1))
    print("B: {0}".format(B))
    print("A + B: {0}".format(A + B))
    print("A - B: {0}".format(A - B))
    print("A / B: {0}".format(A / B))
    print("B / A: {0}".format(B / A))
