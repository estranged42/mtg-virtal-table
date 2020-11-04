#!/bin/bash

ENVIRONMENT=$1
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
BASE="$SCRIPTPATH/.."
source $SCRIPTPATH/env.sh

cd "$BASE/serverless/"

sls invoke local \
    --function $1 \
    --path "$BASE/serverless/events/form-post.json" \
    --docker

cd "$BASE"
