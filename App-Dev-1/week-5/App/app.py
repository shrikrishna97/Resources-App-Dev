from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

appp = Flask(__name__)

appp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///first.sqlite3'

db = SQLAlchemy(appp)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    
with appp.app_context():  
    db.create_all()   

# appp.app_context().push() 

@appp.route('/create_user')
def create_user():
    user = User(username="admin", password="admin",email="admin@g.com")
    # db.session.add(User(username="admin", password="admin",email="admin@g.com"))
    db.session.add(user)
    db.session.commit()
    return "user created"

@appp.route("/get_users")
def get_users():
    users = User.query.all()
    # User.query.filter_by(username="admin").first()
    # User.query.filter_by(username="admin").first_or_404()
    # User.query.filter_by(username="admin").first_or_404(description="User not found")
    # User.query.filter_by(username="admin").all()
    # User.query.filter_by(username="admin").filter_by(email="admin@g.com").all()
    print(users)
    return render_template("happy.html", users=users, users_details=users)
 
@appp.route('/delete_user/<int:user_id>') 
def delete_user(user_id):
    
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return "user deleted"
    return "user not found"

@appp.route('/update_user/<int:user_id>')
def update_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.username = "admin1"
        db.session.commit()
        return "user updated"
    return "user not found"
    
@appp.route('/') #base url 
def hello_world():
    return 'Hello World! hi wo'

@appp.route('/hello') #
def hello():
    users =[
        {'username': "hi",'password': "123"}, #row 1
            {'username': "world"}, 
            {'username': "hello"}
            ]
    return render_template('happy.html', users=users )

if __name__ == '__main__':
    appp.run(debug=True)
