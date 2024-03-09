import os
from flask import request, jsonify, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_cors import CORS
from models import db, Car
from config import Config

def create_cars_app(app):
    cars_app = Blueprint('cars_app', __name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGTH = Config.MAX_CONTENT_LENGTH
    app.config['SECRET_KEY'] = Config.SECRET_KEY

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

    CORS(cars_app, resources={r"/*": {"origins": "*"}})

    @cars_app.route('/', methods=['GET'])
    def get_cars():
        try:
            cars = Car.query.all()
            car_list = []
            for car in cars:
                car_list.append(format_car(car))
            return jsonify({'cars': car_list})
        except Exception as e:
            return jsonify({'error': 'Internal Server Error'}), 500

    @cars_app.route('/', methods=['POST'])
    def add_car():
        try:
            form = request.form
            file = request.files['photo']

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("Received Form Data:", form)

            new_car = Car(
                brand=form['brand'],
                model=form['model'],
                type=form['type'],
                axle=form['axle'],
                year=form['year'],
                price=form['price'],
                color=form['color'],
                weight=form['weight'],
                mileage=form['mileage'],
                photo=filename,
                description=form['description']
            )

            db.session.add(new_car)
            db.session.commit()

            return jsonify({"message": "Car added successfully!"})
        except Exception as e:
            print("Error:", e)
            db.session.rollback()
            return jsonify({"error": f"Internal Server Error: {e}"}), 500

    @cars_app.route('/<int:car_id>', methods=['DELETE'])
    def delete_car(car_id):
        try:
            car = Car.query.get_or_404(car_id)

            if car.photo:
                photo_path = os.path.join(app.config['UPLOAD_FOLDER'], car.photo)
                if os.path.exists(photo_path):
                    os.remove(photo_path)

            db.session.delete(car)
            db.session.commit()

            return jsonify({"message": "Car deleted successfully!"})
        except Exception as e:
            print("Error:", e)
            db.session.rollback()
            return jsonify({"error": f"Internal Server Error: {e}"}), 500

    def format_car(car):
        return {
            'id': car.id,
            'brand': car.brand,
            'model': car.model,
            'type': car.type,
            'axle': car.axle,
            'year': car.year,
            'price': car.price,
            'color': car.color,
            'weight': car.weight,
            'mileage': car.mileage,
            'photo': url_for('static', filename=f'uploads/{car.photo}'),
            'description': car.description
        }

    return cars_app