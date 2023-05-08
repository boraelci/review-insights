import boto3
import json


class GetAnalysisHandler:
    def __init__(self, table_name):
        self.dynamodb = boto3.client("dynamodb")
        self.table_name = table_name

    def run(self, product_id):
        ### dynamodb stuff below ###

        # specify the query parameters
        query_params = {
            "TableName": self.table_name,
            "KeyConditionExpression": "product_id = :pk",
            "ExpressionAttributeValues": {":pk": {"S": product_id}},
        }

        # execute the query
        query_response = self.dynamodb.query(**query_params)

        # return the results
        response = query_response["Items"]
        if len(response) == 0:
            return {"statusCode": 404, "body": "Not found"}

        item = response[0]
        ret = {
            "historical_data": json.loads(item["historical_data"]["S"]),
            "categorical_data": json.loads(item["categorical_data"]["S"]),
        }

        return {"statusCode": 200, "body": ret}

if __name__ == "__main__":
    handler = GetAnalysisHandler("analysis-table")
    result = handler.run("c982d117-2fcc-4cb7-b916-eec2b8fd3d97")
    print(result)