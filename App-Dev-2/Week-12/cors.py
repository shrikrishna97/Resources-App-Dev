from flask import Flask, jsonify, request, make_response
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS with credentials support
# CORS(app, supports_credentials=True, origins=["http://127.0.0.1:5500", "http://localhost:5500"])
# CORS(app, supports_credentials=True, origins="*")
CORS(app, supports_credentials=True)


@app.route("/set-cookie")
def set_cookie():
    resp = make_response(jsonify({"message": "Cookie is set!"}))
    resp.set_cookie(
        "user_token",
        "abc123",
        # max_age=10, # seconds
        # expires=datetime.utcnow() + timedelta(minutes=1) # deletes in 1 minute
        # httponly=True,    # JS cannot read this cookie
        # secure=True,     # True in production with HTTPS
        # secure=True,
        # samesite=None,
        samesite="Strict"    # Works locally for cross-site cookies
    )
    return resp

@app.route("/get-cookie")
def get_cookie():
    token = request.cookies.get("user_token")
    if token:
        return jsonify({"message": "Cookie retrieved!", "token": token})
    return jsonify({"message": "No cookie found!"}), 404

@app.route("/delete-cookie")
def delete_cookie():
    resp = make_response({"msg": "Cookie deleted"})
    resp.delete_cookie("user_token")
    return resp


if __name__ == "__main__":
    app.run(debug=True)