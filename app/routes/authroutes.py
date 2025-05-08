import jwt
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, db
from app.middleware.authmiddleware import verify_token, verify_admin, verify_icer

auth = Blueprint('auth', __name__)

# Config (ideally set in app config)
JWT_SECRET = 'your-secret-key'
JWT_EXPIRY_MINUTES = 60  # Token valid for 1 hour


@auth.route('/api/v1/login', methods=['POST'])
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
        'role': user.role_id,
        'exp': datetime.utcnow() + timedelta(minutes=JWT_EXPIRY_MINUTES)
    }

    # Generate token
    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    if isinstance(token, bytes):
        token = token.decode('utf-8')  # Ensure it's a string

    return jsonify({
        'message': 'Login successful',
        'user': {
            'id': user.id,
            'email': user.email,
            'role_id': user.role_id,
            'created_at': user.created_at.isoformat() if isinstance(user.created_at, datetime) else user.created_at
        },
        'token': token
    }), 200

 # Assumes this checks if the current user is allowed to create admins
@auth.route('/api/v1/auth/register-icer', methods=['POST'])
@verify_token
@verify_icer 
def register_icer():
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400

    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'error': 'Icer already exists'}), 409

    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        email=data['email'],
        password=hashed_password,
        role_id='icer',  # Assuming this is how roles are stored
        created_at=datetime.utcnow()
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Icer registration successful'}), 201


@auth.route('/api/v1/auth/register-admin', methods=['POST'])
@verify_token
@verify_icer  # Assumes this checks if the current user is allowed to create admins
def register_admin():
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400

    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'error': 'Admin already exists'}), 409

    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        email=data['email'],
        password=hashed_password,
        role_id='admin',  # Assuming this is how roles are stored
        created_at=datetime.utcnow()
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Admin registration successful'}), 201


@auth.route('/api/v1/auth/register-user', methods=['POST'])
@verify_token
@verify_admin  # Assumes this checks if the current user is allowed to create admins
def register_user():
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400

    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'error': 'Admin already exists'}), 409

    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        email=data['email'],
        password=hashed_password,
        role_id='user',  # Assuming this is how roles are stored
        created_at=datetime.utcnow()
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registration successful'}), 201
