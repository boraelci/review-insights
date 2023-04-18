from src.report_generator import ReportGenerator
import json


def lambda_handler(event, context):
    report_generator = ReportGenerator()
    report_generator.run(event)
    return {"statusCode": 200, "body": json.dumps("Success!")}
