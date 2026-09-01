from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from datetime import datetime, timedelta


app = Flask(__name__)

CORS(app, supports_credentials=True, origins="*")

@app.route("/set-cookie")
def set_cookie():
    
    resp = make_response(jsonify({"message": "Cookie is set!"}))
    
    print(resp)
    
    resp.set_cookie(
        "user_token",
        "abc123",
        # samesite="Strict",
        httponly=True,
        # expires=datetime.utcnow() + timedelta(minutes=1),
        max_age=10,
        # Works locally for cross-site cookies
    )
    return resp

@app.route("/get-cookie")
def get_cookie():
    token = request.cookies.get("user_token")
    print(token)
    if token:
        return jsonify({"message": "Cookie retrieved!", "token": token})
    return jsonify({"message": "No cookie found!"}), 404

if __name__ == "__main__":
    app.run(debug=True)