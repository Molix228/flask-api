from flask import Flask
from flask_cors import CORS
from cars import create_cars_app
from users import create_users_app
from config import Config
from models import db  # Импортируем экземпляр SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Создание таблицы пользователей и машин
with app.app_context():
    db.create_all()

# Регистрируем Blueprint для машин
app.register_blueprint(create_cars_app(app), url_prefix='/api/cars')

# Регистрируем Blueprint для пользователей
app.register_blueprint(create_users_app(app), url_prefix='/api/users/')


# Разрешаем все источники (можете настроить на более конкретные в зависимости от вашей потребности)
CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == '__main__':
    app.run(debug=True, port=5000)