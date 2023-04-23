from src.analyzer import Analyzer
import json
import boto3
import os

bucket_name = os.environ["REVIEWS_BUCKET_NAME"]
queue_url = os.environ["GENERATE_REPORT_QUEUE_URL"]
table_name = os.environ["ANALYSIS_TABLE_NAME"]


def lambda_handler(event, context):
    print(event)

    product_id, seller_id = parse_from_sqs(event=event)
    s3 = boto3.client("s3")
    key = f"{product_id}.csv"
    response = s3.get_object(Bucket=bucket_name, Key=key)
    csv_content = response["Body"].read().decode("utf-8")

    analyzer = Analyzer(table_name=table_name, queue_url=queue_url)
    result = analyzer.run(key=key, reviews=csv_content)
    print(result)
    push_to_sqs(product_id=product_id, seller_id=seller_id)
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


def push_to_sqs(product_id, seller_id):
    sqs = boto3.client("sqs")
    try:
        message_attributes = {
            "product_id": {"StringValue": product_id, "DataType": "String"},
            "seller_id": {"StringValue": seller_id, "DataType": "String"},
        }
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageAttributes=message_attributes,
            MessageBody=("Push product to queue"),
        )
    except Exception as e:
        raise Exception("Could not push to queue: %s" % e)
