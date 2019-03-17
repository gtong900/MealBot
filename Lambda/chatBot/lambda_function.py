import boto3
import json
import datetime

print('Loading function')
client = boto3.client('lex-runtime')


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json'
        },
    }


def lambda_handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    To scan a DynamoDB table, make a GET request with the TableName as a
    query string parameter. To put, update, or delete an item, make a POST,
    PUT, or DELETE request respectively, passing in the payload to the
    DynamoDB API as a JSON body.
    '''
    #print("Received event: " + json.dumps(event, indent=2))

    operation = event['http_method']
    if operation == 'POST':
        requestBody = event['body']
        parsedText = requestBody['messages'][0]['unstructured']['text']
        identityId = requestBody['messages'][0]['unstructured']['id']
        response = client.post_text(
            botName='OrderFoodBot',
            botAlias='demo',
            userId= identityId,
            sessionAttributes={
            },
            requestAttributes={
            },
            inputText=parsedText
        )
        
        payload = {
            "messages": [
                {
                  "type": "response",
                  "unstructured": {
                    "id": identityId,
                    "text": response["message"],
                    "timestamp": round(datetime.datetime.now().timestamp())
                  }
                }
            ]
        }
        return respond(None, payload)
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))