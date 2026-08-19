from flask import Flask , jsonify
from model import db , User


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SECRET_KEY"] = "your-secret-key"

app.config["JWT_SECRET_KEY"] = "your-key"

db.init_app(app)


@app.route("/register" , methods=["GET" , "POST"])
def register():
    pass
@app.route("/" , methods=["GET"])
def home():
    data = {"numbers" : [1, 2, 3, 4, 5], 
            "message" : "Hello, World!"}
    return jsonify(data, 200) 


if __name__ == "__main__":
    
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(username="admin", email="admin@gmail.com", password="admin123", role="admin")
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)
    