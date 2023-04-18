import csv
import json
from datetime import datetime
import time
from botocore.exceptions import ClientError
from math import pi
from collections import defaultdict
import boto3

# Show graphs
show_graphs = False
if show_graphs:
    import matplotlib.pyplot as plt
# Initialize AWS services
sagemaker = boto3.client('sagemaker-runtime')
comprehend = boto3.client('comprehend')
rekognition = boto3.client('rekognition')
translate = boto3.client('translate')
s3 = boto3.client('s3')
visualize_bucket = 'project-visualized-images'

class Analyzer:

    def __init__(self):
        pass

    def get_text_sentiment(text):
        response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
        return response['Sentiment']


    def translate_text(text, target_language):
        response = translate.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language)
        return response['TranslatedText']


    def run(event):
        return {
            'body': {
                'insights': [
                    {'average_stars_over_time': json.dumps(average_stars(csv_content))},
                    {'sentiments_over_time': json.dumps(analyze_sentiments(csv_content))},
                    {'average_stars_per_category': json.dumps(categorize_reviews(csv_content))},
                ]
            }
        }


    def average_stars(csv_content):
        # Parse CSV content
        data = []
        reader = csv.DictReader(csv_content.splitlines())
        for row in reader:
            data.append(row)

        # Convert date strings to datetime objects
        for row in data:
            row['Date'] = datetime.strptime(row['Date'], '%B %d, %Y')

        # Group data by date and calculate average stars
        date_stars = {}
        for row in data:
            date: datetime = row['Date']
            stars = float(row['Stars'])
            if date in date_stars:
                date_stars[date]['stars'].append(stars)
            else:
                date_stars[date] = {'stars': [stars]}

        dates = []
        avg_stars = []
        for date, star_data in date_stars.items():
            dates.append(str(date))
            avg_stars.append(sum(star_data['stars']) / len(star_data['stars']))

        if show_graphs:
            # Create plot using Matplotlib
            plt.plot(dates, avg_stars)
            plt.xlabel('Date')
            plt.ylabel('Average Stars')
            plt.title('Average Stars Over Time')
            plt.show()

        return {'stars': avg_stars, 'dates': dates}


    def analyze_sentiments(csv_content):

        comprehend = boto3.client('comprehend')
        reader = csv.DictReader(csv_content.splitlines())
        reviews = []
        dates = []
        for row in reader:
            reviews.append(row['Review'])
            dates.append(row['Date'])

        # Use Comprehend to analyze sentiments for all reviews
        sentiment_batches = []
        for i in range(0, len(reviews), 25):
            # Try to get sentiments with exponential backoff
            backoff = 0
            while True:
                try:
                    sentiment_batches.append(comprehend.batch_detect_sentiment(
                        TextList=reviews[i:i + 25],
                        LanguageCode='en'
                    ))
                    break
                except ClientError as e:
                    if e.response['Error']['Code'] == 'ThrottlingException':
                        # If throttling exception, retry after exponential backoff
                        backoff += 1
                        wait_time = 2 ** backoff
                        print(f"Throttling exception caught. Waiting for {wait_time} seconds before retrying...")
                        time.sleep(wait_time)
                    else:
                        # If some other exception, re-raise it
                        raise e

        # Combine sentiment scores for all batches
        pos_sentiments = []
        neg_sentiments = []
        for batch in sentiment_batches:
            for sentiment in batch['ResultList']:
                pos_sentiments.append(sentiment['SentimentScore']['Positive'])
                neg_sentiments.append(sentiment['SentimentScore']['Negative'])

        # Group sentiments by date
        sentiments_by_date = {}
        for i in range(len(dates)):
            if dates[i] not in sentiments_by_date:
                sentiments_by_date[dates[i]] = {'positive': 0, 'negative': 0, 'count': 0}
            sentiments_by_date[dates[i]]['positive'] += pos_sentiments[i]
            sentiments_by_date[dates[i]]['negative'] += neg_sentiments[i]
            sentiments_by_date[dates[i]]['count'] += 1

        # Compute average sentiments for each date
        avg_pos_sentiments = []
        avg_neg_sentiments = []
        for date, sentiments in sentiments_by_date.items():
            avg_pos_sentiments.append(sentiments['positive'] / sentiments['count'])
            avg_neg_sentiments.append(sentiments['negative'] / sentiments['count'])

        if show_graphs:
            # Create a graph with two plots - negative sentiments and positive sentiments over time
            plt.plot(list(sentiments_by_date.keys()), avg_neg_sentiments, label='Negative Sentiments')
            plt.plot(list(sentiments_by_date.keys()), avg_pos_sentiments, label='Positive Sentiments')
            plt.xlabel('Date')
            plt.ylabel('Sentiment Score')
            plt.title('Sentiment Analysis of Reviews')
            plt.legend()
            plt.show()

        return {
            'positive': avg_pos_sentiments,
            'negative': avg_neg_sentiments,
            'dates': [str(date) for date in list(sentiments_by_date.keys())]
        }


    def categorize_reviews(csv_content):
        # Define the categories and the keywords that belong to each category
        categories = {
            'cost': ['cost', 'price', 'expensive', 'affordable', 'inexpensive'],
            'ease of use': ['easy', 'difficult', 'complicated', 'user-friendly', 'intuitive'],
            'effectiveness': ['effective', 'ineffective', 'successful', 'failure', 'helpful'],
            'quality': ['quality', 'cheap', 'poor', 'well-made', 'flimsy'],
            'durability': ['durable', 'breakable', 'long-lasting', 'fragile', 'sturdy']
        }

        # Create a defaultdict to store the reviews for each category
        reviews_per_category = defaultdict(list)

        # Create a defaultdict to store the total stars for each category
        stars_per_category = defaultdict(int)

        # Create a defaultdict to store the number of reviews for each category
        num_reviews_per_category = defaultdict(int)

        # Parse the CSV file
        reader = csv.DictReader(csv_content.splitlines())

        # Loop over the reviews and categorize them
        for row in reader:
            for category, keywords in categories.items():
                for keyword in keywords:
                    if keyword in row['Review'].lower():
                        reviews_per_category[category].append(row)
                        stars_per_category[category] += int(float(row['Stars']))
                        num_reviews_per_category[category] += 1
                        break

        # Compute the average rating for each category
        avg_stars_per_category = {
            category: stars_per_category[category] / num_reviews_per_category[category]
            for category in categories
            if num_reviews_per_category[category] > 0
        }

        if show_graphs:
            # Create the radar chart
            categories = list(avg_stars_per_category.keys())
            values = list(avg_stars_per_category.values())
            values += values[:1]
            angles = [n / float(len(categories)) * 2 * pi for n in range(len(categories))]
            angles += angles[:1]

            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
            ax.set_theta_offset(pi / 2)
            ax.set_theta_direction(-1)
            plt.xticks(angles[:-1], categories)
            ax.set_rlabel_position(0)
            plt.yticks([1, 2, 3, 4, 5], color="grey", size=7)
            plt.ylim(0, 5)
            ax.plot(angles, values, linewidth=1, linestyle="solid")
            ax.fill(angles, values, "b", alpha=0.1)

            plt.show()

        return avg_stars_per_category
