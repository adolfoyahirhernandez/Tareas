import random

X = 99

Matriz = [
    [0,2,9,9,7,3,3],
    [2,0,6,4,3,8,4],
    [9,6,0,5,4,2,4],
    [9,4,5,0,6,3,3],
    [7,3,4,6,0,2,2],
    [3,8,2,3,2,0,X],
    [6,3,2,7,9,X,0]
]

Num_ciudades = len(Matriz)

def evaluar(ruta):
    costo_total = 0
    for i in range (Num_ciudades-1):
        costo_total += Matriz[ruta[i]][ruta[i+1]]
    costo_total += Matriz[ruta[-1]][ruta[0]]
    return costo_total

def crear_ruta():
    ruta = list(range(Num_ciudades))
    random.shuffle(ruta)
    return ruta

def seleccionar(poblacion):
    seleccionados = random.sample(poblacion,3)
    return min(seleccionados, key=evaluar)

def cruce(c1, c2):
    tamano = len(c1)
    inicio, fin = sorted(random.sample(range(tamano),2))
    hijo = [None] * tamano
    hijo[inicio:fin] = c1[inicio:fin]
    pos = fin
    for ciudad in c2:
        if ciudad not in hijo:
            while hijo[pos % tamano] is not None:
                pos +=1
            hijo[pos % tamano] = ciudad
    return hijo

def mutar(ruta, prob=0.1):
    if random.random() < prob:
        i,j =random.sample(range(Num_ciudades),2)
        ruta[i], ruta[j] = ruta[j], ruta[i]
    return ruta

def algoritmo():
    poblacion = [crear_ruta() for _ in range(30)]
    generaciones = 200
    C = 0
    mejor_sol = 0

    for g in range(generaciones):
        nueva_poblacion = []
        for _ in range(len(poblacion)):
            padre_1 = seleccionar(poblacion)
            padre_2 = seleccionar(poblacion)
            hijo = cruce(padre_1, padre_2)
            hijo = mutar(hijo)
            nueva_poblacion.append(hijo)
        poblacion = nueva_poblacion
        mejor = min(poblacion, key=evaluar)
        if (mejor_sol == evaluar(mejor)):
            C+=1
        else:
            C=0
        
        if (C==5):
            break
        mejor_sol = evaluar(mejor)
        print(f"Generacion {g+1}: Ruta {mejor} - Costo: {evaluar(mejor)}")

algoritmo()