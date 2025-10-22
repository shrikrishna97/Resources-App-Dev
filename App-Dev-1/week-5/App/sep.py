from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sep.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)

with app.app_context():
    db.create_all()
    
# OR    
# You push and pop the app context manually
# app.app_context().push() to create the context
# app.app_context().pop() to remove the context
# but this is not recommended way use "with" statement instead that automatically pushes and pops the context    


@app.route('/names')
def home():
    
    db.session.add(User(id=3, username="testuser"))
    db.session.add(User(username="seconduser"))
    
    db.session.commit()
    
    
    return 'Welcome to the Flask App!'      

from flask import render_template

@app.route('/all_users')
def all_users():
    users = User.query.all()
    userss = User.query.filter_by(username='testuser').first()
    return render_template('index.html', name="User List", items=[user.username for user in users])

@app.route('/items')
def items():
    return render_template('index.html', items=["Apple", "Banana", "Cherry"])   

if __name__ == '__main__':            
    app.run(debug=True)    