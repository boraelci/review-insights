from src.report_generator import ReportGenerator
import json
import os

frontend_url = os.environ["FRONTEND_URL"]

def lambda_handler(event, context):
    product_id, seller_id = parse_from_sqs(event=event)
    sender_email = "be2246@columbia.edu"
    receiver_email = "be2246@columbia.edu"
    report_generator = ReportGenerator()
    report_generator.run(frontend_url=frontend_url, product_id=product_id, sender_email=sender_email, receiver_email=receiver_email)
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
        # TODO: only 1 for now, return and main structure should be update to support mode
        # receipt_handle = message["receiptHandle"]
        message_attributes = message["messageAttributes"]
        product_id = message_attributes["product_id"]["stringValue"]
        seller_id = message_attributes["seller_id"]["stringValue"]
    # sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
    return product_id, seller_id
