import os
import boto3, urllib3
import csv
from twilio.rest import Client

AUTH = os.environ['AUTH']
PHONE = os.environ['PHONE']
SID = os.environ['SID']
TO = os.environ['TO']

CLIENT = Client(SID, AUTH)

FIVETHIRTYEIGHT = 'https://projects.fivethirtyeight.com/'\
    '2020-general-data/presidential_national_toplines_2020.csv'


def getfiles():
    http = urllib3.PoolManager()
    resp = http.request('GET', FIVETHIRTYEIGHT)
    five = resp.data.decode('utf-8')
    return resp.status

def text(message):
    message = CLIENT.messages.create(to=TO, from_=PHONE, body=message)
    stat = getfiles()

    return [message.sid, stat]

def main():
    data = text('test')
    return data
