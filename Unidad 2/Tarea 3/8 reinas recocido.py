import math
import random
import time

N=8

# Se genera un tablero, el cual tenga las reinas en diferentes partes del tablero
def generar_estado_inicial():
    # Se genera un tablero vacio
    tablero = [['-' for _ in range(N)] for _ in range(N)]
    
    # Se genera una lista de todas las posiciones posibles en el tablero
    posiciones = [(fila, col) for fila in range(N) for col in range(N)]
    
    # Selecciona posiciones aleatorias del tablero
    posiciones_seleccionadas = random.sample(posiciones, N)

    # Coloca 'O' para representar a las reinas
    for fila, columna in posiciones_seleccionadas:
        tablero[fila][columna] = 'O'
    
    return tablero

def generar_estado_inicial_2():
    # Se genera un tablero vacio
    tablero = [['-' for _ in range(N)] for _ in range(N)]
    
    
    tablero[0][0] = 'O'
    
    return tablero


# Se verifica si hay conflictos en las reinas
def verificar_conflictos(tablero):
    conflictos = 0

    # Verifica las filas y columnas
    for i in range(N):
        num_reinas_fila = tablero[i].count('O')
        num_reinas_columna = sum(tablero[j][i] == 'O' for j in range(N))

        # Si hay mas de una reina en una fila o columna se suma un conflicto
        if num_reinas_fila > 1:
            conflictos += num_reinas_fila - 1
        if num_reinas_columna > 1:
            conflictos += num_reinas_columna -1

    # Verifica las diagonales
    for d in range(-(N-1), N):
        diagonal_1 = [tablero[i][i + d] for i in range(N) if 0 <= i + d < N]
        if diagonal_1.count('O') > 1:
            conflictos += diagonal_1.count('O') - 1

        diagonal_2 = [tablero[i][(N-1) - (i + d)] for i in range(N) if 0 <= (N-1) - (i + d) < N]
        if diagonal_2.count('O') > 1:
            conflictos += diagonal_2.count('O') - 1

    return conflictos

# Genera vecinos moviendo una reina a una posición aleatoria
def generar_vecinos(tablero):
    vecinos = []

    for _ in range(6):  # Generamos los vecinos
        nuevo_tablero = [fila[:] for fila in tablero]

        # Se elige una reina al azar
        reinas = [(fila, col) for fila in range(N) for col in range(N) if tablero[fila][col] == 'O']
        
        fila_ant, col_ant = random.choice(reinas)
        # Se escoge una nueva posicion al azar
        fila_nueva, col_nueva = random.randint(0, (N-1)), random.randint(0, (N-1))

        # Verifica que la nueva posición no esté ocupada por otra reina
        while nuevo_tablero[fila_nueva][col_nueva] == 'O':
            fila_nueva, col_nueva = random.randint(0, (N-1)), random.randint(0, (N-1))

        nuevo_tablero[fila_ant][col_ant] = '-'  
        nuevo_tablero[fila_nueva][col_nueva] = 'O'  # Mover a la reina

        vecinos.append(nuevo_tablero)

    return vecinos


# Algoritmo de Recocido Simulado
def recocido_simulado():
    temperatura = 100.0
    factor_enfriamiento = 0.5
    min_temperatura = 0
    estado_actual = generar_estado_inicial()
    mejor_estado = estado_actual[:]
    mejor_conflictos = verificar_conflictos(estado_actual)
    imprimir_tablero(mejor_estado)

    movimientos = 0
    inicio = time.time()

    while temperatura > min_temperatura:
        vecinos = generar_vecinos(estado_actual)
        vecino = sorted(vecinos, key=verificar_conflictos)[0]

        conflictos_actuales = verificar_conflictos(estado_actual)
        conflictos_vecino = verificar_conflictos(vecino)

        delta = conflictos_vecino - conflictos_actuales

        # Si el vecino es mejor o se acepta por probabilidad
        if delta < 0 or random.random() < math.exp(-delta / temperatura):
            estado_actual = vecino
            conflictos_actuales = conflictos_vecino
            movimientos += 1

        if conflictos_actuales < mejor_conflictos:
            mejor_estado = estado_actual[:]
            mejor_conflictos = conflictos_actuales

        if mejor_conflictos == 0:
            break

        temperatura *= factor_enfriamiento 

    fin = time.time()
    tiempo = fin - inicio

    posiciones = [(fila, col) for fila in range(N) for col in range(N) if mejor_estado[fila][col] == 'O']
    return mejor_estado, mejor_conflictos, tiempo, movimientos, posiciones

# Imprime el trablero
def imprimir_tablero(tablero):
    for fila in tablero:
        print(' '.join(fila))

# Ejecuta la búsqueda tabú
solucion, conflictos, tiempo, movimientos, posiciones_finales = recocido_simulado()

# Muestra los resultados
print("\nMejor solución encontrada:")
imprimir_tablero(solucion)
print(f"\nConflictos: {conflictos}")
print(f"Movimientos: {movimientos}")
print(f"Tiempo de ejecución: {tiempo:.4f} segundos")
print(f"Posiciones:\n{posiciones_finales}")