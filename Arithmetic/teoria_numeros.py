from math import gcd


def algoritmo_euclides_extendido(r0, r1):
    """
    Entrada: r0, r1
    Retorno: (g, s, t)

    Relación:
        gcd(r0, r1) = s*r_0 + t*r_1

    con 'g' el máximo común divisor entre r0 y r1.

    IMPORTANTE los valores de los inversos pueden ser negativos, se recomienda
    aplicar la operación módulo después de ocupar.
    """
    if r0 == 0:
        return (r1, 0, 1)
    else:
        g, s, t = algoritmo_euclides_extendido(r1 % r0, r0)
        return (g, t - (r1 // r0) * s, s)
