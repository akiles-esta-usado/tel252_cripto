from math import gcd
from eulerlib import Divisors
from Arithmetic.teoria_numeros import algoritmo_euclides_extendido


class GrupoFinitoCiclico:
    def __init__(self, p, elements=[], deep=0):
        self.p = p
        self.deep = deep
        #print(deep*"  " + "Caso p={0}, elements={1}".format(p, elements))

        self.__set_elements(elements)
        #print(deep*"  " + "G: {0}".format(self.G))

        self.__set_alphas()
        #print(deep*"  " + "alfas: {0}".format(self.alphas))

        self.__set_subgroups_new()

    def __set_alphas(self):
        self.alphas = []

        for a in self.G:

            # print(self.deep* "  " + "__set_alphas: {0}, orden={1}, cardinalidad={2}"
            #      .format(
            #          a,
            #          self.ord(a),
            #          self.cardinalidad)
            #      )
            if self.ord(a) == self.cardinalidad:
                self.alphas.append(a)

    def __set_elements(self, elements=[]):
        if len(elements) == 0:
            self.G = []

            for i in range(1, self.p):
                if (gcd(i, self.p) == 1):
                    self.G.append(i)

        else:
            self.G = elements

        self.cardinalidad = len(self.G)

    def __set_subgroups_new(self):
        # Los subgrupos no tienen subgrupos por ahora
        if self.deep != 0:
            return

        H = []

        factors = Divisors().divisors(self.cardinalidad)

        mapping = dict()

        for i in range(0, len(factors)):
            q = factors[i]
            mapping[q] = i
            H.append({1})

        for a in self.G:
            orden = self.ord(a)
            index = mapping[orden]

            if len(H[index]) == 1:
                H[index] = sorted(self.get_cycle(a))

        self.H = []

        for i in range(0, len(H)):
            q = factors[i]

            Z = GrupoFinitoCiclico(
                p=self.p, elements=list(H[i]), deep=self.deep + 1
            )

            # print(Z) ## Ojo con esto
            # pass

            self.H.append(Z)

    def __str__(self):
        if self.deep == 0:
            description = "Grupo Z*{0}\n".format(self.p)

        else:
            description = self.deep * "  " + \
                "Subgrupo H{0}\n".format(self.cardinalidad)

        description += self.deep * "  " + \
            "* cardinalidad: {0}\n".format(self.cardinalidad)
        description += self.deep * "  " + "* elementos: {0}\n".format(self.G)
        description += self.deep * "  " + "* alphas: {0}\n".format(self.alphas)

        # Por ahora los subgrupos no contienen subgrupos.
        if self.deep == 0:
            counter = 0
            for subgroup in self.H:
                description += subgroup.__str__() + "\n"

        return description

    def __getitem__(self, index):
        return self.G[index]

    def exp(self, a, x):
        return a**x % self.p

    def mult(self, a, b):
        # print(self.deep*"  " + "  mult: a={0}, b={1}, res={2}".format(
        #    a,
        #    b,
        #    a*b % self.p
        # ))
        return a*b % self.p

    def ord(self, a):
        if a not in self.G:
            print("Error, {0} not in G".format(a))
            return

        order = 1
        last = a
        while (last != 1):
            order += 1
            last = self.mult(last, a)

        return order

    def get_cycle(self, a):
        if a not in self.G:
            print("Error, {0} not in G".format(a))
            return

        cycle = [a]

        while(cycle[-1] != 1):
            cycle.append(self.mult(cycle[-1], a))

        return cycle

    def __call__(self, valor):
        return self._Element(grupo=self, valor=valor)

    class _Element:
        def __init__(self, grupo, valor):
            self.grupo = grupo
            self.valor = valor % grupo.p

        def __pow__(self, other):
            if type(other) == type(self):
                return self.grupo((self.valor ** other.valor) % self.grupo.p)

            elif type(other) == int:
                return self.grupo((self.valor ** other) % self.grupo.p)

            raise TypeError("Solo se admiten enteros y elementos de grupo")

        def __mul__(self, other):
            if type(other) == type(self):
                return self.grupo((self.valor * other.valor) % self.grupo.p)

            elif type(other) == int:
                return self.grupo((self.valor * other) % self.grupo.p)

            raise TypeError("Solo se admiten enteros y elementos de grupo")

        def __add__(self, other):
            if type(other) == type(self):
                return self.grupo((self.valor + other.valor) % self.grupo.p)

            elif type(other) == int:
                return self.grupo((self.valor + other) % self.grupo.p)

            raise TypeError("Solo se admiten enteros y elementos de grupo")

        def __sub__(self, other):
            if type(other) == type(self):
                return self.grupo((self.valor - other.valor) % self.grupo.p)

            elif type(other) == int:
                return self.grupo((self.valor - other) % self.grupo.p)

            raise TypeError("Solo se admiten enteros y elementos de grupo")

        def __truediv__(self, other):
            if type(other) == type(self):
                (_, _, inv_other) = algoritmo_euclides_extendido(
                    other.grupo.p, other.valor
                )
                return self.grupo((self.valor * inv_other) % self.grupo.p)

            elif type(other) == int:
                (_, _, inv_other) = algoritmo_euclides_extendido(
                    self.grupo.p, other)
                return self.grupo((self.valor * inv_other) % self.grupo.p)

            raise TypeError("Solo se admiten enteros y elementos de grupo")

        def __str__(self):
            desc = "{0} in Z_{1}".format(self.valor, self.grupo.p)
            return desc

        def __ge__(self, other):
            if (type(other) == type(self)):
                return self.valor >= other.valor

            elif ((type(other) == int) or (type(other) == float)):
                return self.valor >= other

            raise TypeError("Solo se admiten enteros y elementos de grupo")

        def __lt__(self, other):
            if (type(other) == type(self)):
                return self.valor < other.valor

            elif ((type(other) == int) or (type(other) == float)):
                return self.valor < other

            raise TypeError("Solo se admiten enteros y elementos de grupo")

        def __eq__(self, other):
            if (type(other) == type(self)):
                return self.valor == other.valor

            elif ((type(other) == int) or (type(other) == float)):
                return self.valor == other

            raise TypeError("Solo se admiten enteros y elementos de grupo")


if __name__ == "__main__":
    G = GrupoFinitoCiclico(17)

    print(G)

    # for elem in G:
    #     print("{0}: orden={1}, arreglo:{2}".format(
    #         elem, G.ord(elem), G.get_cycle(elem)))

    #print("Orden de 7 es {0}".format(G.ord(7)))
