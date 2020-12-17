from Arithmetic.grupo_finito_ciclico import GrupoFinitoCiclico

from Labs.lab9 import rho

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
