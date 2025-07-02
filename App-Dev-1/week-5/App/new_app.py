from flask import Flask,render_template

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///week5.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)



# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/')
def home():
    db.create_all()  # Create the database tables
    
    db.session.add(User(username='testtuser', email='VetHwA@example.com'))
    db.session.commit()  # Commit the changes
    return 'Welcome to the Flask App!'

@app.route('/users')
def list_users():
    users = User.query.all()
    # print(users[0].username, users[0].email)
    # print("hi")
    return render_template('happy.html', users=users)
    
if __name__ == '__main__':
    app.run(debug=True)
