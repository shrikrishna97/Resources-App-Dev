from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User, ParkingLot, ParkingSpot, Reservation
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
# from flask_cache import Cache

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'redis://localhost:6379/0'



CORS(app)

db.init_app(app)

jwt = JWTManager(app)

# cache = Cache()
# cache.init_app(app)



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
        access_token = create_access_token(identity=user.id, additional_claims={'role': user.role})
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
    
    for i in range(parkinglot.total_spots):
        parking_spot = ParkingSpot(parking_lot_id=parkinglot.id)
        
        db.session.add(parking_spot)
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
    if not parkinglot or parkinglot.is_deleted:
        return jsonify({'message': 'Parking lot not found'}), 404
    parkinglot.is_deleted = True
    db.session.commit()

    return jsonify({'message': 'Parking lot deleted successfully'}), 200

@app.route('/api/get/parkinglots', methods=['GET'])
@jwt_required()
# @cache.cached(timeout=60)
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
    
    users = User.query.all()
    data = []
    for user in users:
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            }
        data.append(user_data)
    return jsonify(data)


@app.route('/api/get/user/parkinglots', methods=['GET'])
@jwt_required()
def user_parkinglots():
    
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

from datetime import datetime

@app.route('/api/user_reservation', methods=['POST'])
@jwt_required()
def user_reservation():
    # if get_jwt().get('role') != 'user':
    #     return jsonify({'message': 'User access required'}), 403

    data = request.get_json()
    selected_lot_id = data.get('selected_lot')
    vehicle_number = data.get('vehicle_number')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    start = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")
    end = datetime.strptime(end_time, "%Y-%m-%dT%H:%M")
    
    lot = ParkingLot.query.get(selected_lot_id)
    print(lot.id)
    if lot:
        spot = ParkingSpot.query.filter_by(parking_lot_id=lot.id, status='available').first()
        print(spot)
        cost = lot.price * ((end - start).total_seconds() / 3600)  # Calculate cost based on hours
        reservation = Reservation(
            user_id=get_jwt_identity(),
            parking_spot_id=spot.id,
            vehicle_number=vehicle_number,
            start_time=start,
            end_time=end,
            status='active',
            cost=cost
        )
        db.session.add(reservation)
        db.session.commit()
        
        spot.status = 'reserved'
        db.session.commit()
    else:
        return jsonify({'message': 'Parking lot not found'}), 404    

    # Implement reservation logic here
    return jsonify({'message': 'Reservation created successfully'}), 200

@app.route('/api/user_reservations/<int:reservation_id>/release', methods=['PUT'])
@jwt_required()
def release_reservation(reservation_id):
    user_id = get_jwt_identity()
    reservation = Reservation.query.get(reservation_id)
    if not reservation or reservation.status != 'active' or reservation.user_id != user_id:
        return jsonify({'message': 'Reservation not found or already released'}), 404
    
    reservation.status = 'completed'
    db.session.commit()
    
    spot = ParkingSpot.query.get(reservation.parking_spot_id)
    spot.status = 'available'
    db.session.commit()
    
    return jsonify({'message': 'Reservation released successfully'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@gmail.com', password=generate_password_hash('admin'), role='admin')
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)