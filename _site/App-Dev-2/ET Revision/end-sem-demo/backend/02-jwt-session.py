# Topic 2 – JWT vs Session-Based Authentication
# Run: python backend/02-jwt-session.py
# Test JWT login:     POST http://127.0.0.1:5000/auth/jwt/login   {"email":"alice@example.com","password":"alice123"}
# Test Session login: POST http://127.0.0.1:5000/auth/session/login {"email":"alice@example.com","password":"alice123"}

from flask import Flask, jsonify, request, session
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'demo-jwt-secret'
app.config['SECRET_KEY'] = 'demo-session-secret'
JWTManager(app)

# Simulated user DB
USERS = {
    'alice@example.com': {'id': 1, 'password': 'alice123'},
    'bob@example.com':   {'id': 2, 'password': 'bob123'},
}

# ── JWT ──────────────────────────────────────────────────

@app.post('/auth/jwt/login')
def jwt_login():
    body = request.get_json(silent=True) or {}
    user = USERS.get(body.get('email'))
    if not user or user['password'] != body.get('password'):
        return jsonify(msg="Bad credentials"), 401
    token = create_access_token(identity=str(user['id']))
    return jsonify(access_token=token)

@app.get('/auth/jwt/profile')
@jwt_required()
def jwt_profile():
    user_id = get_jwt_identity()   # decoded from token — no DB hit
    return jsonify(user_id=int(user_id))

# ── Session ───────────────────────────────────────────────

@app.post('/auth/session/login')
def session_login():
    body = request.get_json(silent=True) or {}
    user = USERS.get(body.get('email'))
    if not user or user['password'] != body.get('password'):
        return jsonify(msg="Bad credentials"), 401
    session['user_id'] = user['id']   # stored server-side
    return jsonify(msg="Logged in", user_id=user['id'])

@app.get('/auth/session/profile')
def session_profile():
    if 'user_id' not in session:
        return jsonify(msg="Not logged in"), 401
    return jsonify(user_id=session['user_id'])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
