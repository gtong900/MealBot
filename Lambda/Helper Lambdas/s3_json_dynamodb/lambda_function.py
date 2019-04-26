import json
import boto3
import decimal

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # TODO implement
    bucket = event['Records'][0]['s3']['bucket']['name']  # get the bucket name
    print("buctet is :", bucket)
    json_file_name = event['Records'][0]['s3']['object']['key']  # get the json file name
    if json_file_name == 'data_json.json':
        json_object = s3_client.get_object(Bucket=bucket, Key=json_file_name)  # get json object
        jsonFileReader = json_object['Body'].read()  # read json file context
        table = dynamodb.Table('yelp-restaurants-v2')
        restaurants = json.loads(jsonFileReader.decode('utf-8'),
                                 parse_float=decimal.Decimal)  # decide json and use decimal to modify float data
        for restaurant in restaurants:
            id = restaurant['id']
            # alias = restaurant['alias']
            name = restaurant['name']
            # is_closed = restaurant['is_closed']
            categories = restaurant['categories']
            # coordinates = restaurant['coordinates']
            # location = restaurant['location']

            table.put_item(
                Item={
                    'id': id,
                    # 'alias': alias,
                    'name': name,
                    # 'is_closed': is_closed,
                    'categories': categories,
                    # 'coordinates': coordinates,
                    # 'location': location,

                }
            )
            print("rest added", restaurant)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }