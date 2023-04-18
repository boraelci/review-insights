import json
import boto3
import os
import uuid


class CreateProductHandler:
    def __init__(self, queue_url):
        self.sqs = boto3.client("sqs")
        self.queue_url = queue_url

    def run(self, body):
        product_id = str(uuid.uuid4())
        product_name = body["product_name"]
        product_link = body["product_link"]
        product_category = body["product_category"]
        seller_id = "be2246"  # TODO: get seller_id from body
        self.push_to_sqs(
            product_id=product_id,
            product_name=product_name,
            product_link=product_link,
            product_category=product_category,
            seller_id=seller_id,
        )

    def push_to_sqs(
        self, product_id, product_link, product_name, product_category, seller_id
    ):
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
            response = self.sqs.send_message(
                QueueUrl=self.queue_url,
                MessageAttributes=message_attributes,
                MessageBody=("Push product to queue"),
            )
        except Exception as e:
            raise Exception("Could not push to queue: %s" % e)
