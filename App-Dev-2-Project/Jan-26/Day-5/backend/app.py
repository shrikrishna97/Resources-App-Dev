from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User, ParkingLot, ParkingSpot, Reservation
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_caching import Cache

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'



CORS(app)

db.init_app(app)

jwt = JWTManager(app)

cache = Cache(app)




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

@app.route('/api/user/my_reservations', methods=['GET'])
@jwt_required()
def my_reservations():
    user_id = get_jwt_identity()
    reservations = Reservation.query.filter_by(user_id=user_id).all()
    data = []
    
    for reservation in reservations:
        spot = ParkingSpot.query.get(reservation.parking_spot_id)
        lot = ParkingLot.query.get(spot.parking_lot_id)
        reservation_data = {
            'id': reservation.id,
            'vehicle_number': reservation.vehicle_number,
            'start_time': reservation.start_time.isoformat(),
            'end_time': reservation.end_time.isoformat(),
            'status': reservation.status,
            'cost': reservation.cost,
            'parking_lot': {
                'id': lot.id,
                'name': lot.name,
                'city': lot.city,
                'location': lot.location,
                'price': lot.price
            }
        }
        data.append(reservation_data)
    
    return jsonify(data)

@app.route('/api/admin/reservations', methods=['GET'])
@jwt_required()
def admin_reservations():
    if get_jwt().get('role') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403

    reservations = Reservation.query.all()
    data = []

    for reservation in reservations:
        user = User.query.get(reservation.user_id)
        spot = ParkingSpot.query.get(reservation.parking_spot_id)
        lot = ParkingLot.query.get(spot.parking_lot_id)
        reservation_data = {
            'id': reservation.id,
            'user_name': user.username if user else None,
            'vehicle_number': reservation.vehicle_number,
            'start_time': reservation.start_time.isoformat(),
            'end_time': reservation.end_time.isoformat(),
            'spot_number': spot.id if spot else None,
            'status': reservation.status,
            'cost': reservation.cost,
            'parking_lot': {
                'id': lot.id,
                'name': lot.name,
                'city': lot.city,
                'location': lot.location,
                'price': lot.price
            }
        }
        data.append(reservation_data)

    return jsonify(data)

@app.route('/api/export/reservations', methods=['GET'])
@jwt_required()
def export_reservations():
    user_id = get_jwt_identity()
    from tasks import export_reservations_report
    export_reservations_report.delay(user_id)
    return jsonify({'message': 'Reservations report is being generated and will be sent to your email shortly.'}), 200

@app.route('/api/user/summary', methods=['GET'])
@jwt_required()
def user_summary():
    user_id = get_jwt_identity()
    reservations = Reservation.query.filter_by(user_id=user_id).all()
    lot_summary = {}
    for reservation in reservations:
        spot = ParkingSpot.query.get(reservation.parking_spot_id)
        lot = ParkingLot.query.get(spot.parking_lot_id)
        if lot.name not in lot_summary:
            lot_summary[lot.name] = {
                'total_reservations': 0,
                'total_cost': 0.0
            }
        lot_summary[lot.name]['total_reservations'] += 1
        lot_summary[lot.name]['total_cost'] += reservation.cost
        
    lot_names =[]
    lot_counts = []
    lot_costs = []
    for lot_name, summary in lot_summary.items():
        lot_names.append(lot_name)  
        lot_counts.append(summary['total_reservations'])
        lot_costs.append(summary['total_cost'])
    
    total_spent = sum(summary['total_cost'] for summary in lot_summary.values())
    active_reservations = sum(1 for reservation in reservations if reservation.status == 'active')        
    completed_reservations = sum(1 for reservation in reservations if reservation.status == 'completed')
    
    return jsonify({
        'lot_names': lot_names,
        'lot_counts': lot_counts,
        'lot_costs': lot_costs,
        'total_spent': total_spent,        
        'active_reservations': active_reservations,        
        'completed_reservations': completed_reservations,
        'total': len(reservations)
        })


@app.route('/api/admin/summary', methods=['GET'])
@jwt_required()
def admin_summary():
    if get_jwt().get('role') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403

    reservations = Reservation.query.all()
    lot_summary = {}
    for reservation in reservations:
        spot = ParkingSpot.query.get(reservation.parking_spot_id)
        lot = ParkingLot.query.get(spot.parking_lot_id)
        if lot.name not in lot_summary:
            lot_summary[lot.name] = {
                'total_reservations': 0,
                'total_revenue': 0.0
            }
        lot_summary[lot.name]['total_reservations'] += 1
        lot_summary[lot.name]['total_revenue'] += reservation.cost
        
    lot_names =[]
    lot_counts = []
    lot_revenues = []
    for lot_name, summary in lot_summary.items():
        lot_names.append(lot_name)  
        lot_counts.append(summary['total_reservations'])
        lot_revenues.append(summary['total_revenue'])
    
    total_revenue = sum(summary['total_revenue'] for summary in lot_summary.values())
    
    return jsonify({
        'lot_names': lot_names,
        'lot_counts': lot_counts,
        'lot_revenues': lot_revenues,
        'total_revenue': total_revenue,        
        'total_reservations': len(reservations)
        })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@gmail.com', password=generate_password_hash('admin'), role='admin')
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)