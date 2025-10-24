#!/bin/bash
set -e

echo "🔧 Deploying environment variables to Lambda..."

# Get script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Load .env file
ENV_FILE="$PROJECT_ROOT/.env"

if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Error: .env file not found at $ENV_FILE"
    exit 1
fi

echo "📄 Reading environment variables from $ENV_FILE"

# Extract AWS_PROFILE from .env file (don't source to avoid issues with spaces in values)
AWS_PROFILE=$(grep -E '^AWS_PROFILE=' "$ENV_FILE" | cut -d '=' -f 2- | xargs)

if [ -z "$AWS_PROFILE" ]; then
    echo "❌ Error: AWS_PROFILE not found in .env file"
    exit 1
fi

echo "🔑 Using AWS Profile: $AWS_PROFILE"

# Get Lambda function name from CDK output
echo "🔍 Finding Lambda function name..."
FUNCTION_NAME=$(aws cloudformation describe-stacks \
    --stack-name PythonLambdaStack \
    --profile "${AWS_PROFILE}" \
    --query 'Stacks[0].Outputs[?OutputKey==`LambdaFunctionName`].OutputValue' \
    --output text 2>/dev/null)

if [ -z "$FUNCTION_NAME" ]; then
    echo "❌ Error: Could not find Lambda function name. Make sure the stack is deployed first."
    echo "   Run 'make deploy' to deploy the stack."
    exit 1
fi

echo "✅ Found Lambda function: $FUNCTION_NAME"

# Parse .env file and build environment variables JSON
# Exclude: AWS_REGION, AWS_PROFILE, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
# AWS_REGION is automatically provided by Lambda and cannot be overridden
echo "📦 Preparing environment variables..."

ENV_JSON="{"
FIRST=true

while IFS='=' read -r key value; do
    # Skip comments, empty lines, and lines without =
    [[ "$key" =~ ^#.*$ ]] && continue
    [[ -z "$key" ]] && continue
    [[ -z "$value" ]] && continue

    # Trim whitespace
    key=$(echo "$key" | xargs)
    value=$(echo "$value" | xargs)

    # Skip excluded variables (reserved Lambda env vars and credentials)
    case "$key" in
        AWS_REGION|AWS_PROFILE|AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY)
            continue
            ;;
    esac

    # Add to JSON (escape special characters in value)
    if [ "$FIRST" = true ]; then
        ENV_JSON="$ENV_JSON\"$key\":\"$value\""
        FIRST=false
    else
        ENV_JSON="$ENV_JSON,\"$key\":\"$value\""
    fi
done < <(grep -v '^\s*#' "$ENV_FILE" | grep '=')

ENV_JSON="$ENV_JSON}"

echo "🚀 Updating Lambda environment variables..."

# Create temporary JSON file for AWS CLI
TEMP_JSON=$(mktemp)
echo "{\"Variables\":$ENV_JSON}" > "$TEMP_JSON"

# Update Lambda function configuration using file-based JSON
aws lambda update-function-configuration \
    --function-name "$FUNCTION_NAME" \
    --environment "file://$TEMP_JSON" \
    --profile "${AWS_PROFILE}" \
    > /dev/null

# Clean up temp file
rm -f "$TEMP_JSON"

echo ""
echo "✅ Environment variables deployed successfully!"
echo ""
echo "📋 Deployed variables:"
echo "$ENV_JSON" | jq -r 'keys[]' 2>/dev/null || echo "$ENV_JSON"
echo ""
echo "🔒 Security Note: AWS credentials are NOT deployed to Lambda."
echo "   Lambda uses IAM role permissions to access AWS services."
echo ""
