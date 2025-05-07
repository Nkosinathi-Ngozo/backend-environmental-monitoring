import jwt
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash
from models import User

main = Blueprint('main', __name__)


# Replace with a secure, secret key in production
JWT_SECRET = 'your-secret-key'
JWT_EXPIRY_MINUTES = 60  # Token valid for 1 hour

@main.route('api/v1/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401

    # Create JWT payload
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(minutes=JWT_EXPIRY_MINUTES)
    }

    # Generate token
    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')

    return jsonify({'message': 'Login successful', 
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'role_id': user.role_id,
                        'created_at': user.created_at.isoformat()
                    },
                    'token': token}), 200
