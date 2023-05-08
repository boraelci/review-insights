from src.webscraper import WebScraper
import json
import os
import boto3
from selenium.common.exceptions import TimeoutException, WebDriverException
import time

env = os.environ.get("ENV", default="dev")
sqs = boto3.client("sqs")

if env == "dev":
  webscraper = WebScraper(env=env)
  webscraper.run(original_url="auto", number_pages=10)
  exit(0)

bucket_name = os.environ["REVIEWS_BUCKET_NAME"]
queue_url = os.environ["EXTRACT_INSIGHTS_QUEUE_URL"]


def lambda_handler(event, context):
    print(event)

    product_id, product_name, product_link, product_category, seller_id = parse_from_sqs(event=event)
   
    i = 0
    while i < 10:
        try:
            webscraper = WebScraper(env=env)
            webscraper.run(original_url=product_link, number_pages=10)
            break
        except (TimeoutException, WebDriverException) as e:
            print(e)
            print("Trying again...")
            time.sleep(1)
            continue
        
    webscraper.save(
        bucket_name=bucket_name,
        product_id=product_id,
        reviews=webscraper.amazon_reviews,
    )
    push_to_sqs(
        product_id=product_id,
        product_name=product_name,
        product_link=product_link,
        product_category=product_category,
        seller_id=seller_id)
    return {"statusCode": 200, "body": "Success!"}


def try_ex(func):
    try:
        return func()
    except KeyError:
        return None
    except TypeError:
        return None


def parse_from_sqs(event):
    messages = try_ex(lambda: event["Records"])
    if messages is None:
        return "No messages in the queue"
    for message in messages:
        # TODO: only 1 for now, return and main structure should be update to support more
        receipt_handle = message["receiptHandle"]
        message_attributes = message["messageAttributes"]
        product_id = message_attributes["product_id"]["stringValue"]
        product_name = message_attributes["product_name"]["stringValue"]
        product_link = message_attributes["product_link"]["stringValue"]
        product_category = message_attributes["product_category"]["stringValue"]
        seller_id = message_attributes["seller_id"]["stringValue"]
    # sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
    return product_id, product_name, product_link, product_category, seller_id


def push_to_sqs(product_id, product_name, product_link, product_category, seller_id):
    try:
        message_attributes = {
            "product_id": {"StringValue": product_id, "DataType": "String"},
            "product_name": {"StringValue": product_name, "DataType": "String"},
            "product_link": {"StringValue": product_link, "DataType": "String"},
            "product_category": {
                "StringValue": product_category,
                "DataType": "String",
            },
            "seller_id": {"StringValue": seller_id, "DataType": "String"},
        }
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageAttributes=message_attributes,
            MessageBody=("Push product to queue"),
        )
    except Exception as e:
        raise Exception("Could not push to queue: %s" % e)
