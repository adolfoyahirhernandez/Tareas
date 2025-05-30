import tensorflow as tf
import numpy as np
import cv2
import json

# === Rutas ===
ruta_modelo = "C:\\Users\\PC\\Documents\\Trabajos\\Topicos de IA\\proyecto\\modelo_clasificacion_plantas.keras"
ruta_etiquetas = "C:\\Users\\PC\\Documents\\Trabajos\\Topicos de IA\\proyecto\\clases.json"
ruta_val = "C:\\Users\\PC\\Documents\\Trabajos\\Topicos de IA\\proyecto\\validacion"

modelo = tf.keras.models.load_model(ruta_modelo)

modelo.compile(optimizer='adam',
               loss='categorical_crossentropy',
               metrics=['accuracy'])

with open(ruta_etiquetas, 'r') as f:
    etiquetas = json.load(f)
indice_a_clase = {v: k for k, v in etiquetas.items()}

val_data = tf.keras.utils.image_dataset_from_directory(
    ruta_val,
    image_size=(224, 224),
    batch_size=32,
    label_mode='categorical'
)


print("\n--- Evaluando modelo ---")
resultados = modelo.evaluate(val_data, verbose=1)
for nombre, valor in zip(modelo.metrics_names, resultados):
    print(f"{nombre}: {valor:.4f}")

def predecir(frame):
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, (224, 224))
    img_norm = img_resized.astype('float32') / 255.0
    entrada = np.expand_dims(img_norm, axis=0)
    predicciones = modelo.predict(entrada, verbose=0)
    indice = np.argmax(predicciones[0])
    nombre = indice_a_clase.get(indice, "Desconocido")
    confianza = predicciones[0][indice]
    return nombre, confianza

print("\n--- Iniciando cámara para clasificar en tiempo real ---")
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("No se pudo abrir la cámara")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo recibir frame")
        break

    nombre, confianza = predecir(frame)
    texto = f"{nombre}: {confianza*100:.2f}%"
    cv2.putText(frame, texto, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    cv2.imshow('Clasificador de Plantas', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
