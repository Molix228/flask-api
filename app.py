from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
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

# Указываем разрешенные методы запроса
cors = CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST"]}})

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/cars', methods=['GET'])
def get_cars():
    cars = Car.query.all()
    return jsonify({'cars': [car.serialize for car in cars]})

@app.route('/api/cars', methods=['POST'])
def add_car():
    try:
        data = request.form.to_dict()

        # Create the 'uploads' folder if it doesn't exist
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

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
    with app.app_context():
        db.create_all()
    app.run(debug=True)