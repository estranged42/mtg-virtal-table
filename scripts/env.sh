#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
ENVIRONMENT=$1

echo ""

if [ "$ENVIRONMENT" == "prd" ]
then
    export ENVIRONMENT="prd"
    ENVIRONMENT_FILE="$SCRIPTPATH/../environment-prd.sh"
    SECRETS_FILE="$SCRIPTPATH/../secrets-prd.sh"
else
    export ENVIRONMENT="dev"
    ENVIRONMENT_FILE="$SCRIPTPATH/../environment-dev.sh"
    SECRETS_FILE="$SCRIPTPATH/../secrets-dev.sh"
fi

if [ -f "$ENVIRONMENT_FILE" ]; then
    source "$ENVIRONMENT_FILE"
else
    echo "⛔️ Environment File Not Found: $ENVIRONMENT_FILE"
    echo ""
    exit 1
fi

export AWS_REGION=us-west-2
export AWS_PROFILE="$AWS_CLI_PROFILE"

# What version of the AWS CLI do we have? certain cmds differs between 1 and 2
AWS_CLI_VERSION_STRING=$(aws --version)
if [[ $AWS_CLI_VERSION_STRING == *"aws-cli/2"* ]]; then
    AWS_CLI_VERSION=2
    # Disable output paging
    export AWS_PAGER=""
else
    AWS_CLI_VERSION=1
fi

# If we have a set of valid AWS credentials loaded, this sts call should return the ARN of the active user
# ie: arn:aws:sts::XYZ123:assumed-role/fdn-SuperAdmin/fischerm@arizona.edu
AUTH_USER_ID=$(aws sts get-caller-identity --output text --query "Arn" 2>&1)
if [[ $AUTH_USER_ID != *"arn:aws"* ]]; then
    echo "⛔️ AWS Authentication failed"
    echo "   Be sure an environment file exists and you have an active AWS CLI session / credentials"
    echo ""
    exit 1
fi


get_stack_export () {
    EXPORTNAME=$1
    echo "$(aws cloudformation list-exports --query "Exports[?Name==\`$EXPORTNAME\`].Value" --output text 2>&1)"
}

get_stack_output () {
    STACKNAME=$1
    OUTPUTKEY=$2
    echo "$(aws cloudformation describe-stacks --stack-name "$STACKNAME" --query "Stacks[0].Outputs[?OutputKey==\`$OUTPUTKEY\`].OutputValue" --output text 2>&1)"
}

get_ssm_param () {
    PARAMNAME=$1
    echo "$(aws ssm get-parameter --name $PARAMNAME --with-decryption --output text --query 'Parameter.[Value]' 2>&1)"
}

ACCOUNT_NAME=$(aws iam list-account-aliases --query 'AccountAliases[0]' --output text)
ACCOUNT_NUMBER=$(aws sts get-caller-identity --output text --query "Account")
CLOUDFORMATION_DEPLOY_ROLE=$(get_stack_export fdn-iam-cloudformation-deployer-role-arn)


if [ -f "$SECRETS_FILE" ]; then
    source "$SECRETS_FILE"
else
    if [ "$REQUIRE_SECRETS_FILE" == "true" ]
    then
        echo "⛔️ Secrets File Not Found: $SECRETS_FILE"
        echo ""
        exit 1
    fi
fi

echo ""
echo "=============================================================================="
echo "  $ACCOUNT_NAME"
echo "  $ACCOUNT_NUMBER"
echo "  $AUTH_USER_ID"
echo "  $ENVIRONMENT_FILE"
echo "=============================================================================="
echo ""

if [ "$ACCOUNT_NUMBER" != "$ACCOUNT_NUMBER_CHECK" ]; then
    echo "⛔️ Environment file ACCOUNT_NUMBER_CHECK does not match ACCOUNT_NUMBER"
    echo "   ACCOUNT_NUMBER: $ACCOUNT_NUMBER"
    echo "   ACCOUNT_NUMBER_CHECK: $ACCOUNT_NUMBER_CHECK"
    echo ""
    exit 1
fi
