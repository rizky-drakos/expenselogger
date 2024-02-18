import os
import json
import logging

from boto3                      import resource
from boto3.dynamodb.conditions  import Key


logger = logging.getLogger()
logger.setLevel("INFO")

def lambda_handler(event, context):
    TABLE_NAME = os.getenv("TABLE_NAME")
    try:
        payload = json.loads(event["body"])
        resource('dynamodb').Table(TABLE_NAME).put_item(
            Item = {
                "username": payload["username"],
                "date_item": "{}#{}".format(payload["date"], payload["item"]),
                "cost": payload["cost"]
            }
        )
        response = { "statusCode": 201 }
    except Exception as error:
        logger.error(f"Failed to create the item with error: {error}")
        response = { "statusCode": 400 }

    return response
