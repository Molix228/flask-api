from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)

# Режим разработки (для локального сервера)
if os.environ.get('FLASK_ENV') == 'development':
    app.config['DEBUG'] = True

# Устанавливаем CORS только для нужных методов
CORS(app, resources={r"/api/cars": {"origins": "*", "methods": ["GET", "POST"]}})

# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}

db = SQLAlchemy(app)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    axle = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(80), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    photo = db.Column(db.String(200), nullable=False)

# Создаем 'uploads' директорию, если она не существует
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Инициализация базы данных
db.create_all()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/api/cars', methods=['GET'])
def get_cars():
    cars = Car.query.all()
    return jsonify({'cars': [car.serialize for car in cars]})

@app.route('/api/cars', methods=['POST'])
def add_car():
    try:
        data = request.form.to_dict()

        # Проверяем наличие обязательных полей
        required_fields = ['brand', 'model', 'axle', 'type', 'year', 'price', 'color', 'weight', 'mileage', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Валидация полей year, price, weight, mileage
        for numeric_field in ['year', 'price', 'weight', 'mileage']:
            if not data[numeric_field].isdigit():
                return jsonify({'error': f'Invalid value for {numeric_field}'}), 400

        # Handle multiple file upload
        photos = []
        if 'photo' in request.files:
            files = request.files.getlist('photo')
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    photos.append(file_path)

        new_car = Car(
            brand=data["brand"],
            model=data["model"],
            axle=data["axle"],
            type=data["type"],
            year=int(data["year"]),
            price=int(data["price"]),
            color=data["color"],
            weight=int(data["weight"]),
            mileage=int(data["mileage"]),
            description=data["description"],
            photo=photos
        )

        db.session.add(new_car)
        db.session.commit()

        return jsonify({'message': 'Car added successfully!'})

    except Exception as e:
        error_message = f"Error adding car: {str(e)}"
        print(error_message)
        return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    app.run(debug=True)  # This line is for local development
    # The following lines are for deployment on render.com
    import os
    workers = int(os.environ.get('GUNICORN_WORKERS', '4'))
    from gunicorn.app.base import BaseApplication
    class StandaloneApplication(BaseApplication):
        def __init__(self, app, workers=4):
            self.application = app
            self.workers = workers
            super().__init__()
        def load_config(self):
            from gunicorn.config import Config
            config = Config()
            config.set('workers', self.workers)
            return config
        def load(self):
            return self.application

    standalone_app = StandaloneApplication(app, workers)
    standalone_app.run()