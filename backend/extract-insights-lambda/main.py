from src.analyzer import Analyzer


def lambda_handler(event, context):
    # Retrieve the CSV file from the S3 bucket
    # bucket = event['Records'][0]['s3']['bucket']['project-cvs-files']
    # key = event['Records'][0]['s3']['object']['key']
    bucket = "project-cvs-files"
    key = "airpods.csv"
    response = s3.get_object(Bucket=bucket, Key=key)
    csv_content = response["Body"].read().decode("utf-8")

    analyzer = Analyzer()
    analyzer.run(csv_content)
    return True
