from flask import Blueprint, request, jsonify
from app.model.predict import predict_image
from app.utils.gcloud import upload_to_bucket
from app.utils.database import get_db_connection, execute_query
from datetime import datetime

predictions_bp = Blueprint('predictions', __name__)

@predictions_bp.route('/predict', methods=['POST'])
def predict():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    file.save("temp_image.jpg")

    predicted_food = predict_image("temp_image.jpg")
    gcs_url = upload_to_bucket(None, "temp_image.jpg")

    conn = get_db_connection()
    query = """
        INSERT INTO predict_history (user_id, food_name, prediction_date)
        VALUES (%s, %s, %s)
    """
    execute_query(conn, query, (user_id, predicted_food, datetime.now()))

    return jsonify({
        "predicted_food": predicted_food,
        "file_url": gcs_url
    })
