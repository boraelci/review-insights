import json
import boto3

def lambda_handler(event, context):
    
    # create an SQS client
    sqs = boto3.client('sqs')
    
    queue_url = "https://sqs.us-east-1.amazonaws.com/412391315699/GatherReviewsOrder"
    params = event["queryStringParameters"]
    print(params)
    
    body = {}
    # push a message to the SQS queue
    sqs.send_message(QueueUrl=queue_url, MessageBody=body)
    
    
    
    
    
    ### dynamodb stuff below ###
    
    dynamodb = boto3.client('dynamodb')
    
    # specify the table name
    table_name = 'Insights_1'
    product_id = 'airpods'
    
    # specify the query parameters
    query_params = {
        'TableName': table_name,
        'KeyConditionExpression': 'product_id = :pk',
        'ExpressionAttributeValues': {
            ':pk': {'S': product_id}
        }
    }
    
    # execute the query
    query_response = dynamodb.query(**query_params)
    
    # return the results
    data = query_response['Items']
    
    ret = {}
    ret['product_id'] = product_id
    
    for r in data:
        if r['insight_name']['S'] == 'average_stars_over_time':
            # dictionary = {}
            # dvalue = {}
            # jd = json.loads(r['data']['S'])
            # #return jd['stars']
            # for i in range(len(jd['stars'])):
            #     dvalue[jd['dates'][i]] = jd['stars'][i]
            
            # dictionary['average_stars_over_time'] = dvalue
            # ret.append(dictionary)
            continue
            
        if r['insight_name']['S'] == 'average_stars_per_category':
            dictionary = {}
            dvalue = {}
            jd = json.loads(r['data']['S'])
            for i in range(len(jd['positive'])):
                dvalue[jd['dates'][i]] = jd['positive'][i]
            
            ret['categorical_data'] = {}
            new_data = [{"category": category, "count": str(count)} for category, count in dvalue.items()]
            ret['historical_data']['positive'] = new_data
            
            dictionary = {}
            dvalue = {}
            jd = json.loads(r['data']['S'])
            for i in range(len(jd['negative'])):
                dvalue[jd['dates'][i]] = jd['negative'][i]
            
            new_data = [{"category": category, "count": str(count)} for category, count in dvalue.items()]
            ret['historical_data']['negative'] = new_data
            
        if r['insight_name']['S'] == 'sentiments_over_time':
            dictionary = {}
            dvalue = {}
            jd = json.loads(r['data']['S'])
            for i in range(len(jd['positive'])):
                dvalue[jd['dates'][i]] = jd['positive'][i]
            
            ret['historical_data'] = {}
            new_data = [{"date": date, "count": str(count)} for date, count in dvalue.items()]
            ret['historical_data']['positive'] = new_data
    
            dictionary = {}
            dvalue = {}
            jd = json.loads(r['data']['S'])
            for i in range(len(jd['negative'])):
                dvalue[jd['dates'][i]] = jd['negative'][i]
            
            new_data = [{"date": date, "count": str(count)} for date, count in dvalue.items()]
            ret['historical_data']['negative'] = new_data
    
    return {
        'statusCode': 200,
        'body': ret
    }
