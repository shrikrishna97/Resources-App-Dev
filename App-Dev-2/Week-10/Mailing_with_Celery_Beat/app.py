from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from models import db, User, BookRequest



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()
    
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')   
    password = data.get('password')
    email = data.get('email')
    role = data.get('role')
    new_user = User(username=username, password=password, email=email, role=role)
    db.session.add(new_user)
    db.session.commit()
    return "User registered successfully", 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if not user:
        return jsonify({'msg': 'Invalid credentials'}), 401
    token = create_access_token(identity=user.id, additional_claims={'role': user.role})
    return jsonify({'access_token': token}), 200  

@app.route('/request-book', methods=['POST'])
@jwt_required()
def request_book():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    book_name = data.get('book_name')
    new_request = BookRequest(user_id=current_user_id, book_name=book_name)
    db.session.add(new_request)
    db.session.commit()
    return "Book request submitted", 201    

@app.route('/export-report', methods=['POST'])
@jwt_required()
def export_report():
    user_id = get_jwt_identity()
    from tasks import generate_user_report
    
    task_id = generate_user_report.delay(user_id)
    print(f"Task ID: {task_id}")
    
    
    return jsonify({'msg': 'Report is being generated. You will receive it via email.'}), 200




if __name__ == '__main__':
    app.run(debug=True)