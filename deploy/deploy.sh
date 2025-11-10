#!/bin/bash
# Deployment script for Rift Rewind

set -e

ENVIRONMENT=${1:-development}
STACK_NAME="rift-rewind-${ENVIRONMENT}"

echo "Deploying Rift Rewind to ${ENVIRONMENT}..."

# Package and deploy CloudFormation stack
aws cloudformation package \
    --template-file deploy/cloudformation.yaml \
    --s3-bucket ${DEPLOYMENT_BUCKET} \
    --output-template-file deploy/packaged-template.yaml

aws cloudformation deploy \
    --template-file deploy/packaged-template.yaml \
    --stack-name ${STACK_NAME} \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides Environment=${ENVIRONMENT} \
    --tags rift-rewind-hackathon=2025

echo "Deployment complete!"

