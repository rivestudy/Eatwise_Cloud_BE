from flask import Blueprint, request, jsonify
from app.utils.database import get_db_connection, execute_query

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['POST'])
def add_user():
    data = request.json
    conn = get_db_connection()
    query = """
        INSERT INTO users (id, name, age, gender, height, weight, eat_goal)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    execute_query(conn, query, (
        data['id'],
        data['name'], data['age'], data['gender'], 
        data['height'], data['weight'], data['eat_goal']
    ))
    return jsonify({"message": "User added successfully"}), 201

@users_bp.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404
