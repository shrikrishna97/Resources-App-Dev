from flask import Flask
from flask_caching import Cache
import time 

app = Flask(__name__)

app.config.from_mapping({
    "CACHE_TYPE": "RedisCache",
    "CACHE_REDIS_HOST": "localhost",
    "CACHE_REDIS_PORT": 6379,
    "CACHE_REDIS_DB": 0,
    # "CACHE_REDIS_URL": "redis://localhost:6379/0",
    # "CACHE_DEFAULT_TIMEOUT": 60
    "CACHE_KEY_PREFIX": "myapp_"
})

cache = Cache(app)

@app.route("/home")
@cache.cached(timeout=60 , key_prefix="home")
def home():
    time.sleep(5)
    return f"Home generated at {time.time()}"
@app.route("/homepage")
@cache.cached(timeout=60 , key_prefix="homepage")
def homepage():
    return "Welcome"

@app.route("/delete-homepage-cache")
def delete_homepage_cache():
    cache.delete("home")
    return "Homepage cache deleted!"

@app.route("/square/<int:num>")
@cache.memoize(timeout=90)
def square(num):
    time.sleep(2)  # Simulating heavy work
    return f"Square of {num} is {num * num}"

@app.route("/clear-cache")
def clear_cache():
    cache.clear()
    return "All cache cleared!"


if __name__ == "__main__":
    app.run(debug=True)