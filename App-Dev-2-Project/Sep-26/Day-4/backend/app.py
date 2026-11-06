from flask import Flask, jsonify, request
from models import db, User,ParkingLot, ParkingSpot, Reservation
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt
from flask_cors import CORS
from flask_caching import Cache


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)
# jwt = JWTManager()
# jwt.init_app(app)
CORS(app)
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)

    
    
cache = Cache(app)    

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    # Process the login data
    if user and check_password_hash(user.password, data.get('password')):
        access_token = create_access_token(identity=user.id, additional_claims={'role': user.role})
        return jsonify({'message': 'Login successful', 'status': 'success', 'access_token': access_token})

    return jsonify({'message': 'Not authorized', 'status': 'error'}), 401

@app.route('/api/register', methods=['GET','POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided', 'status': 'error'}), 400
    if request.method == 'POST' and data:
        print(data)
        user = User.query.filter_by(username=data['username']).first()
        if user:
            return jsonify({'message': 'User already exists', 'status': 'error'}), 400
        new_user = User(username=data['username'], email=data['email'], password=generate_password_hash(data['password']))
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully', 'status': 'success'}), 200
    
# create a parking lot from admin
@app.route('/api/create_parking_lot', methods=['POST'])
@jwt_required()
def create_parking_lot():
    role = get_jwt().get('role')
    if role != 'admin':
        return jsonify({'message': 'Not authorized', 'status': 'error'}), 403
    parking_lot_data = request.get_json()
    if  parking_lot_data:
        new_parking_lot = ParkingLot(
            name=parking_lot_data['name'],
            city=parking_lot_data['city'],
            location=parking_lot_data['location'],
            total_spots=parking_lot_data['total_spots'],
            price=parking_lot_data['price']
        )
        db.session.add(new_parking_lot)
        db.session.commit()
        
        for i in range(parking_lot_data['total_spots']):
            new_parking_spot = ParkingSpot(lot_id=new_parking_lot.id)
            db.session.add(new_parking_spot)
        db.session.commit()

        return jsonify({'message': 'Parking lot created successfully', 'status': 'success'}), 200

@app.route('/api/update_parking_lot/<int:lot_id>', methods=['PUT'])
@jwt_required()
def update_parking_lot(lot_id):
    role = get_jwt().get('role')
    if role != 'admin':
        return jsonify({'message': 'Not authorized', 'status': 'error'}), 403
    
    parking_lot = ParkingLot.query.get_or_404(lot_id)
    data = request.get_json()
    if data:
        if data.get('total_spots') > parking_lot.total_spots:
            parking_lot.name = data.get('name', parking_lot.name)
            parking_lot.total_spots = data.get('total_spots', parking_lot.total_spots)
            parking_lot.price = data.get('price', parking_lot.price)
            new_spots_count = data.get('total_spots') - parking_lot.total_spots

            db.session.commit()
            
            for i in range(new_spots_count):
                new_parking_spot = ParkingSpot(lot_id=parking_lot.id)
                db.session.add(new_parking_spot)
            db.session.commit()
        else:
            return jsonify({'message': 'Total spots cannot be decreased', 'status': 'error'}), 400

        return jsonify({'message': 'Parking lot updated successfully', 'status': 'success'}), 200

    return jsonify({'message': 'No update data provided', 'status': 'error'}), 400

@app.route('/api/admin/parking_lots', methods=['GET'])
@jwt_required()
@cache.cached(timeout=10)
def get_parking_lots():
    role = get_jwt().get('role')
    if role != 'admin':
        return jsonify({'message': 'Not authorized', 'status': 'error'}), 403
    parking_lots = ParkingLot.query.all()
    parking_lots_data = []
    for lot in parking_lots:
        parking_lots_data.append({
            'id': lot.id,
            'name': lot.name,
            'city': lot.city,
            'location': lot.location,
            'total_spots': lot.total_spots,
            'price': lot.price,
            'is_deleted': lot.is_deleted
        })
    return jsonify(parking_lots_data), 200



@app.route('/api/user_data', methods=['GET'])
@jwt_required()
def get_user_data():
    role = get_jwt().get('role')
    if role != 'admin':
        return jsonify({'message': 'Not authorized', 'status': 'error'}), 403
    user_data = User.query.all()
    data = []
    for user in user_data:
        data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'status': user.status
        })
    # return data
    return jsonify(data), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(role='admin').first():
            admin_user = User(username='admin',email="admin@gmail.com",password=generate_password_hash('admin123'), role='admin')
            db.session.add(admin_user)
            db.session.commit()
    app.run(debug=True)