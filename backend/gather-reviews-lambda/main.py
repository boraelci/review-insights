from src.webscraper import WebScraper
import json
import os
import boto3

env = os.environ.get("ENV", default="dev")
bucket_name = os.environ.get("REVIEWS_BUCKET_NAME")
sqs = boto3.client("sqs")


def try_ex(func):
    try:
        return func()
    except KeyError:
        return None
    except TypeError:
        return None


def get_product_info(event):
    messages = try_ex(lambda: event["Records"])
    if messages is None:
        return "No messages in the queue"
    for (
        message
    ) in (
        messages
    ):  # TODO: only 1 for now, return and main structure should be update to support mode
        receipt_handle = message["receiptHandle"]
        message_attributes = message["messageAttributes"]
        product_id = message_attributes["product_id"]["stringValue"]
        product_link = message_attributes["product_link"]["stringValue"]
    sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=receipt_handle)
    return product_id, product_link


def lambda_handler(event, context):
    print(event)

    product_id, product_link = get_product_info(event)
    webscraper = WebScraper(env=env)
    webscraper.run(original_url=product_link, number_pages=2)
    webscraper.save(bucket_name, product_id, webscraper.amazon_reviews)
    return {
        "statusCode": 200,
        "body": json.dumps("Success!"),
    }


if env == "dev":
    lambda_handler(
        {
            "product_id": "uuid-1",
            "product_link": "https://www.amazon.com/Tide-Febreze-Defense-Detergent-Packaging/dp/B01BZQJLFW/ref=asc_df_B01BZQJLFW/?tag=hyprod-20&linkCode=df0&hvadid=309832782859&hvpos=&hvnetw=g&hvrand=14385160540479028809&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9073502&hvtargid=pla-425063129473&psc=1&tag=&ref=&adgrpid=70155173188&hvpone=&hvptwo=&hvadid=309832782859&hvpos=&hvnetw=g&hvrand=14385160540479028809&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9073502&hvtargid=pla-425063129473",
        },
        None,
    )
