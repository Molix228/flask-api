from flask import Flask
from flask_cors import CORS
from cars import create_cars_app
from users import create_users_app
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(create_cars_app(app), url_prefix='/api/cars')
app.register_blueprint(create_users_app(app), url_prefix='/api/users/')


CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == '__main__':
    app.run(debug=True, port=5000)