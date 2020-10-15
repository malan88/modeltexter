import os, csv
import urllib3
import boto3
from twilio.rest import Client

AUTH = os.environ['AUTH']
PHONE = os.environ['PHONE']
SID = os.environ['SID']

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
            ':t': str(trump),
            ':b': str(biden)
        }
    )


def getlast538():
    table = gettable()
    resp = table.get_item(Key={'id': '538'})['Item']
    return float(resp['Trump']), float(resp['Biden'])


def get538():
    http = urllib3.PoolManager()
    resp = http.request('GET', FIVETHIRTYEIGHT)
    table = list(csv.reader(resp.data.decode('utf-8').split('\n')))
    trump = float(table[1][7]) * 100
    biden = float(table[1][8]) * 100
    return trump, biden


def proc538():
    newtrump, newbiden = get538()
    oldtrump, oldbiden = getlast538()
    message = None
    if newtrump != oldtrump or newbiden != oldbiden:
        message = text(f"{newtrump} - {newbiden}")
        updatetable(newtrump, newbiden)
    return message


def getnumbers():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('phone')
    resp = table.scan()
    return resp['Items']


def text(message):
    numbers = getnumbers()
    failures = []
    successes = []
    for number in numbers:
        success = CLIENT.messages.create(to=number['num'],
                                         from_=PHONE,
                                         body=message)
        if not success.sid:
            failures.append(number)
        else:
            successes.append(success.sid)
    return [failures, successes]


def main():
    data = proc538()
    return data
