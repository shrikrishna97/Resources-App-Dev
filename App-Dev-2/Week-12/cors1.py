from flask import Flask, jsonify, request, make_response
from flask_cors import CORS

app = Flask(__name__)

# CORS(app, origins=["http://127.0.0.1:5500", "http://localhost:5500"] , supports_credentials=True)

# CORS(app, origins="*", supports_credentials=True)
CORS(app, supports_credentials=True)

@app.route("/set-cookie")
def set_cookie():
    resp = make_response(jsonify({"message": "Cookie is set!"}))
    resp.set_cookie(
        "some_token",
        "abc123",
        # max_age=10,
        # expires=
        # httponly=True,  # JS cannot read this cookie
        # samesite="Strict" 
        secure=True,     # True in production with HTTPS
        samesite="None"
        # Works locally for cross-site cookies
    )
    return resp
@app.route("/get-cookie")
def get_cookie():
    token = request.cookies.get("some_token")
    return jsonify({"token": token})  
    


if __name__ == "__main__":
    app.run(debug=True)