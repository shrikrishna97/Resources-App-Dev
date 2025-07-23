from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func  #new line added here

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///players.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the new table PlayerStats
class PlayerStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    runs = db.Column(db.Integer, nullable=False)

# Initialize and populate the database
@app.route('/setup_db')
def setup_db():
    db.drop_all()
    db.create_all()

    # Insert records: (1, 45), (2, 123), (3, 87)
    db.session.add_all([
        PlayerStats(id=1, runs=45),
        PlayerStats(id=2, runs=123),
        PlayerStats(id=3, runs=87),
    ])
    db.session.commit()


    
    result = db.session.query.max(PlayerStats.runs)
    result = db.session.query(func.max(PlayerStats.runs)).scalar()
    result = db.session.query(func.max(PlayerStats.runs))
    result = db.session.query.max(PlayerStats.runs).scalar()
    print(f"Maximum Runs: {result}")

if __name__ == '__main__':
    app.run(debug=True)
