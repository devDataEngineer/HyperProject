import json
import boto3
import os

# This is a temporary lambda function to check SNS and Cloud watch services
client = boto3.client('sns')
         
def lambda_handler(event, context):
   try:  
      messege = "this is from second transform lambad messege"
      topic_arn = os.environ.get('TOPIC_ARN')
      one = "One"
      two = 2
      total = sum(one, two)
      return total
   except TypeError:
      
      client.publish(TopicArn=topic_arn,Message=messege)
