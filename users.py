from flask import Blueprint, request, jsonify
from werkzeug.exceptions import NotFound
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from models import db, User

def create_users_app(app):
    users_app = Blueprint('users_app', __name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'wazxdesz21'

    # db.init_app(app)
    #
    # with app.app_context():
    #     db.create_all()

    CORS(users_app, resources={r"/*": {"origins": "*"}})

    @users_app.route('/register', methods=['POST'])
    def register_user():
        try:
            data = request.form
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')

            # Проверка наличия обязательных данных
            if not username or not password or not email:
                return jsonify({'error': 'All fields are required'}), 400

            # Хеширование пароля перед сохранением в базу данных
            hashed_password = generate_password_hash(password, method='sha256')

            # Создание нового пользователя
            new_user = User(username=username, password=hashed_password, email=email)
            db.session.add(new_user)
            db.session.commit()

            return jsonify({'message': 'User registered successfully'}), 200

        except Exception as e:
            print("Error:", e)
            db.session.rollback()
            return jsonify({'error': 'Internal Server Error'}), 500

    @users_app.route('/get_all', methods=['GET'])
    def get_all_users():
        try:
            users = User.query.all()
            user_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
            return jsonify({'users': user_list}), 200
        except Exception as e:
            return jsonify({'error': 'Internal Server Error'}), 500

    @users_app.route('/delete/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        try:
            user = User.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "User deleted successfully!"}), 200
        except Exception as e:
            print("Error:", e)
            db.session.rollback()
            return jsonify({"error": f"Internal Server Error: {e}"}), 500

    @users_app.route('/update/<int:user_id>', methods=['PATCH'])
    def update_user(user_id):
        try:
            user = User.query.get_or_404(user_id)
            data = request.form

            if 'username' in data:
                user.username = data['username']
            if 'password' in data:
                user.password = generate_password_hash(data['password'], method='sha256')
            if 'email' in data:
                user.email = data['email']

            db.session.commit()
            return jsonify({"message": "User updated successfully!"}), 200

        except NotFound:
            return jsonify({"error": f"User with ID {user_id} not found"}), 404
        except Exception as e:
            print("Error:", e)
            db.session.rollback()
            return jsonify({"error": f"Internal Server Error: {e}"}), 500

    return users_app