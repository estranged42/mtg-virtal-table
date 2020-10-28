#!/bin/bash

ENVIRONMENT=$1
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
source $SCRIPTPATH/env.sh

DISTRIBUTION_FOLDER=$SCRIPTPATH/../dist

if [ -d "$DISTRIBUTION_FOLDER" ]; then
    aws s3 sync --delete $DISTRIBUTION_FOLDER s3://$HOSTNAME
else 
    echo "$DISTRIBUTION_FOLDER does not exist. Run `yarn build` first"
fi


DISTRIBUTION_ID="$(get_stack_output $FRONTEND_STACK_NAME CloudFrontDistribution)"

INVALIDATION_ID=$(aws cloudfront create-invalidation \
    --query "Invalidation.Id" --output text \
    --distribution-id $DISTRIBUTION_ID \
    --paths "/*" \
    2>&1)

echo "Waiting for invalidation to complete... $INVALIDATION_ID"

aws cloudfront wait invalidation-completed \
    --distribution-id $DISTRIBUTION_ID \
    --id $INVALIDATION_ID
