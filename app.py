import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
app.config['SECRET_KEY'] = 'wazxdesz21'
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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

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
                'photo': url_for('static', filename=f'static/uploads/{car.photo}'),
                'description': car.description
            })
        return jsonify({'cars': car_list})
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/cars', methods=['POST'])
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

@app.route('/api/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    try:
        car = Car.query.get_or_404(car_id)
        # Удаление изображения из папки uploads
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


if __name__ == '__main__':
    app.run(debug=True)