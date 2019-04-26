import json
import boto3
import decimal
from botocore.vendored import requests
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

s3_client = boto3.client('s3')
bucket = "yelp-restaurants"
json_file_name = "data_json.json"
headers = {'Content-Type': 'application/json'}
url = 'https://search-mealbot-production-t2xwa56pdi7fopnif65ouu43la.us-west-2.es.amazonaws.com/restaurants/restaurant/_bulk'


def read_from_s3():
    data = ''
    #count = 0
    json_object = s3_client.get_object(
        Bucket=bucket, Key=json_file_name)  # get json object
    jsonFileReader = json_object['Body'].read()  # read json file context
    restaurants = json.loads(jsonFileReader.decode('utf-8'),
                             parse_float=decimal.Decimal)  # decide json and use decimal to modify float data
    for restaurant in restaurants:
        # for category in restaurant['categories']:
        id = restaurant['id']
        categories = restaurant['categories']
        data = data + "{\"index\": {}}\n" + "{{\"Id\":\"{}\", \"Cuisine\":\"{}\"}}\n".format(id,categories)
        #count = count + 1
    #index to elastic search
    response = requests.post(url, headers=headers, data=data)
    json_data = response.json()
    #logger.debug('json_data>>>{}'.format(count))
    return json_data


def lambda_handler(event, context):
    data = read_from_s3()
    return {
        'statusCode': 200,
        'body': json.dumps('Succesfully!')
    }
