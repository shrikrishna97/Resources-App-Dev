from flask import Flask, render_template, request, jsonify, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
import random

app = Flask(__name__)
app.secret_key = "secret123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
api = Api(app)


# ------------------ Model ------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()


# ------------------ API Resources ------------------
class SignupAPI(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if User.query.filter_by(username=username).first():
            return {"status": "error", "message": "Username already exists"}, 400

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return {"status": "success", "message": "User registered successfully"}, 201


class LoginAPI(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username, password=password).first()
        if not user:
            return {"status": "error", "message": "Invalid username or password"}, 401

        session["user"] = username
        if password == "1234":
            # Need CAPTCHA
            a, b = random.randint(1, 9), random.randint(1, 9)
            session["captcha_answer"] = str(a + b)
            return {
                "status": "captcha_required",
                "question": f"{a} + {b}",
            }
        return {"status": "success", "message": "Login successful"}


class CaptchaAPI(Resource):
    def post(self):
        data = request.get_json()
        answer = data.get("answer")
        correct = session.get("captcha_answer")

        if answer == correct:
            return {"status": "success", "message": "CAPTCHA passed"}
        else:
            return {"status": "error", "message": "Incorrect CAPTCHA"}, 400


# Register APIs
api.add_resource(SignupAPI, "/api/signup")
api.add_resource(LoginAPI, "/api/login")
api.add_resource(CaptchaAPI, "/api/captcha")


# ------------------ Frontend Routes ------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return render_template("index.html")
        # return redirect("/")
    return render_template("dashboard.html", user=session["user"])

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
