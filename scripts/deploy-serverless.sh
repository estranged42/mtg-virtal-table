#!/bin/bash

ENVIRONMENT=$1
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
BASE="$SCRIPTPATH/.."
source $SCRIPTPATH/env.sh

cd "$BASE/serverless/"

sls deploy

cd "$BASE"
