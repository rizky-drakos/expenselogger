import os
import json
import logging

from boto3                      import resource
from boto3.dynamodb.conditions  import Key


logger = logging.getLogger()
logger.setLevel("INFO")

def __transform_items(items):
    for item in items:
        item["cost"] = int(item["cost"])
        item["item"] = item["date_item"].split('#')[1]
        item["date"] = item["date_item"].split('#')[0]
        del item["date_item"]
    return items

def lambda_handler(event, context):
    TABLE_NAME = os.getenv("TABLE_NAME")
    try:
        table = resource('dynamodb').Table(TABLE_NAME)
        if not event["queryStringParameters"]:
            result = table.query(KeyConditionExpression = Key("username").eq("root")) # Temporarily hard code the username.
        else:
            if "time" not in event["queryStringParameters"]:
                raise ValueError("Query parameter missing: time")
            result = table.query(
                KeyConditionExpression = Key("username").eq("root") \
                & Key("date_item").begins_with(event["queryStringParameters"]["time"])
            )
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "items": __transform_items(result["Items"])
            })
        }
    except Exception as error:
        logger.error(f"Failed to retrieve items with error: {error}")
        response = { "statusCode": 400 }

    return response
