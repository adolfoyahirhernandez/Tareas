import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.applications import MobileNetV2

ruta_dataset = "C:\\Users\\PC\\Documents\\Trabajos\\Topicos de IA\\proyecto\\dataset"

datos = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    zoom_range=0.2,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
    validation_split=0.3
)

datos_entrenamiento = datos.flow_from_directory(
    ruta_dataset,
    target_size=(224,224),
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

datos_validacion = datos.flow_from_directory(
    ruta_dataset,
    target_size=(224,224),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

base_modelo = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_modelo.trainable = False

modelo = Sequential([
    base_modelo,
    GlobalAveragePooling2D(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(50, activation='softmax') 
])

callbacks = [
    EarlyStopping(patience=5, restore_best_weights=True),
    ModelCheckpoint("mejor_modelo.keras", save_best_only=True)
]

modelo.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

modelo.fit(datos_entrenamiento, epochs=15, validation_data=datos_validacion, callbacks=callbacks, verbose=1)

modelo.save('modelo_clasificacion_plantas.keras')