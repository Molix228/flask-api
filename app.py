from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

cars = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('api/cars', methods=['GET'])
def get_cars():
    return jsonify({'cars': cars})

@app.route('api/cars', methods=['POST'])
def add_car():
    data = request.form.to_dict()

    new_car = {
        "brand": data["brand"],
        "model": data["model"],
        "type": data["type"],
        "year": int(data["year"]),
        "price": int(data["price"]),
        "color": data["color"],
        "weight": int(data["weight"]),
        "mileage": int(data["mileage"]),
        "specs": data["specs"],
        "photo": ''  # This will be updated with the uploaded file path
    }

    # Handle file upload
    if 'photo' in request.files:
        file = request.files['photo']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            new_car["photo"] = file_path

    cars.append(new_car)

    return jsonify({'message': 'Car added successfully!'})

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)