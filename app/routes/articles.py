from flask import Blueprint, request, make_response, jsonify
from app.utils.database import get_db_connection, execute_query
from app.utils.gcloud import upload_to_bucket
from app.utils.config import Config  

articles_bp = Blueprint('articles', __name__)
@articles_bp.route('/articles', methods=['GET'])
def get_articles():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles")
    rows = cursor.fetchall()
    
    articles_data = []

    response = make_response(jsonify(rows), 200)
    response.headers['Content-Type'] = 'application/json'
    response.headers['X-Data-Name'] = 'Articles List'
    response.headers['Access-Control-Allow-Origin'] = '*'
    
    for idx, row in enumerate(rows):
        article_id = row[0]  
        title = row[1] 
        description = row[2]  
        content = row[3]  
        image_url = row[4] 
        timestamp = row[5]  
        
        response.headers[f'X-Article-{article_id}-Title'] = title
        response.headers[f'X-Article-{article_id}-Description'] = description
        response.headers[f'X-Article-{article_id}-Content'] = content
        response.headers[f'X-Article-{article_id}-Image_url'] = image_url
        response.headers[f'X-Article-{article_id}-Timestamp'] = timestamp
        
        articles_data.append({
            'id': article_id,
            'title': title,
            'description': description,
            'content': content,
            'image_url': image_url,
            'timestamp': timestamp
        })
    
    response.set_data(jsonify(articles_data).get_data())
    
    return response
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