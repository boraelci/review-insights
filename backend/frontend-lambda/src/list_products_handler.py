import boto3
import json


class ListProductsHandler:
    def __init__(self, table_name):
        self.dynamodb = boto3.client("dynamodb")
        self.table_name = table_name

    def run(self):

        # specify the query parameters
        scan_params = {
            "TableName": self.table_name,
            }

        # execute the scan
        scan_response = self.dynamodb.scan(**scan_params)

        # return the results
        response = scan_response.get("Items", [])
        if len(response) == 0:
            return {"statusCode": 404, "body": "Not found"}

        products = []
        print(response)
        for item in response:
          products.append({
              "product_id": item["product_id"]["S"],
              "product_name": item["product_name"]["S"],
              "product_link": item["product_link"]["S"],
              "product_category": item["product_category"]["S"],
              "analysis_status": "Ready"
          })
        return {"statusCode": 200, "body": products}

if __name__ == "__main__":
    handler = ListProductsHandler("analysis-table")
    result = handler.run()
    print(result)