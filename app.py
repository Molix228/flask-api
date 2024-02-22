import os

import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
db = SQLAlchemy(app)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50))
    axle = db.Column(db.String(50))
    year = db.Column(db.String(10))
    price = db.Column(db.String(20))
    color = db.Column(db.String(20))
    weight = db.Column(db.String(20))
    mileage = db.Column(db.String(20))
    photo = db.Column(db.String(100))
    description = db.Column(db.Text)

with app.app_context():
    db.create_all()

@app.route('/api/cars', methods=['GET'])
def get_cars():
    try:
        cars = Car.query.all()
        car_list = []
        for car in cars:
            car_list.append({
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
                'photo': car.photo,
                'description': car.description
            })
        return jsonify({'cars': car_list})

    except Exception as e:
        app.logger.error(e)
        return jsonify({'error': str(e)}), 500

@app.route('/api/cars', methods=['POST'])
def add_car():
    try:
        data = request.form
        file = request.files['photo']

        # Сохраняем файл на сервере
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_car = Car(
            brand=data['brand'],
            model=data['model'],
            type=data['type'],
            axle=data['axle'],
            year=data['year'],
            price=data['price'],
            color=data['color'],
            weight=data['weight'],
            mileage=data['mileage'],
            photo=filename,  # Сохраняем имя файла в базе данных
            description=data['description']
        )

        db.session.add(new_car)
        db.session.commit()

        print("No errors so far")

        return jsonify({"message": "Car added successfully!"})

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)