from flask import Flask 
from flask_restful import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

class Course(Resource):
    def get(s, course_id):
        if course_id == 201:
                return {
                        "course_id": 201,
                        "course_name": "Maths1",
                        "course_code": "MA101",
                        "course_description": "Course Description Example"
                        }
                
        else: 
            return {"COURSE001":"Course Name is required"},404
        

api.add_resource(Course,'/api/course/<int:course_id>')   


if __name__ == '__main__':
    app.run(debug=True)     