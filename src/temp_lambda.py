import json
import boto3
import os

# This is a temporary lambda function to chekc SNS and Cloud watch services
client = boto3.client('sns')
         
def lambda_handler(event, context):
   try:  
      
      topic_arn = os.environ.get('TOPIC_ARN')
      one = "One"
      two = 2
      total = sum(one, two)
      return total
   except TypeError:
      
      client.publish(TopicArn=topic_arn,Message="type error ")
