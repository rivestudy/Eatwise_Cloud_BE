import tensorflow as tf
from PIL import Image
import numpy as np

LABELS = ["a", "b", "c"]
MODEL_PATH = "./model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

def predict_image(image_path):
    img = Image.open(image_path).resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = img_array[np.newaxis, ...]
    predictions = model.predict(img_array)
    predicted_label = LABELS[np.argmax(predictions)]
    return predicted_label
