import json
from botocore.vendored import requests
import random
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
dynamodb = boto3.client('dynamodb')
sqs = boto3.client('sqs')
ses = boto3.client('ses')

def elastic_search(message):
    #elastic search
    messageAttributes=message['MessageAttributes']
    cuisine = messageAttributes['Cuisine']['StringValue']
    location = messageAttributes['Location']['StringValue']
    date = messageAttributes['Date']['StringValue']
    time = messageAttributes['Time']['StringValue']
    people = messageAttributes['People']['StringValue']
    
    headers = {'Content-Type': 'application/json'}
    url = 'https://search-mealbot-production-t2xwa56pdi7fopnif65ouu43la.us-west-2.es.amazonaws.com/restaurants/_search?pretty&size=500'
    data = json.dumps({
        "query": {
            "match": {
                "Cuisine": cuisine
            }
        }
    })
    response = requests.post(url, headers=headers, data=data)
    json_data = response.json()
    
    
    #get the total number of results
    hits=json_data["hits"]["total"]
    
    #randomly pick id of one of the results
    random_number = random.randint(0,hits-1)
    parsedID = json_data["hits"]["hits"][random_number]["_source"]["Id"]
    #retrieve data from dynamodb
    restaurant_info = retrieve_from_dynamodb(parsedID, cuisine)
    restaurant_name = restaurant_info['Item']['name']['S']
    return "Your {} dinning recommendations for {} people in {} on {} at {} is : {}".format(cuisine,people,location,date,time,restaurant_name)
    
def retrieve_from_dynamodb(restaurant_id, cuisine):
    response = dynamodb.get_item(
        TableName='yelp-restaurants-v2',
        Key={
            'categories': {
                'S': cuisine
            },
            'id': {
                'S': restaurant_id
            }
        }
    )
    return response
    
def poll_one_message_from_SQS():
    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl='https://sqs.us-west-2.amazonaws.com/321471117150/mealbot-queue',
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    if "Messages" not in response:
        return None
    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']
    
    #Delete received message from queue
    sqs.delete_message(
        QueueUrl='https://sqs.us-west-2.amazonaws.com/321471117150/mealbot-queue',
        ReceiptHandle=receipt_handle
    )
    
    return message
    
def send_email_to_user(email, bodyText):
    response = ses.send_email(
        Source='gtong900@gmail.com',
        Destination={
            'ToAddresses': [
                email
            ],
            'CcAddresses': [
            ],
            'BccAddresses': [
            ]
        },
        Message={
            'Subject': {
                'Data': 'MealBot-recommendations for your dinning.',
                'Charset': 'UTF-8'
            },
            'Body': {
                'Text': {
                    'Data': bodyText,
                    'Charset': 'UTF-8'
                }
            }
        },
        ReplyToAddresses=[
            'gtong900@gmail.com',
        ]
    )
    return response['MessageId']
    
def lambda_handler(event, context):
    # TODO implement
    message = poll_one_message_from_SQS()
    if message is None:
        return "no message in SQS"
    cuisine = message['MessageAttributes']['Cuisine']['StringValue']
    searchReult = elastic_search(message)
    return send_email_to_user(message['MessageAttributes']['Email']['StringValue'], searchReult)
