from app import mail
from threading import Thread
import smtplib, ssl
from flask_mail import Mail, Message

def send_email(reciever, message):
    server = smtplib.SMTP()
    # server.connect('smtp.googlemail.com', '465')


    port = 465  # For SSL
    password = 'Congratulations'
    subject = "Hermes_Prediction Result(s)"
    message = 'Subject: {}\n\n{}'.format(subject, message)

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("hermesprediction@gmail.com", password)
        server.sendmail("hermesprediction@gmail.com", reciever, message)


