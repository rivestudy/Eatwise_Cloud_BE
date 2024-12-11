import numpy as np
import tensorflow as tf
import pandas as pd

MODEL_PATH = './model.h5'
model = tf.keras.models.load_model(MODEL_PATH)

NUTRITION_CSV_PATH = './nutritiondata.csv'
df = pd.read_csv(NUTRITION_CSV_PATH)

# Read class names from the 3rd column of the CSV
class_names = df.iloc[:, 2].unique().tolist()

def preprocess_image(file_stream):
    img = tf.keras.utils.load_img(file_stream, target_size=(224, 224))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
    return np.expand_dims(img_array, axis=0)

def get_prediction_with_threshold(predictions, class_names, threshold=80):
    max_confidence_idx = np.argmax(predictions)
    max_confidence_score = predictions[max_confidence_idx] * 100

    if max_confidence_score >= threshold:
        return {
            "label": class_names[max_confidence_idx],
            "confidence": max_confidence_score
        }
    return {
        "label": "Unknown",
        "confidence": 0.0
    }

def get_nutrition(label):
    row = df[df['food'] == label]
    if not row.empty:
        return {
            key.lower(): row[key].values[0]
            for key in df.columns if key != 'food'
        }
    return None