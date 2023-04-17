AWS_ACCOUNT_ID=412391315699
ARTIFACTS_BUCKET_NAME=artifacts-$AWS_ACCOUNT_ID
GATHER_REVIEWS_LAMBDA_PATH=frontend-lambda

mkdir tmp

cd $GATHER_REVIEWS_LAMBDA_PATH
echo "# Assuming you already uploaded the lambda layer #"
zip ../tmp/$GATHER_REVIEWS_LAMBDA_PATH.zip *.py src/*
cd ..
aws s3 cp tmp/$GATHER_REVIEWS_LAMBDA_PATH.zip s3://$ARTIFACTS_BUCKET_NAME/$GATHER_REVIEWS_LAMBDA_PATH/lambda_function.zip

rm -rf tmp
