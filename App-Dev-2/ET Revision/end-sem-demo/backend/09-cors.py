# Topic 9 – CORS: Frontend to Backend Access Control
# Run: python backend/09-cors.py
# Open frontend/09-cors.html in browser — check DevTools > Network > Response Headers
# to see Access-Control-Allow-Origin on each response.

from flask import Flask, jsonify, make_response
from flask_cors import CORS

app = Flask(__name__)

# Dev: allow all origins
# CORS(app)

# Production: restrict to specific origin
CORS(app, resources={r"/api/*": {
    "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
    "methods": ["GET", "POST", "PUT", "DELETE"],
    "allow_headers": ["Content-Type", "Authorization"]
}})

# ── Via flask-cors (header added automatically) ───────────
@app.get('/api/data')
def api_data():
    return jsonify(data="Hello from /api/data — CORS via flask-cors")

# ── Manual: make_response + set header explicitly ─────────
@app.get('/api/manual')
def api_manual():
    resp = make_response(jsonify(data="Hello from /api/manual"), 200)   # 200 = status code
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    return resp

# ── Inline: return (body, status_code, headers_dict) tuple ──
@app.get('/api/hello')
def api_hello():
    return jsonify(msg="Hello from /api/hello"), 200, {'Access-Control-Allow-Origin': 'http://localhost:5173'}

# ── Preflight OPTIONS handler (for PUT/DELETE/custom headers) ──
@app.route('/api/manual', methods=['OPTIONS'])
def preflight():
    resp = make_response('', 204)
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return resp

if __name__ == '__main__':
    app.run(debug=True, port=5000)
