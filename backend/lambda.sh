#!/bin/bash

AWS_ACCOUNT_ID=412391315699
ARTIFACTS_BUCKET_NAME=artifacts-$AWS_ACCOUNT_ID
FRONTEND_LAMBDA=frontend-lambda
GATHER_REVIEWS_LAMBDA=gather-reviews-lambda
EXTRACT_INSIGHTS_LAMBDA=extract-insights-lambda
GENERATE_REPORT_LAMBDA=generate-report-lambda

ERROR_MESSAGE="Please provide 1, 2, 3 or 4 for LF1, LF2, LF3 or LF4 respectively or a for ALL. Also, \n\t\t\t \
you can specify 'n' afterwards to not actually update the lambda function but only upload the zip to S3."

uploadLambda() {
	lambda=$1
	update=$2
  cd $lambda
	zip ../tmp/$lambda.zip *.py src/*
	cd ..
	aws s3 cp tmp/$lambda.zip s3://$ARTIFACTS_BUCKET_NAME/$lambda/lambda_function.zip

	if [ $update ]; then
		aws lambda update-function-code \
		--function-name $lambda \
		--s3-bucket $ARTIFACTS_BUCKET_NAME \
		--s3-key $lambda/lambda_function.zip
	fi
}

if [ -z "$1" ]; then
  echo -e "Error: No argument provided. $ERROR_MESSAGE"
  exit 1
fi

if [ "$2" == "n" ]; then
	update=false
else
	update=true
fi

rm -rf tmp
mkdir tmp

if [ "$1" == "1" ]; then
    uploadLambda $FRONTEND_LAMBDA $update
elif [ "$1" == "2" ]; then
    uploadLambda $GATHER_REVIEWS_LAMBDA $update
elif [ "$1" == "3" ]; then
    uploadLambda $EXTRACT_INSIGHTS_LAMBDA $update
elif [ "$1" == "4" ]; then
    uploadLambda $GENERATE_REPORTS_LAMBDA $update
elif [ "$1" == "a" ]; then
    uploadLambda $FRONTEND_LAMBDA $update
    uploadLambda $GATHER_REVIEWS_LAMBDA $update
		uploadLambda $EXTRACT_INSIGHTS_LAMBDA $update
	  uploadLambda $GENERATE_REPORTS_LAMBDA $update
else
  echo -e "Error: Invalid argument. $ERROR_MESSAGE"
	exit 1
fi

rm -rf tmp
