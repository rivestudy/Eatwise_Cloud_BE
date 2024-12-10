# app/routes/articles.py
from flask import Blueprint, request, jsonify
from app.utils.database import get_db_connection, execute_query
from app.utils.gcloud import upload_to_bucket
from app.utils.config import Config  # Import Config class to access bucket name

articles_bp = Blueprint('articles', __name__)

@articles_bp.route('/articles', methods=['GET'])
def get_articles():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles")
    rows = cursor.fetchall()

    return jsonify(rows), 200, {'X-Data-Name': 'Articles List'}
@articles_bp.route('/articles', methods=['POST'])
def add_article():
    data = request.form  
    file = request.files.get('image')  
    
    if not file:
        return jsonify({"error": "No image file provided"}), 400

    try:
        image_url = upload_to_bucket(Config.BUCKET_NAME, file) 
    except Exception as e:
        return jsonify({"error": str(e)}), 500 

    conn = get_db_connection()
    query = "INSERT INTO articles (title, description, content, image_url) VALUES (%s, %s, %s, %s)"
    execute_query(conn, query, (data['title'], data['description'], data['content'], image_url))

    response = jsonify({"message": "Article added successfully"})
    response.headers['X-Operation'] = 'Article Creation'
    return response, 201
