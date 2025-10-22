from flask import Flask,render_template

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///week5.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    classes = db.relationship('Class', backref='creator', lazy=True)

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
with app.app_context():
    db.create_all()
    
# OR    
# You push and pop the app context manually
# app.app_context().push() to create the context
# app.app_context().pop() to remove the context
# but this is not recommended way use "with" statement instead that automatically pushes and pops the context

@app.route('/')
def home():
    # db.create_all()  # Create the database tables
    
    db.session.add(User(username='testtuser', email='VetHwA@example.com'))
    db.session.commit()  # Commit the changes
    return 'Welcome to the Flask App!'

@app.route('/users')
def list_users():
    users = User.query.all()
    # user = User.query.get(1)
    user = User.query.filter_by(username='testtuser').first()
    user.id = 3
    # db.session.delete(user)
    db.session.commit()
    # print(user)
    # print(users[0].username, users[0].email)
    # print("hi")
    return render_template('happy.html', users=users, user=user)
    
if __name__ == '__main__':
    app.run(debug=True)
