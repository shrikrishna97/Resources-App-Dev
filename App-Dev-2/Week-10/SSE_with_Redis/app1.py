from flask_sse import sse

from flask import Flask, render_template, request, jsonify
import redis

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost:6379/1"

app.register_blueprint(sse, url_prefix='/stream')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_notification', methods=['POST'])
def notify():
    data = request.get_json()
    message = data.get('message')
    
    if not message:
        return jsonify({"status": "error", "message": "No message provided"}), 400
    
    # Publish the message to Redis
    # sse = redis.from_url(app.config["REDIS_URL"])
    with app.app_context():
        sse.publish({"message": message}, type='notify')
    
    return jsonify({"status": "Message sent"})

if __name__ == "__main__":
    app.run(debug=True)