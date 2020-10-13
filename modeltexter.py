import os
from twilio.rest import Client

AUTH = os.environ['AUTH']
PHONE = os.environ['PHONE']
SID = os.environ['SID']
TO = os.environ['TO']

CLIENT = Client(SID, AUTH)

def text(message):
    message = CLIENT.messages.create(to=TO, from_=PHONE, body=message)
    return message

def main():
    data = text('test')
    return data
