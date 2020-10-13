import os, csv
import urllib3
import boto3
from twilio.rest import Client

AUTH = os.environ['AUTH']
PHONE = os.environ['PHONE']
SID = os.environ['SID']
TO = os.environ['TO']
TOETHAN = os.environ['TOETHAN']

TABLE = 'modeltexter'

CLIENT = Client(SID, AUTH)

FIVETHIRTYEIGHT = 'https://projects.fivethirtyeight.com/'\
    '2020-general-data/presidential_national_toplines_2020.csv'


def gettable():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE)
    return table


def updatetable(trump, biden):
    table = gettable()
    table.update_item(
        Key={'id': '538'},
        UpdateExpression="set Trump=:t, Biden=:b",
        ExpressionAttributeValues={
            ':t': trump,
            ':b': biden
        }
    )


def getlast538():
    table = gettable()
    resp = table.get_item(Key={'id': '538'})['Item']
    return int(resp['Trump']), int(resp['Biden'])


def get538():
    http = urllib3.PoolManager()
    resp = http.request('GET', FIVETHIRTYEIGHT)
    table = list(csv.reader(resp.data.decode('utf-8').split('\n')))
    trump = round(float(table[1][7]), 2) * 100
    biden = round(float(table[1][8]), 2) * 100
    return int(trump), int(biden)


def proc538():
    newtrump, newbiden = get538()
    oldtrump, oldbiden = getlast538()
    message = None
    if newtrump != oldtrump or newbiden != oldbiden:
        message = text(f"{newtrump} - {newbiden}")
        updatetable(newtrump, newbiden)
    return message


def text(message):
    success = CLIENT.messages.create(to=TO, from_=PHONE, body=message)
    CLIENT.messages.create(to=TOETHAN, from_=PHONE, body=message)
    return [success.sid]


def main():
    data = proc538()
    return data
