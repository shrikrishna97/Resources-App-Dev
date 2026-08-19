# Topic 10 – Cookies: Use Cases
# Run: python backend/10-cookies.py
# Open frontend/10-cookies.html (served from http://localhost:5173) in browser.
# Use DevTools > Application > Cookies to watch cookies being set/deleted.

from flask import Flask, jsonify, make_response, request
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'demo-secret'

CORS(app, resources={r"/cookie/*": {
    "origins": ["http://localhost:5173", "http://127.0.0.1:5173",
                "http://localhost:5500", "http://127.0.0.1:5500"],
    "supports_credentials": True,
}})

@app.get('/cookie/set')
def set_cookie():
    resp = make_response(jsonify(msg="Cookie set"))
    resp.set_cookie(
        'user_pref', 'dark_mode',
        max_age=60 * 60 * 24 * 7,   # 7 days
        httponly=True,               # JS cannot read → blocks XSS theft
        secure=False,                # False for localhost HTTP demo (True in prod)
        samesite='Lax',              # CSRF protection
        path='/'
    )
    return resp

@app.get('/cookie/read')
def read_cookie():
    return jsonify(preference=request.cookies.get('user_pref', 'light_mode'))

@app.get('/cookie/delete')
def delete_cookie():
    resp = make_response(jsonify(msg="Cookie deleted"))
    resp.delete_cookie('user_pref', path='/')
    return resp

# Subdomain sharing example (reference — needs a real domain, not localhost):
# resp.set_cookie('auth_token', 'abc123',
#     domain='.y.com',   # leading dot = all subdomains share this cookie
#     httponly=True, secure=True, samesite='Lax')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
