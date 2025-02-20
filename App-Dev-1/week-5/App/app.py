from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

appp = Flask(__name__)

appp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///first.sqlite3'

db = SQLAlchemy(appp)

# from model import User, Profile, db

# db.init_app(appp)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     profile = db.relationship('Profile', backref='User', uselist=False, cascade="all, delete-orphan")

# class Profile(db.Model):

#     id = db.Column(db.Integer, primary_key=True)
#     bio = db.Column(db.String(200))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     # classes = db.relationship('Class', backref='creator', lazy=True)
#     classes = db.relationship('Class', back_populates='student')
    

# class Class(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     student = db.relationship('User', back_populates='classes')

class_participants = db.Table('class_participants',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('class_id', db.Integer, db.ForeignKey('class.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # classes = db.relationship('Class', backref='student', lazy=True)
    # classes = db.relationship('Class', back_populates='student')
    classes = db.relationship('Class', secondary=class_participants, back_populates='participants')
    # classes = db.relationship('Class', secondary=class_participants, backref='participants')

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # student = db.relationship('User', back_populates='classes')
    # participants = db.relationship('User', backref='classes')
    # participants = db.relationship('User', secondary=class_participants, back_populates='classes')
    # participants = db.relationship('User', secondary=class_participants, backref='classes')
    
    
with appp.app_context():  
    db.create_all()   

# appp.app_context().push()     #to start
# appp.app_context().pop()      #to stop



@appp.route('/create_profile/<int:user_id>/<bio>')
def create_profile(user_id, bio):
    user = User.query.get(user_id)
    if user:
        profile = Profile(bio=bio, user_id=user_id)
        db.session.add(profile)
        db.session.commit()
        return "Profile Created"
    return "User Not Found"

@appp.route('/profile/<int:user_id>')
def get_profile(user_id):
    user = User.query.get(user_id)
    
    if user and user.profile:
        print(user.profile.id)
        print(user.profile.user_id)
        return render_template('profile.html', user=user)
    return "Profile not found"

# One-to-Many: Create & View User's Classes
@appp.route('/create_class/<int:user_id>/<title>')
def create_class(user_id, title):
    class_instance = Class(title=title, user_id=user_id)
    db.session.add(class_instance)
    db.session.commit()
    return "Class Created"

# Fetch One-to-Many Relationship
@appp.route('/classes/<int:user_id>')
def get_classes(user_id):
    user = User.query.get(user_id)
    return render_template('classes.html', user=user)

# Fetch Many-to-Many Relationship
@appp.route('/enrolled_classes/<int:user_id>')
def get_enrolled_classes(user_id):
    user = User.query.get(user_id)
    return render_template('enrolled_classes.html', user=user)

@appp.route('/enroll_user/<int:user_id>/<int:class_id>')
def enroll_user(user_id, class_id):
    user = User.query.get(user_id)
    class_instance = Class.query.get(class_id)

    if user and class_instance:
        class_instance.participants.append(user)  # Add user to class participants
        db.session.commit()
        return f"User {user.username} enrolled in {class_instance.title}"
    return "User or Class not found"

# @appp.route('/get_class')
# def get_class():
#     classes = Class.query.all()
#     user = User.query.get(1)
#     print(user.classes)  # List of quizzes created by the user

#     classs = Class.query.get(1)
#     print(classs.student)  # User who created the quiz (automatically available)  
#     return {"classes": "done"}

# @appp.route('/get_all')
# def get_all():
#     user = User.query.get(1)
#     print(user.classes)  # List of quizzes the user participated in

#     quiz = Class.query.get(1)
#     print(quiz.participants) 
#     return "done"  # List of users who participated in this quiz



@appp.route('/create_user')
def create_user():
    user = User(username="admin")
    # user = User(username="admin", password="admin",email="admin@g.com")
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

# with appp.app_context(): 
    # create_user()
    # create_class()

if __name__ == '__main__':
    appp.run(debug=True)
    




