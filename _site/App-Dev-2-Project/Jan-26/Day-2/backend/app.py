from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User, ParkingLot, ParkingSpot, Reservation
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'


CORS(app)

db.init_app(app)

jwt = JWTManager(app)




@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    
    user = User(
        username=data['username'],
        email=data['email'],        
        password=generate_password_hash(data['password']),
        role='user'
    )
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 200

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'message': 'Login successful', 'data': {'username': user.username, 'email': user.email, 'role': user.role, 'access_token': access_token}}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and check_password_hash(user.password, data['password']) and user.role == 'admin':
        access_token = create_access_token(identity=user.id, additional_claims={'role': user.role})
        return jsonify({'message': 'Admin login successful', 'data': {'username': user.username, 'email': user.email, 'role': user.role, 'access_token': access_token}}), 200
    else:
        return jsonify({'message': 'Invalid admin credentials'}), 401
@app.route('/api/create/parkinglot', methods=['POST'])
@jwt_required()
def create_parkinglot():
    if get_jwt().get('role') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403

    data = request.get_json()
    parkinglot = ParkingLot(
        name=data['name'],
        city=data['city'],
        location=data['location'],
        price=data['price'],
        total_spots=data['total_spots']
    )
    db.session.add(parkinglot)
    db.session.commit()

    return jsonify({'message': 'Parking lot created successfully'}), 200

@app.route('/api/update/parkinglot/<int:parkinglot_id>', methods=['PUT'])
@jwt_required()
def update_parkinglot(parkinglot_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403

    parkinglot = ParkingLot.query.get(parkinglot_id)
    # pl = ParkingLot.query.filter_by(id=parkinglot_id).first()
    if not parkinglot:
        return jsonify({'message': 'Parking lot not found'}), 404

    data = request.get_json()
    parkinglot.city = data.get('city', parkinglot.city)
    parkinglot.location = data.get('location', parkinglot.location)
    parkinglot.price = data.get('price', parkinglot.price)
    parkinglot.total_spots = data.get('total_spots', parkinglot.total_spots)

    db.session.commit()

    return jsonify({'message': 'Parking lot updated successfully'}), 200

@app.route('/api/delete/parkinglot/<int:parkinglot_id>', methods=['DELETE'])
@jwt_required()
def delete_parkinglot(parkinglot_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403

    parkinglot = ParkingLot.query.get(parkinglot_id)
    if not parkinglot:
        return jsonify({'message': 'Parking lot not found'}), 404
    
    db.session.commit()

    return jsonify({'message': 'Parking lot deleted successfully'}), 200

@app.route('/api/get/parkinglots', methods=['GET'])
@jwt_required()
def get_parkinglots():
    if get_jwt().get('role') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403 
    
    parkinglots = ParkingLot.query.all()
    
    data = []
    for parkinglot in parkinglots:
        lot_data = {
            'id': parkinglot.id,
            'name': parkinglot.name,
            'city': parkinglot.city,
            'location': parkinglot.location,
            'price': parkinglot.price,
            'total_spots': parkinglot.total_spots
        }
        data.append(lot_data)
        
    return jsonify(data)



@app.route('/api/get-data', methods=['GET'])
@jwt_required()
def get_data():
    
    data = {
        'id': 1,
        'message': 'Hello from the backend',
        'items': [1, 2, 3, 4, 5]
        }
    return jsonify(data)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@gmail.com', password=generate_password_hash('admin'), role='admin')
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)