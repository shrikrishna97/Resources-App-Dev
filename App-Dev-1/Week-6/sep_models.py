from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy object (will be linked to Flask app in app.py)
db = SQLAlchemy()

class LinkedInProfile(db.Model):
    __tablename__ = 'linkedin_profiles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    linkedin_url = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<LinkedInProfile name={self.name} linkedin_url={self.linkedin_url}>"
