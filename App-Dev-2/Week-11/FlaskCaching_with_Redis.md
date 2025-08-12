---

# **Complete Beginner’s Guide: Flask-Caching with Redis**

---

## **1. Why Do We Need Caching?**

Imagine a Flask route that:

* Fetches large amounts of data from a database, **or**
* Does heavy calculations.

If 100 users request that route at the same time:

* **Without caching** → Flask recomputes 100 times → slow, high CPU usage.
* **With caching** → Flask computes once, stores the result in memory (Redis), and instantly serves the cached result to the next 99 users.

---

## **2. Our Solution**

We will:

* Use **Redis** as our cache store (fast, in-memory, key-value database).
* Use **Flask-Caching** to integrate Redis into Flask.
* Learn two techniques:

  1. **`@cache.cached`** – Cache full route responses.
  2. **`@cache.memoize`** – Cache function results based on arguments.

---

## **3. Step-by-Step Setup**

### **3.1 Install Python packages**

```bash
pip install flask flask-caching redis
```

---

### **3.2 Install Redis**

⚠ **Windows Users** – Redis latest version isn’t supported natively. Use **WSL (Windows Subsystem for Linux)**.

#### **Linux / Ubuntu / WSL**

```bash
sudo apt update
sudo apt install redis-server
```

#### **macOS**

```bash
brew install redis
```

---

### **3.3 Start Redis Server**

```bash
redis-server
```

Check if it’s working:

```bash
redis-cli ping
```

Output:

```
PONG
```

---

### **3.4 Install RedisInsight (Optional, for Viewing Cache Data)**

1. Visit **[https://redis.io/insight/](https://redis.io/insight/)**
2. Fill **Name, Email, Organization** to download.
3. Install and run RedisInsight.
4. Click **Add Redis Database**:

   * Host: `localhost`
   * Port: `6379`
5. Connect → You can now see keys & values.

---

## **4. Understanding `@cache.cached` and Key Prefixes**

### **4.1 What `@cache.cached` Does**

* Stores the **entire HTML response** of a route.
* Perfect for static or slow-changing pages.
* Returns the cached page instantly until it expires.

### **4.2 Why Key Prefixes?**

Without a prefix, two routes might accidentally generate the same cache key.
Example:

* `/` → might store as `view//`
* Another unrelated route could overwrite it.

With a prefix:

```python
@cache.cached(timeout=30, key_prefix="homepage")
```

The Redis key will start with `homepage`, avoiding conflicts.

---

## **5. Understanding `@cache.memoize` and Key Prefixes**

### **5.1 Why Not Use `@cached` for Everything?**

`@cached` ignores function arguments — meaning:

* `/square/4` and `/square/5` could use the same cache entry — wrong results.

### **5.2 How `@memoize` Solves It**

`@memoize` automatically includes **function arguments** in the cache key.

* `/square/4` gets one cache entry.
* `/square/5` gets another.

### **5.3 Key Prefix with Memoize**

You can group memoized entries with a prefix:

```python
@cache.memoize(timeout=60)
def get_data(id):
    ...
```

Keys will be like:

```
flask_cache_memoize:get_data:args
```

---

## **6. Clearing and Deleting Cache Items**

Sometimes, you don’t want to wait for the timeout to expire — maybe the data has changed, and you need to refresh the cache immediately.

### **6.1 `cache.clear()`**

* Removes **all cache entries** from Redis for your app.
* Useful for a “Clear Cache” admin button.
* **Warning**: This wipes everything — both `@cached` and `@memoize` entries.

```python
@app.route("/clear-cache")
def clear_cache():
    cache.clear()
    return "All cache cleared!"
```

---

### **6.2 `cache.delete(key)`**

* Deletes **a specific cache key**.
* Useful if you know exactly what you want to remove.

Example: removing the cache for the homepage route:

```python
@app.route("/delete-homepage-cache")
def delete_homepage_cache():
    cache.delete("homepage")
    return "Homepage cache deleted!"
```

---

💡 **Tip**: To find the key name, check RedisInsight or know your `key_prefix` / function signature.

---

## **7. Full Working Flask App**

```python
from flask import Flask
from flask_caching import Cache
import time

app = Flask(__name__)

# Config from Flask documentation style
app.config.from_mapping({
    "CACHE_TYPE": "RedisCache",
    "CACHE_REDIS_HOST": "localhost",
    "CACHE_REDIS_PORT": 6379,
    "CACHE_REDIS_DB": 0,
    "CACHE_REDIS_URL": "redis://localhost:6379/0",
    "CACHE_DEFAULT_TIMEOUT": 60
})

cache = Cache(app)

# Cached full route with key_prefix
@app.route("/")
@cache.cached(timeout=30, key_prefix="homepage")
def home():
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
```

---

## **8. Running the App**

### **Linux / macOS / Windows WSL**

```bash
python app.py 
# OR
python3 app.py
```

---

## **9. Viewing Cached Keys in RedisInsight**

You might see:

```
homepage                         -> cached HTML for "/"
flask_cache_memoize:square:4     -> result for square(4)
flask_cache_memoize:square:5     -> result for square(5)
```

* **Keys**: strings (names of cached items).
* **Values**: binary data (Python pickled objects).

---

## **10. Before vs After Caching — Example**

### **Without Caching:**

```text
GET /square/5  -> 2.002 seconds
GET /square/5  -> 2.004 seconds
```

Every request runs the heavy computation.

### **With Caching:**

```text
GET /square/5  -> 2.001 seconds   (first run, cache miss)
GET /square/5  -> 0.001 seconds   (second run, cache hit)
```

**Result:** Instant response after first computation.

---

## **11. Logic Flow Diagram**

```
[Browser Request]
        |
        v
   [Flask App]
        |
        v
[Check Redis Cache] -----> (Cache Hit) ---> [Return Cached Response]
        |
    (Cache Miss)
        |
        v
 [Run Actual Code]
        |
        v
 [Store in Redis]
        |
        v
[Send Response to Browser]
```

---

## **12. Summary & Best Practices**

* **`@cached`** – Use for whole route caching (static pages).
* **`@memoize`** – Use for caching function results per argument.
* **`cache.clear()`** – Wipes all cache entries.
* **`cache.delete(key)`** – Deletes a specific cache key.
* **Key Prefix** – Avoids overwriting unrelated cache entries.
* **Timeout** – Always set reasonable cache expiry to avoid stale data.
* Use **RedisInsight** for easy debugging.
* Cache only **expensive computations or slow-changing data**.

---

## 🛠 **Extra Notes — Stopping and Restarting Redis**

When running Flask with Redis caching, you might get:

```
Could not create server TCP listening socket *:6379: bind: Address already in use
```

This means **Redis is already running** on port `6379`.

### **Check if Redis is running**

```bash
redis-cli ping
```

If it returns:

```
PONG
```

then Redis is already running — no need to start it again.

---

### **Graceful shutdown (preferred)**

```bash
redis-cli shutdown
```

Safely closes Redis and saves data if persistence is enabled.

---

### **Using systemd (Linux, WSL with systemd)**

```bash
sudo systemctl stop redis
sudo systemctl status redis  # check status
```

---

### **Older SysV init systems**

```bash
sudo service redis-server stop
# or
sudo /etc/init.d/redis-server stop
```

---

### **Kill by PID**

```bash
ps aux | grep '[r]edis-server'   # find PID
sudo kill <PID>                  # gentle
sudo kill -9 <PID>               # force
```

**One-liner:**

```bash
sudo kill -9 $(ps -ef | grep '[r]edis-server' | awk '{print $2}')
```

---

### **Kill by Port**

```bash
sudo lsof -i :6379               # find PID using port 6379
sudo kill -9 $(sudo lsof -t -i:6379)
# or
sudo fuser -k 6379/tcp
```

---

### **pkill shortcut**

```bash
sudo pkill -f redis-server
# or
sudo pkill redis-server
```

---

### **If running in Docker**

```bash
docker ps                       # find container id
docker stop <container_id>      # graceful
docker kill <container_id>      # immediate
```

---

**Recommendation:** Always try `redis-cli shutdown` or `systemctl stop redis` before using `kill -9` or `pkill`.
Brute-force killing can cause data loss if persistence is enabled.

---