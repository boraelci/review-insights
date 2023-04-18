from src.create_product_handler import CreateProductHandler
from src.get_analysis_handler import GetAnalysisHandler
import json
import os

queue_url = os.environ.get("GATHER_REVIEWS_QUEUE_URL")
table_name = os.environ.get("ANALYSIS_TABLE_NAME")


def lambda_handler(event, context):
    print(event)
    resourcePath = event["resourcePath"]
    httpMethod = event["httpMethod"]
    if resourcePath == "/products" and httpMethod == "POST":
        print("Create product")
        create_product_handler = CreateProductHandler(queue_url=queue_url)
        create_product_handler.run(body=event["body"])
    else:
        get_analysis_handler = GetAnalysisHandler(table_name=table_name)
        get_analysis_handler.run()
    return {"statusCode": 200, "body": json.dumps("Success!")}
