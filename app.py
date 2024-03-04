from flask import Flask
from cars import create_cars_app

app = Flask(__name__)

# Регистрируем Blueprint
app.register_blueprint(create_cars_app(), url_prefix='/api/cars')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
