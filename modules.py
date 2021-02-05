from pymongo import MongoClient
client = MongoClient("mongodb+srv://Admin:kdjhi832h!ya6@cluster0.l6quu.mongodb.net/hackaton?retryWrites=true&w=majority")
db = client.hackaton
users = db.users
codes = db.codes
rooms = db.rooms

from server import sio

from datetime import datetime
import threading
import bcrypt
import time as tim

import smtplib
HOST = "smtp.gmail.com"
email_server = smtplib.SMTP(HOST)
email_server.ehlo()
email_server.starttls()
email_server.login("hack05022021@gmail.com", "kdjhi832h!ya6")

class helpful_functions():

    def __init__(self):
        pass

    def check_reg_codes(self):
        for user in codes.find():
            if (datetime.utcnow() - user['time']).seconds > 3600:
                codes.delete_one({
                    "email": user['email']
                })

    def send_email(self, subject, to, text):
        body = "\r\n".join((
            "From: hack05022021@gmail.com",
            "To: %s" % to,
            "Subject: %s" % subject,
            "",
            text + "\n\n\n------\nЭто письмо было отправлено автоматически. Отвечать на него не нужно",
        ))
        email_server.sendmail("hack05022021@gmail.com", [to], body.encode('utf8'))

    def check_session_id(self, data):
        email = data['email']
        user = users.find_one({
            'email': email,
        })
        if user != None and bcrypt.checkpw(data['session_id'].encode(), user['session_id']):
            return True
        else:
            return False


hf = helpful_functions()