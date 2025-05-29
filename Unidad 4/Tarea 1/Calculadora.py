import numpy as np

datos=[]
resultados=[]

for a in range(10):
    for b in range(10):
        datos.append([a,b])
        resultados.append([
            a + b,
            a - b,
            a * b,
            a / b if b!=0 else 0
        ])

datos = np.array(datos, dtype=np.float32)
resultados = np.array(resultados, dtype=np.float32)

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

modelo = Sequential([
    Dense(32, input_dim=2, activation='relu'),
    Dense(64, activation='relu'),
    Dense(4)
])

modelo.compile(optimizer='adam', loss='mse')

modelo.fit(datos, resultados, epochs=500, verbose=1)

prueba = np.array([[4,8]], dtype=np.float32)
prediccion = modelo.predict(prueba)
print(prediccion[0])