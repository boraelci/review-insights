CLOUDFORMATION_TEMPLATE_PATH=cloudformation.yaml
CLOUDFORMATION_STACK_NAME=review-insights-stack

aws cloudformation deploy \
	--template-file $CLOUDFORMATION_TEMPLATE_PATH \
	--stack-name $CLOUDFORMATION_STACK_NAME \
	--capabilities CAPABILITY_NAMED_IAM \
