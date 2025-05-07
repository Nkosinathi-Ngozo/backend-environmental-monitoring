import jwt
from functools import wraps
from flask import request, jsonify, current_app

JWT_SECRET = 'your-secret-key'  # use current_app.config if you prefer

def verify_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Unauthorized: No token provided'}), 401

        token = auth_header.split('Bearer ')[1]

        try:
            decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            request.user = decoded  # Attach user to request
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 403

        return f(*args, **kwargs)
    return decorated


def verify_agent(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(request, 'user') or request.user.get('role') != 'agent':
            return jsonify({'error': 'Access denied: User is not an agent'}), 403
        return f(*args, **kwargs)
    return decorated


def verify_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(request, 'user') or request.user.get('role') != 'admin':
            return jsonify({'error': 'Access denied: User is not an admin'}), 403
        return f(*args, **kwargs)
    return decorated
