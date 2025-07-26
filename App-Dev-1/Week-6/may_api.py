from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)
api = Api(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

with app.app_context():
    db.create_all()

class User(Resource):
    def get(self, user_id):
        user = UserModel.query.get(user_id)
        if user:
            return jsonify({"id": user.id, "name": user.name, "email": user.email})
        return jsonify({"message": "User not found"})

    def post(self, user_id):
        data = request.get_json()
        user = UserModel(id=user_id, name=data['name'], email=data['email'])
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User added", "data": data})

    def put(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"})
        data = request.get_json()
        user.id = data.get('id', user.id)
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        db.session.commit()
        return jsonify({"message": "User updated", "data": {"name": user.name, "email": user.email}})

    def delete(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"})
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"})

api.add_resource(User, '/user/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)