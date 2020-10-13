import json
from modeltexter import main

def lambda_handler(event, context):
    data = main()
    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }

