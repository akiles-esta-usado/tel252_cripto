from Arithmetic.grupo_finito_ciclico import GrupoFinitoCiclico

# Actividad:

# La idea básica del método Pollard's Rho es generar de manera pseudoaleatoria
# un grupo de elementos de la forma $a^i*B^j$.

# Los valores $i$ y $j$ son registrados para verificar una eventual colisión.

# En la práctica, Pollard's Rho es un algoritmo que realiza el cómputo de
# logaritmos discretos en $Z^*_p$.

# Considere el siguiente pseudocódigo y proponga una solución.

# Describa eventuales supuestos de su prototipo.

# Ref.:http://web.cse.msstate.edu/~ramkumar/pollard.pdf


class rho:
    """
    G: grupo cíclico de tipo GrupoFinitoCiclico
    g: generador de G
    h: elemento de G, g^x = h
    """

    def __init__(self, G, g):
        self.G = G
        self.R = GrupoFinitoCiclico(G.ord(g.valor))

        if(type(g) == GrupoFinitoCiclico._Element):
            self.g = g

        else:
            self.g = G(g)

    def solve(self, h):
        if(type(h) == GrupoFinitoCiclico._Element):
            self.h = h
        else:
            self.h = self.G(h)

        x_i = self.G(1)
        a_i = self.G(0)
        b_i = self.G(0)

        x_2i = self.G(1)
        a_2i = self.G(0)
        b_2i = self.G(0)

        for _ in range(self.G.p):
            x_i, a_i, b_i = self.__walk(x_i, a_i, b_i)

            x_2i, a_2i, b_2i = self.__walk(x_2i, a_2i, b_2i)
            x_2i, a_2i, b_2i = self.__walk(x_2i, a_2i, b_2i)

            if (x_i == x_2i):
                break

        u = self.R((a_2i - a_i).valor)
        v = self.R((b_i - b_2i).valor)

        print("R.p: {0}".format(self.R.p))
        print("u: {0}".format(u))
        print("v: {0}".format(v))

        return u/v

    def __walk(self, x, a, b):
        """
        Retorna: x_i+1, a_i+1, b_i+1
        """
        tercio = self.G.p/3

        if (x >= 0) & (x < tercio):
            return self.h*x, a, b+1

        elif (x >= tercio) & (x < 2*tercio):
            return x**2, a*2, b*2

        else:
            return self.g*x, a+1, b


if __name__ == "__main__":

    # Ocuparemos el ejemplo 8.1 del libro
    G = GrupoFinitoCiclico(29)
    alpha = G(2)

    # Alice
    a = G(5)
    A = alpha**a

    # Bob
    b = G(12)
    B = alpha**b

    print("Estado inicial:")
    print("Alice:")
    print("  a: {0}".format(a))
    print("  A: {0}".format(A))
    print("  k_AB = {0}".format(A**b))

    print("Bob:")
    print("  b: {0}".format(b))
    print("  B: {0}".format(B))
    print("  k_BA = {0}".format(B**a))

    Breaker = rho(G, alpha)

    K_pr_alice = Breaker.solve(A)
    K_pr_bob = Breaker.solve(B)

    print("Luego de romper las claves:")
    print("- a obtenido: {0}".format(K_pr_alice))
    print("- b obtenido: {0}".format(K_pr_bob))
