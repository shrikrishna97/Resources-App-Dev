from flask import Flask, jsonify, request

app = Flask(__name__)

users = {"1": {"name": "Alice", "email": "alice@example.com"}}

@app.route('/user/<string:user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify(users.get(user_id, "User not found"))

@app.route('/user/<string:user_id>', methods=['POST'])
def create_user(user_id):
    print(request.json)
    if request.json:
        users[user_id] = request.json
        return jsonify({"message": "User added", "data": users[user_id]}),201
    else:
        return jsonify({"message": "User id not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)