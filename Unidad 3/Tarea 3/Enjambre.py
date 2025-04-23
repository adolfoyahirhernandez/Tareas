import random

class Particula:
    def crear(self, dimensiones, limites):
        self.posicion_actual = [random.uniform(limites[0], limites[1]) for _ in range(dimensiones)]
        self.velocidad = [0 for _ in range(dimensiones)]
        self.valor_actual = None  
        self.mejor_valor = None
        self.mejor_posicion = self.posicion_actual[:]

    def mostrar(self):
        print(f"Posición: {self.posicion_actual}")
    
    def mover_particula(self,limites, mejor_posicion_global):
        nueva_posicion =[]
        nueva_velocidad =[]
        w=1
        c1=2
        c2=2

        r1=random.random()
        r2=random.random()

        for i in range(len(self.posicion_actual)):

            inercia = w * self.velocidad[i]
            cognitivo = c1 * r1 * (self.mejor_posicion[i] - self.posicion_actual[i])
            social = c2 * r2 * (mejor_posicion_global[i] - self.posicion_actual[i])

            v = inercia + cognitivo + social
            nueva_velocidad.append(v)

            p = self.posicion_actual[i] + v

            if p < limites[0]:
                p = limites[0]
            elif p > limites[1]:
                p = limites[1]
            
            nueva_posicion.append(p)
        
        self.velocidad = nueva_velocidad
        self.posicion_actual = nueva_posicion

    def evaluar_particula(self, orden):
        self.valor_actual = sum(x**2 for x in self.posicion_actual)

        if (self.mejor_valor is None):
            self.mejor_valor = self.valor_actual
            self.mejor_posicion = self.posicion_actual[:]
        elif (orden == 0):
            if (self.valor_actual < self.mejor_valor):
                self.mejor_valor = self.valor_actual
                self.mejor_posicion =self.posicion_actual[:]
        else:
            if (self.valor_actual > self.mejor_valor):
                self.mejor_valor = self.valor_actual
                self.mejor_posicion =self.posicion_actual[:]

        

       
class Enjambre:
    def crear(self, num_particulas, dimensiones, limites):
        self.particulas = []
        self.mejor_posicion_global = None
        self.mejor_valor_global = None
        self.limites = limites
        self.orden = 0

        for _ in range(num_particulas):
            p = Particula()
            p.crear(dimensiones, limites)
            self.particulas.append(p)

    def mostrar_particulas(self):
        for i, p in enumerate(self.particulas):
            print(f"Partícula {i+1}:")
            p.mostrar()
    
    def mover_enjambre(self):
        for p in self.particulas:
            p.mover_particula(self.limites, self.mejor_posicion_global)

    def evaluar_enjambre(self):
        for p in self.particulas:
            p.evaluar_particula(self.orden)
            if (self.mejor_valor_global is None):
                self.mejor_valor_global = p.valor_actual
                self.mejor_posicion_global =p.posicion_actual[:]
            elif (self.orden == 0):
                if (p.valor_actual < self.mejor_valor_global):
                    self.mejor_valor_global = p.valor_actual
                    self.mejor_posicion_global =p.posicion_actual[:]
            else:
                if (p.valor_actual > self.mejor_valor_global):
                    self.mejor_valor_global = p.valor_actual
                    self.mejor_posicion_global =p.posicion_actual[:]



enjambre = Enjambre()
enjambre.crear(num_particulas=2, dimensiones=2, limites=(-100, 100))
for iteracion in range(10):
    print(f"\n--- Iteración No.{iteracion+1} ---")
    enjambre.evaluar_enjambre()
    enjambre.mover_enjambre()
    enjambre.mostrar_particulas()
    print(f"Mejor valor global: {enjambre.mejor_valor_global:.4f}")
    print(f"Mejor posición global: {enjambre.mejor_posicion_global}")