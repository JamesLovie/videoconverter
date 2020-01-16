import boto3
import json
import urllib
import os

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))

    # Get the object from the event
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    print(key)
    # Create an SNS client
    sns = boto3.client('sns')

    # Publish a simple message to the specified SNS topic
    response = sns.publish(
        TopicArn='arn:aws:sns:ap-southeast-2:062497424678:videoconverter-topic',
        Message=key
    )

    # Print out the response
    print(response)