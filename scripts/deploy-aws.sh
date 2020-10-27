#!/bin/bash

ENVIRONMENT=$1
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
source $SCRIPTPATH/env.sh

aws cloudformation deploy \
--region "$AWS_REGION" \
--stack-name "$FRONTEND_STACK_NAME" \
--template-file /$SCRIPTPATH/../cf/website.yaml \
--parameter-overrides \
        "SiteName=$HOSTNAME" \
        "CertificateARN=$SSL_CERTIFICATE_ARN" \
