from flask import Flask, jsonify, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class Car:
    def __init__(self, brand, model, car_type, year, price, color, weight, mileage, specs, photo):
        self.brand = brand
        self.model = model
        self.type = car_type
        self.year = year
        self.price = price
        self.color = color
        self.weight = weight
        self.mileage = mileage
        self.specs = specs
        self.photo = photo

    def to_dict(self):
        return {
            'brand': self.brand,
            'model': self.model,
            'type': self.type,
            'year': self.year,
            'price': self.price,
            'color': self.color,
            'weight': self.weight,
            'mileage': self.mileage,
            'specs': self.specs,
            'photo': self.photo,
        }

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

all_cars = []

@app.route('/api/all_cars', methods=['GET'])
def get_all_cars():
    return jsonify([car.to_dict() for car in all_cars])

@app.route('/api/cars', methods=['POST'])
def add_car():
    data = request.form
    brand = data.get('brand')
    model = data.get('model')
    car_type = data.get('type')
    year = int(data.get('year'))
    price = int(data.get('price'))
    color = data.get('color')
    weight = int(data.get('weight'))
    mileage = int(data.get('mileage'))
    specs = data.get('specs')
    photo = request.files.get('photo')

    # Базовая валидация
    if not brand or not model or not car_type or year < 0 or price < 0 or not color or weight < 0 or mileage < 0:
        return jsonify({'error': 'Invalid data. Please fill in all required fields with valid values.'}), 400

    if not allowed_file(photo.filename):
        return jsonify({'error': 'Invalid file format. Allowed formats are png, jpg, jpeg, gif.'}), 400

    new_car = Car(brand, model, car_type, year, price, color, weight, mileage, specs, photo.filename)
    all_cars.append(new_car)

    # Сохранение файла в папку uploads
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo.filename))

    return jsonify({'message': 'Car added successfully'})