#!/bin/bash
# Script to set Fly.io secrets from local .env file
# Usage: ./scripts/set-flyio-secrets.sh

set -e

echo "🚀 Setting Fly.io secrets from .env file..."
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found in current directory"
    echo "   Please run this script from the project root"
    exit 1
fi

# Check if flyctl is installed
if ! command -v flyctl &> /dev/null; then
    echo "❌ Error: flyctl is not installed"
    echo "   Install it with: brew install flyctl"
    exit 1
fi

# Load .env file using source (more reliable than export $(grep...))
echo "📖 Reading environment variables from .env..."
set -a  # automatically export all variables
source .env
set +a  # stop auto-exporting

echo ""
echo "✅ Environment variables loaded"
echo ""

# Check if required variables are set
REQUIRED_VARS=(
    "AWS_REGION"
    "LOG_LEVEL"
    "SUPABASE_URL"
    "SUPABASE_ANON_KEY"
    "SUPABASE_HOST"
    "SUPABASE_USER"
    "SUPABASE_PASSWORD"
    "SUPABASE_PORT"
    "SUPABASE_DATABASE"
    "SUPABASE_USE_POOLER"
    "AWS_ACCESS_KEY_ID"
    "AWS_SECRET_ACCESS_KEY"
    "AWS_S3_BUCKET"
    "AWS_S3_BASE_URL"
)

MISSING_VARS=()
for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        MISSING_VARS+=("$var")
    fi
done

if [ ${#MISSING_VARS[@]} -gt 0 ]; then
    echo "❌ Error: The following required variables are missing or empty in .env:"
    for var in "${MISSING_VARS[@]}"; do
        echo "   - $var"
    done
    echo ""
    echo "Please check your .env file and ensure all required variables are set."
    exit 1
fi

# Show what will be set (masked for security)
echo "📋 Variables to be set in Fly.io:"
echo "   - AWS_REGION: $AWS_REGION"
echo "   - LOG_LEVEL: $LOG_LEVEL"
echo "   - PYTHONPATH: /app"
echo "   - API_TITLE: Phobos Backend API"
echo "   - API_VERSION: 1.0.0"
echo "   - CORS_ORIGINS: ${CORS_ORIGINS:-*}"
echo "   - SUPABASE_URL: ${SUPABASE_URL:0:30}..."
echo "   - SUPABASE_ANON_KEY: ${SUPABASE_ANON_KEY:0:20}..."
echo "   - SUPABASE_HOST: $SUPABASE_HOST"
echo "   - SUPABASE_USER: $SUPABASE_USER"
echo "   - SUPABASE_PASSWORD: ****"
echo "   - SUPABASE_PORT: $SUPABASE_PORT"
echo "   - SUPABASE_DATABASE: $SUPABASE_DATABASE"
echo "   - SUPABASE_USE_POOLER: $SUPABASE_USE_POOLER"
echo "   - AWS_ACCESS_KEY_ID: ${AWS_ACCESS_KEY_ID:0:8}..."
echo "   - AWS_SECRET_ACCESS_KEY: ****"
echo "   - AWS_S3_BUCKET: $AWS_S3_BUCKET"
echo "   - AWS_S3_BASE_URL: $AWS_S3_BASE_URL"
echo "   - BRANCH_BASE_URL: ${BRANCH_BASE_URL:-<not set>}"
echo ""

read -p "Continue to set these secrets in Fly.io? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Set Fly.io secrets
echo ""
echo "🔐 Setting secrets in Fly.io app 'gbauction'..."
echo "   This will trigger a deployment and may take a minute..."
echo ""

flyctl secrets set \
    AWS_REGION="$AWS_REGION" \
    LOG_LEVEL="$LOG_LEVEL" \
    PYTHONPATH="/app" \
    API_TITLE="Phobos Backend API" \
    API_VERSION="1.0.0" \
    CORS_ORIGINS="${CORS_ORIGINS:-*}" \
    SUPABASE_URL="$SUPABASE_URL" \
    SUPABASE_ANON_KEY="$SUPABASE_ANON_KEY" \
    SUPABASE_HOST="$SUPABASE_HOST" \
    SUPABASE_USER="$SUPABASE_USER" \
    SUPABASE_PASSWORD="$SUPABASE_PASSWORD" \
    SUPABASE_PORT="$SUPABASE_PORT" \
    SUPABASE_DATABASE="$SUPABASE_DATABASE" \
    SUPABASE_USE_POOLER="$SUPABASE_USE_POOLER" \
    AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
    AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
    AWS_S3_BUCKET="$AWS_S3_BUCKET" \
    AWS_S3_BASE_URL="$AWS_S3_BASE_URL" \
    BRANCH_BASE_URL="${BRANCH_BASE_URL:-}" \
    --app gbauction

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✅ Secrets set successfully!"
    echo ""
    echo "📝 The app is now deploying with new secrets..."
    echo "   This may take 1-2 minutes."
    echo ""
    echo "🔍 To verify secrets were set:"
    echo "   fly secrets list --app gbauction"
    echo ""
    echo "📊 To view deployment status:"
    echo "   fly status --app gbauction"
    echo ""
    echo "📋 To view logs:"
    echo "   fly logs --app gbauction"
    echo ""
    echo "🌐 Test your API:"
    echo "   curl https://gbauction.fly.dev/docs"
else
    echo ""
    echo "❌ Failed to set secrets (exit code: $EXIT_CODE)"
    echo "   Check the error message above for details."
    exit $EXIT_CODE
fi
