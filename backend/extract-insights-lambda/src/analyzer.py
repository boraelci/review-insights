import csv
import json
import datetime
import time
from botocore.exceptions import ClientError
from math import pi
from collections import defaultdict
import boto3
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
try:
    from .gpt_wrapper import GptWrapper
except:
    from gpt_wrapper import GptWrapper
import os

comprehend = boto3.client("comprehend")
s3 = boto3.client("s3")
env = os.environ.get("ENV", default="dev")

def round_float(number):
    """
    Round a float to two decimal places.
    """
    return round(number, 2)


class Analyzer:
    def __init__(self, table_name, queue_url, product_name, product_category):
        self.table_name = table_name
        self.queue_url = queue_url
        self.product_name = product_name
        self.product_category = product_category

    def run(self, product_id, product_name, product_link, product_category, seller_id, csv_content):
        historical_data = self.get_historical_data(csv_content)
        categorical_data = self.get_categorical_data(csv_content)

        
        if True and env == "dev":
            print({
                "product_id": product_id,
                "historical_data": historical_data,
                "categorical_data": categorical_data
            })
            return
        
        
        # Create DynamoDB client and table resource objects
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(self.table_name)

        table.put_item(
            Item={
                "product_id": product_id,
                "product_name": product_name,
                "product_link": product_link,
                "product_category": product_category,
                "seller_id": seller_id,
                "historical_data": json.dumps(historical_data),
                "categorical_data": json.dumps(categorical_data)
            }
        )

        return {
            "product_id": product_id,
            "historical_data": historical_data,
            "categorical_data": categorical_data
        }

    def get_historical_data(self, csv_content):
        csv_content = csv.DictReader(csv_content.splitlines())
        comprehend = boto3.client("comprehend")
        reviews = []
        dates = []
        for row in csv_content:
            reviews.append(row["Review"])
            date_obj = datetime.datetime.strptime(row["Date"], "%B %d, %Y")
            formatted_date = date_obj.strftime("%m/%d/%Y")
            dates.append(formatted_date)

        # Use Comprehend to analyze sentiments for all reviews
        sentiment_batches = []
        for i in range(0, len(reviews), 25):
            # Try to get sentiments with exponential backoff
            backoff = 0
            while True:
                try:
                    sentiment_batches.append(
                        comprehend.batch_detect_sentiment(
                            TextList=reviews[i : i + 25], LanguageCode="en"
                        )
                    )
                    break
                except ClientError as e:
                    if e.response["Error"]["Code"] == "ThrottlingException":
                        # If throttling exception, retry after exponential backoff
                        backoff += 1
                        wait_time = 2**backoff
                        print(
                            f"Throttling exception caught. Waiting for {wait_time} seconds before retrying..."
                        )
                        time.sleep(wait_time)
                    else:
                        # If some other exception, re-raise it
                        raise e

        positives = {}
        negatives = {}
        i = 0
        for batch in sentiment_batches:
            for sentiment in batch["ResultList"]:
                score = sentiment["SentimentScore"]["Positive"]
                date = dates[i]
                if score > 0.5:
                    positives[date] = positives.get(date, 0) + 1
                else:
                    negatives[date] = negatives.get(date, 0) + 1
                
                i += 1

        return {
            "positives": positives,
            "negatives": negatives,
        }

    def get_categorical_data(self, csv_content):
        csv_content = csv.DictReader(csv_content.splitlines())
        user_prompt_generate_categories = f"Product Name: {self.product_name} Product Category: {self.product_category}"
        system_prompt_generate_categories = "Generate and list 5 category names that customer reviews of the given product can be classified into, based on each review's main topic. The categories should be relevant to the type of the product being reviewed, not necessarily specific to this product. First one is \"Value for Money\" Reply in the following format: [\"<CATEGORY-1>\", ...]"
        gpt_generate_categories = GptWrapper(system_prompt_generate_categories)

        categories = eval(gpt_generate_categories.query(user_prompt_generate_categories))
        print(categories)

        reviews = []
        for row in csv_content:
            reviews.append(f"Index:{row['Index']} Review:{row['Review']}")

        system_prompt_evaluate_categories = f"Perform sentiment analysis on the following customer reviews based on the following categories. Categories: {categories}. For each review, label the category with the review's sentiment (Positive, Negative, or Neutral) if the review can be classified into a category, otherwise label it as {{\"<CATEGORY_NAME>\": \"N/A\"}}. Respond in the following format: {{\"<REVIEW_INDEX_1>\": {{\"<CATEGORY_1>\":\"<SENTIMENT>\", ...}}, ...}}. Don't include any explanation."
        gpt_evaluate_categories = GptWrapper(system_prompt_evaluate_categories)
        review_index_to_category_sentiments = {}
        
        def process_review(user_prompt_evaluate_categories):
            try:
                response = gpt_evaluate_categories.query(user_prompt_evaluate_categories)
                # print(response)
                return eval(response)
            except:
                return {}

        workers_size = 10
        batch_size = 25
        with ThreadPoolExecutor(max_workers=workers_size) as executor:
            futures = []
            for i in range(0, len(reviews), batch_size):
                user_prompt_evaluate_categories = str(reviews[i : i + batch_size])
                futures.append(executor.submit(process_review, user_prompt_evaluate_categories))

            for future in as_completed(futures):
                try:
                    result = future.result()
                    review_index_to_category_sentiments.update(result)
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
                except Exception as e:
                    print(f"Job failed with error: {e}")
        
        print(review_index_to_category_sentiments)
        positives = {} 
        negatives = {}
        for review_index, category_sentiments in review_index_to_category_sentiments.items():
            for category, sentiment in category_sentiments.items():
                if sentiment == "N/A" or category not in categories:
                    continue
                elif sentiment == "Positive":
                    positives[category] = positives.get(category, 0) + 1
                elif sentiment == "Negative":
                    negatives[category] = negatives.get(category, 0) + 1
        print(positives)

        return {
            "positives": positives,
            "negatives": negatives,
        }
        """
        total_count = len(list(csv_content))
        per_category_max_count = total_count // len(categories)

        positives = {}
        negatives = {}
        for category in categories:
            positives[category] = random.randint(1, per_category_max_count)
            negatives[category] = random.randint(1, per_category_max_count)

        return {
            "positives": positives,
            "negatives": negatives,
        }
        """
        

if __name__ == "__main__":
    product_id = "ea5d434d-e764-4d3b-a59c-02ada9cce5ea"
    with open (f"data/{product_id}.csv", "r") as f:
        csv_content = f.read()
    analyzer = Analyzer(table_name="analysis-table", queue_url=None, product_name="Apple AirPods Pro", product_category="Electronics")
    result = analyzer.run(
        product_id=product_id,
        product_name="Apple AirPods Pro",
        product_link="https://",
        product_category="Electronics",
        seller_id="123",
        csv_content=csv_content)

