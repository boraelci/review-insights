from src.create_product_handler import CreateProductHandler
from src.get_analysis_handler import GetAnalysisHandler
from src.list_products_handler import ListProductsHandler
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
        return create_product_handler.run(body=event["body"])
    elif resourcePath == "/analyses/{product_id}" and httpMethod == "GET":
        get_analysis_handler = GetAnalysisHandler(table_name=table_name)
        return get_analysis_handler.run(product_id=event['product_id'])
    elif resourcePath == "/products" and httpMethod == "GET":
        list_products_handler = ListProductsHandler(table_name=table_name)
        return list_products_handler.run()
    else:
        return {"statusCode": 400, "body": "Path/method not implemented in Lambda"}
