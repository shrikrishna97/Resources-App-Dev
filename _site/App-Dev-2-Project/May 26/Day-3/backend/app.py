from flask import Flask , jsonify, request
from flask_cors import CORS
from model import db , User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SECRET_KEY"] = "your-secret-key"

app.config["JWT_SECRET_KEY"] = "your-key"

CORS(app)

JWTManager(app)


db.init_app(app)


@app.route("/register" , methods=["GET" , "POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    if request.method == "POST":
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


@app.route("/" , methods=["GET"])
@jwt_required()
def home():
    print(get_jwt_identity())
    data = {"numbers" : [1, 2, 3, 4, 5], 
            "message" : "Hello, World!"}
    return jsonify(data, 200) 


if __name__ == "__main__":
    
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(username="admin", email="admin@gmail.com", password=generate_password_hash("admin123"), role="admin")
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)
    