from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, get_jwt, current_user
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "your-secret-key"  # Change this in production!
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
# from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin

db = SQLAlchemy(app)
jwt = JWTManager(app)
app.app_context().push()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")

@jwt.user_identity_loader
def load(user):
    return user.username

@jwt.user_lookup_loader
def user_lookup(jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(username=identity).one_or_none()

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    print(data)
    
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"msg": "Username already exists"}), 400
    
    new_user = User(username=data["username"], password=data["password"], role=data.get("role", "user"))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User registered successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"], password=data["password"]).first()
    if not user:
        return jsonify({"msg": "Invalid credentials"}), 401

    # access_token = create_access_token(identity=user.username , additional_claims={"role": user.role}) # this is for using get_jwt_identity() to get username and get_jwt() to get role
    access_token = create_access_token(identity=user) # if we want to use current_user then we have to give object to the identity
    return jsonify(access_token=access_token), 200

@app.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()
    claims = get_jwt()
    role = claims.get("role", "user")
    
    roles = get_jwt().get("role")
    current_user = current_user.id
    
    return jsonify(logged_in_as=current_user, role=role, roles = roles), 200
@app.route("/check_user", methods=["GET"]) # this will work for current_user
@jwt_required()
def check_current_user():
    user = current_user.username # we have give any other variable name other than current_user to use it
    return jsonify(logged_in_as=user), 200
    

@app.route("/admin", methods=["GET"])
@jwt_required()
def admin():
    role = get_jwt().get("role", "user")
    if role != "admin":
        return jsonify({"msg": "Admins only!"}), 403
    return jsonify({"msg": "Welcome, admin!"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)    