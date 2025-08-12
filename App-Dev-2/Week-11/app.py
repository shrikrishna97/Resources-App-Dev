from flask import Flask, make_response, render_template
from flask_caching import Cache, CachedResponse
import time

app = Flask(__name__)

# Config from Flask documentation style
app.config.from_mapping({
    "CACHE_TYPE": "RedisCache",
    "CACHE_REDIS_HOST": "localhost",
    "CACHE_REDIS_PORT": 6379,
    "CACHE_REDIS_DB": 0,
    "CACHE_REDIS_URL": "redis://localhost:6379/0",
    "CACHE_DEFAULT_TIMEOUT": 60,
    "CACHE_KEY_PREFIX": "flask_cache_",
})

cache = Cache(app)


# Cached full route with key_prefix
@app.route("/")
@cache.cached(timeout=30, key_prefix="homepage")
def home():
    time.sleep(5)
    return f"Home generated at {time.time()}"

# Memoized function result (different for each number)
@app.route("/square/<int:num>")
@cache.memoize(timeout=60)
def square(num):
    time.sleep(2)  # Simulating heavy work
    return f"Square of {num} is {num * num}"

# Clear all cache
@app.route("/clear-cache")
def clear_cache():
    cache.clear()
    return "All cache cleared!"

# Delete only homepage cache
@app.route("/delete-homepage-cache")
def delete_homepage_cache():
    cache.delete("homepage")
    return "Homepage cache deleted!"

app.run(debug=True)