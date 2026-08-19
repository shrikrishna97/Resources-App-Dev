from celery_worker import celery_app
from models import User, BookRequest


@celery_app.task
def generate_user_report(user_id):
    user = User.query.get(user_id)
    if not user:
        return f"No user found with ID {user_id}"
    
    req = BookRequest.query.filter_by(user_id=user_id).all()
    
    print("Report Starts Here")
    for r in req:
        print(r.book_name , r.status , r.request_date)
    print("Report Ends Here")    
        
    return f"Report generated for user {user.username} with {len(req)} book requests"    