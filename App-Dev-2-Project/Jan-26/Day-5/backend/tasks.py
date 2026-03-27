from celery_worker import celery_app
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
import smtplib 
from flask import render_template
from models import User, Reservation, ParkingLot, ParkingSpot

SERVER_SMTP_HOST = 'localhost'
SERVER_SMTP_PORT = 1025
SENDER_ADDRESS='shrikrishna@gmail.com'
SENDER_PASSWORD=''

def send_email(to_address,subject,message,content="text",attachment=None):
    msg = MIMEMultipart()
    msg['To']=to_address
    msg['From']=SENDER_ADDRESS
    msg['Subject']=subject
    if content == "html":
        msg.attach(MIMEText(message,'html'))
    else:
        msg.attach(MIMEText(message, 'plain'))

    if attachment:
        with open(attachment,"rb") as a:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(a.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment: filename={attachment}")
        msg.attach(part)          

    s = smtplib.SMTP(host=SERVER_SMTP_HOST, port=SERVER_SMTP_PORT )
    s.login(SENDER_ADDRESS,SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    return True

@celery_app.task
def send_monthly_report():
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        return "No admin user found"
    reservation = Reservation.query.all()
    reservation_data = []
    for res in reservation:
        user = User.query.get(res.user_id)
        parking_spot = ParkingSpot.query.get(res.parking_spot_id)
        parking_lot = ParkingLot.query.get(parking_spot.parking_lot_id)
        reservation_data.append({
            'username': user.username,
            'vehicle_number': res.vehicle_number,
            'parking_lot': parking_lot.name,
            'status': res.status,
            'cost': res.cost
        })
    html = render_template('monthly_report.html', reservations=reservation_data)
    send_email(admin.email, "Monthly Report", html, content="html")
    
    # Logic to generate report and send email
    return "Monthly report sent to admin."
    
@celery_app.task
def send_daily_reminder():  
    active_reservations = Reservation.query.filter_by(status='active').all()
    for res in active_reservations:
        user = User.query.get(res.user_id)
        send_email(user.email, "Daily Reminder", f"Dear {user.username}, you have an active reservation for your vehicle {res.vehicle_number}. Please remember to complete it on time.") 
    # Logic to generate reminder and send email
    return "Daily reminder sent to users with active reservations"
    
@celery_app.task
def export_reservations_report(user_id):
        user = User.query.get(user_id)
        reservations = Reservation.query.filter_by(user_id=user_id).all()
        reservation_data = []
        for res in reservations:
            parking_spot = ParkingSpot.query.get(res.parking_spot_id)
            parking_lot = ParkingLot.query.get(parking_spot.parking_lot_id)
            reservation_data.append({
                'vehicle_number': res.vehicle_number,
                'parking_lot': parking_lot.name,
                'status': res.status,
                'start_time': res.start_time,
                'end_time': res.end_time,
                'cost': res.cost
            })
        html = render_template('export.html', reservations=reservation_data, username=user.username, total_reservations=len(reservation_data), total_cost=sum(res['cost'] for res in reservation_data))    
        
        send_email(user.email, "Your Reservations Report", html, content="html")
        return "Reservations report sent to user."
            
        
