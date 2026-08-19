from flask import Flask, request, jsonify
from flask_cors import CORS




app = Flask(__name__)

CORS(app)

notes = [
    {
        "id": 1,
        "title": "Learn Flask",
        "content": "Create REST APIs"
    },
    {
        "id": 2,
        "title": "Learn Vue",
        "content": "Use Vue CDN"
    }
]


@app.route('/api/data', methods=['GET'])
def get_data():
    # users = User.query.all()
    # data = {
    #     'message': 'Hello from the backend',
    #     'items': [1, 2, 3, 4, 5]
    #     }
    # return jsonify(data)
    # return json.dumps(data)
    return notes

@app.route('/api/data', methods=['POST'])
def add_note():
    new_note = request.json
    print(new_note)  # Debugging line to check the received data
    new_note1 = request.get_json()
    print(new_note1)
    notes.append(new_note)
    return jsonify(new_note), 201


if __name__ == '__main__':
    app.run(debug=True)