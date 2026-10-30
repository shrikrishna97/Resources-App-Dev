from flask import Flask, jsonify, request
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_cors import CORS


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)
# jwt = JWTManager()
# jwt.init_app(app)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)
    

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

@app.route('/api/data', methods=['GET'])
@jwt_required()
def get_data():
    data = {
        'message': 'Hello, World!',
        'status': 'success'
    }
    # return data
    return jsonify(data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(role='admin').first():
            admin_user = User(username='admin',email="admin@gmail.com",password=generate_password_hash('admin123'), role='admin')
            db.session.add(admin_user)
            db.session.commit()
    app.run(debug=True)