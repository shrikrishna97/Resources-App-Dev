from flask import Flask , jsonify, request
from flask_cors import CORS
from model import db , User, ParkingLot, ParkingSpot, Reservation
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_caching import Cache

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SECRET_KEY"] = "your-secret-key"

app.config["JWT_SECRET_KEY"] = "your-key"
app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/0"

CORS(app)

JWTManager(app)

cache = Cache(app)


db.init_app(app)


@app.route("/register" , methods=["GET" , "POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    if request.method == "POST":
        data = request.get_json()
        print(data)
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        # role = data.get("role")
        
        user = User(username=username, password=generate_password_hash(password), email=email) #User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    if request.method == "POST":
        username = data.get("username")
        password = data.get("password")
        role = data.get("role")
        
        user = User.query.filter_by(username=username, role=role).first()
        print(user)
        if user.role == "admin":
            if not user or not check_password_hash(user.password, password):
                return jsonify({"error": "Invalid username or password"}), 401
            access_token = create_access_token(identity=user.id, additional_claims={"role": "admin"})
            return jsonify({"message": "Admin login successful", "role": "admin", "access_token": access_token}), 200
        if user:
            if not user or not check_password_hash(user.password, password):
                return jsonify({"error": "Invalid username or password"}), 401
            access_token = create_access_token(identity=user.id, additional_claims={"role": "user"})
            return jsonify({"message": "Login successful", "role": "user", "access_token": access_token}), 200

#create parking lot using jwt token
@app.route("/api/parking_lots", methods=["POST"])
@jwt_required()
def create_parking_lot():
    role = get_jwt().get("role")
    if role != "admin":
        return jsonify({"error": "Unauthorized access"}), 403
    data = request.get_json()
    
    name = data.get("name")
    city = data.get("city")
    location = data.get("location")
    total_spots = data.get("total_spots")
    price = data.get("price")
    
    parking_lot = ParkingLot(name=name, city=city, location=location, total_spots=total_spots, price=price)
    
    db.session.add(parking_lot)
    db.session.commit()
    
    for i in range(total_spots):
        parking_spot = ParkingSpot(lot_id=parking_lot.id, status='available')
        db.session.add(parking_spot)
        db.session.commit()
    
    return jsonify({"message": "Parking lot created successfully"}), 201

#update parking lot
@app.route("/api/parking_lots/<int:parkinglot_id>", methods=["PUT"])
@jwt_required()
def update_parking_lot(parkinglot_id):
    role = get_jwt().get("role")
    if role != "admin":
        return jsonify({"error": "Unauthorized access"}), 403
    data = request.get_json()
    
    name = data.get("name")
    total_spots = data.get("total_spots")
    price = data.get("price")
    
    parking_lot = ParkingLot.query.get(parkinglot_id)
    if not parking_lot:
        return jsonify({"error": "Parking lot not found"}), 404
    
    parking_lot.name = name
    parking_lot.total_spots = total_spots
    parking_lot.price = price
    
    db.session.commit()
    
    return jsonify({"message": "Parking lot updated successfully"}), 200

@app.route("/api/admin/parking_lots", methods=["GET"])
@jwt_required()
def get_admin_parking_lots():
    role = get_jwt().get("role")
    if role != "admin":
        return jsonify({"error": "Unauthorized access"}), 403
    parking_lots = ParkingLot.query.all()
    result = []
    for lot in parking_lots:
        lot_data = {
            "id": lot.id,
            "name": lot.name,
            "city": lot.city,
            "location": lot.location,
            "total_spots": lot.total_spots,
            "price": lot.price,
            "is_deleted": lot.is_deleted
        }
        result.append(lot_data)
    return jsonify(result), 200

@app.route("/api/user/parking_lots", methods=["GET"])
@jwt_required()
def get_parking_lots():
    parking_lots = ParkingLot.query.filter_by(is_deleted=False).all()
    result = []
    for lot in parking_lots:
        lot_data = {
            "id": lot.id,
            "name": lot.name,
            "city": lot.city,
            "location": lot.location,
            "total_spots": lot.total_spots,
            "price": lot.price
        }
        result.append(lot_data)
    return jsonify(result), 200

from datetime import datetime

#delete parking lot
#user reservation creation
@app.route("/api/user_reservations", methods=["POST"])
@jwt_required()
def create_reservation():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    print(data)
    
    parkingLot_id = data.get("parking_lot_id")
    vehicle_number = data.get("vehicle_number")
    start_time_str = data.get("start_time")
    end_time_str = data.get("end_time")
    start_time = datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M")    
    end_time = datetime.strptime(end_time_str, "%Y-%m-%dT%H:%M")
    
    parkingLot = ParkingLot.query.get(parkingLot_id)
    if not parkingLot:
        return jsonify({"error": "Parking lot not found"}), 404
    
    cost = parkingLot.price * ((end_time - start_time).total_seconds() / 3600)  # Calculate cost based on hours
    if parkingLot:
        spot = ParkingSpot.query.filter_by(lot_id=parkingLot_id, status='available').first()
        if not spot:
            return jsonify({"error": "No available parking spot found"}), 400
        reservation = Reservation(
            user_id=user_id, 
            spot_id=spot.id, 
            vehicle_number=vehicle_number, 
            start_time=start_time, 
            end_time=end_time, 
            cost=cost
            )
        db.session.add(reservation)
        db.session.commit()
        
        spot.status = 'reserved'
        db.session.commit()
        
        return jsonify({"message": "Reservation created successfully", "reservation_id": reservation.id}), 201
    else:
        return jsonify({"error": "Parking lot not found"}), 404
    
@app.route("/api/user_reservations", methods=["GET"])
@jwt_required()
def get_user_reservations():
    user_id = get_jwt_identity()
    reservations = Reservation.query.filter_by(user_id=user_id).all()
    result = []
    for res in reservations:
        res_data = {
            "id": res.id,
            "spot_id": res.spot_id,
            "vehicle_number": res.vehicle_number,
            "start_time": res.start_time,
            "end_time": res.end_time,
            "cost": res.cost,
            "status": res.status,
            "parking_lot_name": ParkingLot.query.get(ParkingSpot.query.get(res.spot_id).lot_id).name
        }
        result.append(res_data)
    print(result)
    return jsonify(result), 200


#user reservation update
@app.route("/api/user_reservations/<int:reservation_id>", methods=["PUT"])
@jwt_required()
def update_reservation(reservation_id):
    user_id = get_jwt_identity()
    reservation = Reservation.query.get(reservation_id)
    if not reservation or reservation.user_id != user_id:
        return jsonify({"error": "Reservation not found or unauthorized access"}), 404
    
    if reservation.status == 'completed':
        return jsonify({"error": "Completed reservations cannot be updated"}), 400
    
    if reservation.status == 'active':
        reservation.status = 'completed'
        spot = ParkingSpot.query.get(reservation.spot_id)
        spot.status = 'available'
        db.session.commit()
        return jsonify({"message": "Reservation updated successfully"}), 200
    else:
        return jsonify({"error": "Only active reservations can be updated"}), 400
    

# admin user get all reservations
@app.route("/api/admin/reservations", methods=["GET"])
@jwt_required()
# @cache.cached(timeout=60)  # Cache this route for 60 seconds
def get_admin_reservations():
    role = get_jwt().get("role")
    if role != "admin":
        return jsonify({"error": "Unauthorized access"}), 403
    reservations = Reservation.query.all()
    result = []
    for res in reservations:
        res_data = {
            "id": res.id,
            "user_id": res.user_id,
            "spot_id": res.spot_id,
            "vehicle_number": res.vehicle_number,
            "start_time": res.start_time,
            "end_time": res.end_time,
            "cost": res.cost,
            "status": res.status
        }
        result.append(res_data)
    return jsonify(result), 200



@app.route("/" , methods=["GET"])
@jwt_required()
# @cache.cached(timeout=60)  # Cache this route for 60 seconds
def user_details():
    # print(get_jwt_identity())
    user = User.query.all()
    data = []
    for u in user:
        data.append({
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role
        })
    

    return jsonify(data)




@app.route('/api/user/export_reservations', methods=['GET'])
@jwt_required()
def export_user_reservations():
    user_id = get_jwt_identity()
    
    from tasks import export_reservations
    export_reservations.delay(user_id)
    return jsonify({"message": "Reservation report sent to user"}), 200

@app.route("/api/user/summary", methods=["GET"])
@jwt_required()
def get_user_summary():
    user_id = get_jwt_identity()
    reservations = Reservation.query.filter_by(user_id=user_id).all()
    lot_summary = {}
    for res in reservations:
        parking_spot = ParkingSpot.query.get(res.spot_id)
        parking_lot = ParkingLot.query.get(parking_spot.lot_id)
        if parking_lot.name not in lot_summary:
            lot_summary[parking_lot.name] = {
                "total_reservations": 0,
                "total_cost": 0.0
            }
        lot_summary[parking_lot.name]["total_reservations"] += 1
        lot_summary[parking_lot.name]["total_cost"] += res.cost
        
    lot_names = []
    lot_counts = []
    lot_costs = []
    for lot_name, summary in lot_summary.items():
        lot_names.append(lot_name)
        lot_counts.append(summary["total_reservations"])
        lot_costs.append(summary["total_cost"])

    total_spent = sum(summary["total_cost"] for summary in lot_summary.values())
    active_reservations = sum(1 for res in reservations if res.status == "active")
    completed_reservations = sum(1 for res in reservations if res.status == "completed")    
    
    return jsonify({
        "lot_names": lot_names,
        "lot_counts": lot_counts,
        "lot_costs": lot_costs,
        "total_spent": total_spent,
        "active_reservations": active_reservations,
        "completed_reservations": completed_reservations,
        "total_reservations": len(reservations)
    })
    

if __name__ == "__main__":
    
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(username="admin", email="admin@gmail.com", password=generate_password_hash("admin123"), role="admin")
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)
    