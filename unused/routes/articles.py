from flask import Blueprint, request, jsonify
from app.utils.database import get_db_connection, execute_query
from app.utils.gcloud import upload_to_bucket

articles_bp = Blueprint('articles', __name__)

@articles_bp.route('/articles', methods=['GET'])
def get_articles():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles")
    rows = cursor.fetchall()
    return jsonify(rows)

@articles_bp.route('/articles', methods=['POST'])
def add_article():
    data = request.form
    file = request.files.get('image')
    image_url = upload_to_bucket(None, file)

    conn = get_db_connection()
    query = "INSERT INTO articles (title, description, content, image_url) VALUES (%s, %s, %s, %s)"
    execute_query(conn, query, (data['title'], data['description'], data['content'], image_url))
    return jsonify({"message": "Article added successfully"})
