from celery_worker import celery_app
from models import User, BookRequest
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from flask import render_template

SMTP_HOST = 'localhost'
SMTP_PORT = 1025
SENDER_EMAIL = "skp@iitm.in"
SENDER_PASSWORD = ""


def send_email(to_address, subject, body, content_type="text", attachments=None):
    msg = MIMEMultipart()
    msg['To'] = to_address
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    
    if content_type == "html":
        msg.attach(MIMEText(body, 'html'))
    else:
        msg.attach(MIMEText(body, 'plain'))
    s = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    s.login(SENDER_EMAIL, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    return True 
    


@celery_app.task
def generate_monthly_report():
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        return "No admin user found."
    book_requests = BookRequest.query.all()
    book_details = []
    for req in book_requests:
        user_id = req.user_id
        username = User.query.get(user_id).username
        book_name = req.book_name
        status = req.status
        
        book_details.append({'username': username, 'book_name': book_name, 'status': status})
    # print(book_details)    
    html_body = render_template('monthly_report.html', book_details=book_details)   
    send_email(admin.email, "Monthly Book Request Report", html_body, content_type="html")   
    return "Monthly report generated and sent to admin."


@celery_app.task
def send_daily_reminder():
    user = User.query.all()
    book_requests = BookRequest.query.filter_by(status='pending').all()
    
    for u in user:
        for req in book_requests:
            if u.id == req.user_id:
                message = f"Hello {u.username}, you have a pending book request for '{req.book_name}' made on {req.request_date}."
                send_email(u.email, "Daily Reminder", message)
    return "done sending daily reminder."

@celery_app.task
def generate_user_report(user_id):
    user = User.query.get(user_id)
    if not user:
        return f"No user found with ID {user_id}"
    
    req = BookRequest.query.filter_by(user_id=user_id).all()
    
    rq = []
    for r in req:
        user_id = r.user_id
        username = User.query.get(user_id).username
        book_name = r.book_name
        status = r.status
        
        rq.append({'username': username, 'book_name': book_name, 'status': status})
    # print(book_details)    
    html_body = render_template('monthly_report.html', book_details=rq)   
    send_email(user.email, "Monthly Book Request Report", html_body, content_type="html")   
     
        
    return f"Report generated for user {user.username} with {len(req)} book requests"    