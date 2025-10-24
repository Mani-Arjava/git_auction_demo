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

# Load .env and extract values
echo "📖 Reading environment variables from .env..."

# Extract values from .env file
export $(grep -v '^#' .env | grep -v '^$' | xargs)

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
    echo "⚠️  Warning: The following variables are missing from .env:"
    for var in "${MISSING_VARS[@]}"; do
        echo "   - $var"
    done
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Set Fly.io secrets
echo ""
echo "🔐 Setting secrets in Fly.io app 'gbauction'..."
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

echo ""
echo "✅ Secrets set successfully!"
echo ""
echo "📝 Note: Setting secrets will trigger a deployment."
echo "   Your app will restart with the new environment variables."
echo ""
echo "🔍 To verify secrets were set:"
echo "   fly secrets list --app gbauction"
echo ""
echo "📊 To view deployment status:"
echo "   fly status --app gbauction"
echo ""
echo "📋 To view logs:"
echo "   fly logs --app gbauction"
