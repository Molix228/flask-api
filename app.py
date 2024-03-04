from flask import Flask
from cars import create_cars_app
from flask_cors import CORS

app = Flask(__name__)

# Регистрируем Blueprint
app.register_blueprint(create_cars_app(app), url_prefix='/api/cars')

# Разрешаем все источники (можете настроить на более конкретные в зависимости от вашей потребности)
CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
