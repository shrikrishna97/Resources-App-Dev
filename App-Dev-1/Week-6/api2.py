from flask import Flask, Response, request
import json

app = Flask(__name__)

users = {"1": {"name": "Alice", "email": "alice@example.com"}}

@app.route('/user/<string:user_id>', methods=['GET'])
def get_user(user_id):
    response = json.dumps(users.get(user_id, {"error": "User not found"}))
    return Response(response, status=200, mimetype='application/json')

@app.route('/user/<string:user_id>', methods=['POST'])
def create_user(user_id):
    users[user_id] = request.json
    response = json.dumps({"message": "User added", "data": users[user_id]})
    return Response(response, status=201, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)
