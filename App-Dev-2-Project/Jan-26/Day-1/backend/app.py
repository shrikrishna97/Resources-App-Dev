from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route('/', methods=['GET'])
def get_data():
    
    data = {
        'message': 'Hello from the backend!',
        'items': [1, 2, 3, 4, 5]
    }
    return jsonify(data)


app.run(debug=True)
