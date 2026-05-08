# Topic 8 – Flask Caching: @cache.cached vs @cache.memoize
# Run: python backend/08-caching.py
# Test cached view:   GET http://127.0.0.1:5000/home         (watch terminal — only prints on 1st call)
# Test memoize:       GET http://127.0.0.1:5000/report/1/2024
# Clear memoize:   DELETE http://127.0.0.1:5000/report/1/2024

from flask import Flask, jsonify
from flask_caching import Cache

app = Flask(__name__)

# SimpleCache = in-memory, single-process (dev only)
# For production: CACHE_TYPE = 'RedisCache', CACHE_REDIS_URL = 'redis://localhost:6379/0'
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
cache = Cache(app)

# @cache.cached — caches entire view, key = request URL
@app.get('/home')
@cache.cached(timeout=60)
def home():
    print("home() actually ran")   # only prints on first call, then cached
    return jsonify(msg="Home page data")

# @cache.memoize — caches per argument combination
@cache.memoize(timeout=120)
def get_user_report(user_id, year):
    print(f"Computing report for user={user_id}, year={year}")
    # Expensive DB query / calculation here
    return {'user_id': user_id, 'year': year, 'sales': user_id * year}

@app.get('/report/<int:user_id>/<int:year>')
def report(user_id, year):
    data = get_user_report(user_id, year)   # cached per (user_id, year) combo
    return jsonify(data)

# Manually clear a memoized result (e.g. after data changes)
@app.delete('/report/<int:user_id>/<int:year>')
def clear_report(user_id, year):
    cache.delete_memoized(get_user_report, user_id, year)
    return jsonify(msg="Cache cleared")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
