from src.webscraper import WebScraper
import json
import os

env = os.environ.get("ENV", default="dev")
bucket_name = os.environ.get("REVIEWS_BUCKET_NAME")


def lambda_handler(event, context):
    product_id = event["product_id"]
    webscraper = WebScraper("auto", env)
    webscraper.run()
    webscraper.save(bucket_name, product_id, webscraper.amazon_reviews)
    return {
        "statusCode": 200,
        "body": json.dumps("Success!"),
    }


if env == "dev":
    lambda_handler({"product_id": "air1"}, None)
