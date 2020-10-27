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
