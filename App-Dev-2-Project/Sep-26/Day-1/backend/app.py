from flask import Flask, jsonify, request
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)
# jwt = JWTManager()
# jwt.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)
    

@app.route('/admin/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    # Process the login data
    if user and check_password_hash(user.password, data.get('password')) and user.role == 'admin':
        access_token = create_access_token(identity=user.id, additional_claims={'role': user.role})
        return jsonify({'message': 'Login successful', 'status': 'success', 'access_token': access_token})
    if data.get('password') != 'admin123' and data.get('role') != 'user':
        return jsonify({'message': 'Invalid credentials', 'status': 'error'})
    return jsonify({'message': 'Not authorized', 'status': 'success'})

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