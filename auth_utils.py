from datetime import datetime, timedelta
from functools import wraps
import jwt
from flask import jsonify, request, current_app
from models import User

def create_token(user_id, secret_key):
    expiration_time = datetime.utcnow() + timedelta(hours=1)
    payload = {'user_id': user_id, 'exp': expiration_time}
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def decode_token(token, secret_key):
    try:
        decoded = jwt.decode(token, secret_key, algorithms=['HS256'])
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        app = current_app
        with app.app_context():
            token = kwargs.get('token')

            if not token:
                return jsonify({'error': 'Token is missing'}), 401

            decoded_token = decode_token(token, app.config['SECRET_KEY'])

            if not decoded_token:
                return jsonify({'error': 'Invalid token'}), 401

            user_id = decoded_token.get('user_id')
            current_user = User.query.get(user_id)

            if not current_user:
                return jsonify({'error': 'User not found'}), 401

            return func(current_user, *args, **kwargs)

    return wrapper