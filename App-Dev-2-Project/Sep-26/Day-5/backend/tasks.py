from celery_worker import celery_app
from models import User, Reservation
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

SERVER_SMTP_HOST = 'localhost'
SERVER_SMTP_PORT = 1025
SENDER_ADDRESS = 'sk@gmail.com'
SENDER_PASSWORD = ''


def send_email(to_address,subject, body, content='text', attachment=None):
    msg = MIMEMultipart()
    msg['To'] = to_address
    msg['From'] = SENDER_ADDRESS
    msg['Subject'] = subject
    if content == 'html':
        msg.attach(MIMEText(body, 'html'))
    else: 
        msg.attach(MIMEText(body, 'plain'))
    
    if attachment:
        with open(attachment, 'rb') as a:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(a.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={attachment}')
        msg.attach(part)
        
    s = smtplib.SMTP(SERVER_SMTP_HOST, SERVER_SMTP_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    return True

@celery_app.task
def send_daily_reminder():
    active_reservations = Reservation.query.filter(Reservation.status == 'active').all()            
    
    for reservation in active_reservations:
        user = User.query.get(reservation.user_id)
        if user:
            subject = "Daily Reminder: Your Parking Reservation is Active"
            body = f"Hello {user.username},\n\nThis is a friendly reminder about your parking reservation at {reservation.parking_spot.id} on {reservation.start_time}.\n\nThank you for using our service!"
            send_email(user.email, subject, body)
            
    return "daily reminder has been sent."        