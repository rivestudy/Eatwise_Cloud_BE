import os
import requests
from flask import Flask, request, jsonify
from google.cloud import storage
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker
from config import CLOUD_STORAGE_BUCKET, CLOUD_SQL_CONNECTION_NAME, DB_USER, DB_PASSWORD, DB_NAME

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

storage_client = storage.Client()

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}?host=/cloudsql/{CLOUD_SQL_CONNECTION_NAME}"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

ML_API_URL = "https://your-ml-model-api-xyz.a.run.app/predict"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_blob_to_gcs(filename, file):
    bucket = storage_client.get_bucket(CLOUD_STORAGE_BUCKET)
    blob = bucket.blob(filename)
    blob.upload_from_file(file)
    return blob.public_url

def get_prediction_from_ml_model(image_file):
    files = {'file': image_file}
    response = requests.post(ML_API_URL, files=files)
    if response.status_code == 200:
        return response.json().get('prediction')
    else:
        return None

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        file_url = upload_blob_to_gcs(filename, file)
        
        prediction = get_prediction_from_ml_model(file)
        
        if prediction is not None:
            return jsonify({"message": "File uploaded successfully", "file_url": file_url, "prediction": prediction}), 200
        else:
            return jsonify({"error": "Prediction failed"}), 500
    else:
        return jsonify({"error": "Invalid file type"}), 400

if __name__ == '__main__':
    app.run(debug=True)
