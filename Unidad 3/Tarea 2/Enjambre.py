import random

class Particula:
    def crear(self, dimensiones, limites):
        self.posicion_actual = [random.uniform(limites[0], limites[1]) for _ in range(dimensiones)]
        self.velocidad = None
        self.valor_actual = None  
        self.mejor_valor = None
        self.mejor_posicion = self.posicion_actual[:]

    def mostrar(self):
        print(f"Posición: {self.posicion_actual}")


class Enjambre:
    def crear(self, num_particulas, dimensiones, limites):
        self.particulas = []
        self.mejor_posicion_global = None
        self.mejor_valor_global = None
        self.limites = limites

        for _ in range(num_particulas):
            p = Particula()
            p.crear(dimensiones, limites)
            self.particulas.append(p)

    def mostrar_particulas(self):
        for i, p in enumerate(self.particulas):
            print(f"Partícula {i+1}:")
            p.mostrar()


enjambre = Enjambre()
enjambre.crear(num_particulas=5, dimensiones=2, limites=(-10, 10))
enjambre.mostrar_particulas()