from flask import Flask 
import time 
from flask_caching import Cache

app = Flask(__name__)

app.config.from_mapping({
    "CACHE_TYPE":"RedisCache",
    "CACHE_REDIS_HOST": "localhost",
    "CACHE_REDIS_PORT": 6379,
    "CACHE_REDIS_DB": 0,
    # "CACHE_REDIS_URL": "redis://localhost:6379/1",
    "CACHE_DEFAULT_TIMEOUT": 50, 
})

cache = Cache(app)

# flask_cache_ + view/ + url()
# cache.init_app(app)

@app.route("/home")
@cache.cached(key_prefix="home")
def home():
    time.sleep(5)
    return f"Home generated at {time.time()}"

@app.route("/square/<int:num>")
@cache.memoize(timeout=120)
def square(num):
    time.sleep(2)  # Simulating heavy work
    return f"Square of {num} is {num * num}"

@app.route("/clear-cache")
def clear_cache():
    cache.clear()
    return "All cache cleared!"

@app.route("/delete")
def delete_homepage_cache():
    cache.delete("home")
    return "Homepage cache deleted!"


app.run(debug=True)