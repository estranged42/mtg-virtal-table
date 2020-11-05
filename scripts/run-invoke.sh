#!/bin/bash

ENVIRONMENT=$1
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
BASE="$SCRIPTPATH/.."
source $SCRIPTPATH/env.sh

cd "$BASE/serverless/"

sls invoke local \
    --function $1 \
    --path "$BASE/serverless/events/connect.json" \
    --env AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    --env AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    --env GAMETABLE=$DYNAMODB_TABLE \
    --env APIGATEWAY_ENDPOINT="https://5mz965txnl.execute-api.us-west-2.amazonaws.com/dev" \
    --docker

cd "$BASE"
