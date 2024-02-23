from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, FileField

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
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


class CarForm(FlaskForm):
    brand = StringField('Brand')
    model = StringField('Model')
    type = StringField('Type')
    axle = StringField('Axle')
    year = StringField('Year')
    price = StringField('Price')
    color = StringField('Color')
    weight = StringField('Weight')
    mileage = StringField('Mileage')
    photo = FileField('Photo')
    description = StringField('Description')


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
                'photo': car.photo,
                'description': car.description
            })
        return jsonify({'cars': car_list})

    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/cars', methods=['POST'])
def add_car():
    try:
        form = CarForm(request.form)

        if form.validate_on_submit():
            file = request.files['photo']

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            new_car = Car(
                brand=form.brand.data,
                model=form.model.data,
                type=form.type.data,
                axle=form.axle.data,
                year=form.year.data,
                price=form.price.data,
                color=form.color.data,
                weight=form.weight.data,
                mileage=form.mileage.data,
                photo=filename,
                description=form.description.data
            )

            db.session.add(new_car)
            db.session.commit()

            return jsonify({"message": "Car added successfully!"})
        else:
            return jsonify({"error": "Invalid form data"}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Internal Server Error: {e}"}), 500


if __name__ == '__main__':
    app.run(debug=True)