# Review Insights

![MIT License](https://img.shields.io/github/license/boraelci/review-master)

Sentiment Analysis of Amazon Product Reviews to Derive Business Intelligence

### UI Clickable Prototype
Figma: https://www.figma.com/file/tQe03Y1JbrqLyjgD8JXBKj/Review-Tracker

Description: When the user first enters our website, they are taken to the sign in screen where they can choose to either sign in to their existing account, or create a new account. Once they either sign in or create an account, they are taken to our homepage where they can enter the URL of a product that they wish to analyze. When they click analyze, they are then taken to the products page where they can view two different types of analyses for their product based off of its reviews. On the left, there is the categorical analysis with a chart representing how good or bad this product is for each of the categories we define. On the right, there is a historical analysis where we can see the ratings of various categories over time, or the ratings of the entire product over time. On the products page, the user can also toggle other products that they have entered into our website and view information about those products.

### API Description
Swagger: https://app.swaggerhub.com/apis/BORAELCI/ReviewInsights/v0

Editor: https://app.swaggerhub.com/apis/BORAELCI/ReviewInsights/v0#/

Our API captures the asynchronous flow of our service. A seller signs up and adds a new product. Once the product is added, a GatherReviewsOrder is pushed to an SQS queue. In the Gather Reviews stage, a Lambda function pulls the order and processes it. The e-commerce website is scraped and reviews are downloaded. These reviews are saved as a CSV file to an S3 bucket. Once the reviews are gathered, an ExtractInsightsOrder is pushed to an SQS queue. In the Extract Insights stage, a Lambda function pulls the order and processes it. The specific categories based on product type are determined and sentiment analysis on each review is performed. The results are stored in a DynamoDB table. Once the analysis is complete, a GenerateReportOrder is pushed to an SQS queue. In the Generate Report stage, a Lambda function pulls the order and processes it. QuickSight is used to visualize the data and a report is generated. The user is notified via SES that they are able to access the results through the frontend. This architecture leveraging multiple queues and worker Lambdas provides decoupling and improves the scalability of our service.

### Architecture Design Diagram

Lucidchart: https://lucid.app/lucidchart/e2dd37cd-5d81-422c-af4d-f32378ad1b24/edit

Need-to-have components (shown in diagram):
- S3: hosts frontend and stores review data
- API Gateway: connects S3 frontend and Lambda for handling requests
- Lambda: handles requests, gathers reviews, extracts insights, and generates reports
- SQS: gathers review order, extracts insights order, and generates review order
- DynamoDB: stores insight
- Amazon Comprehend (analyzing insights in texts)
- Amazon Translate (in case the reviews are in non-English languages)
- Amazon Recognition (images and video analysis). It’s for comments with images and videos
- SageMaker: trains ML models for extracting insights
- QuickSight: visualizes data and creates report
- SES: Emails user once data is prepared and UI is ready
- Nice-to-have components (not shown in diagram):
- GPT: sentiment analysis 
- IAM: ensures that only certain users can access their product’s insights
- CloudWatch: checks service performance with logs, metrics, and alarms
- CloudFormation: provisions infrastructure as code
- CloudFront: hosts the frontend and serves it to users
