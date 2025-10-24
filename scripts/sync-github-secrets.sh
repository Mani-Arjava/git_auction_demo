#!/bin/bash
# Script to sync .env file to GitHub repository secrets
# Usage: ./scripts/sync-github-secrets.sh

set -e

echo "🔐 Syncing .env to GitHub Secrets..."
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found in current directory"
    echo "   Please run this script from the project root"
    exit 1
fi

# Check if gh is installed
if ! command -v gh &> /dev/null; then
    echo "❌ Error: GitHub CLI (gh) is not installed"
    echo ""
    echo "Install it with:"
    echo "   brew install gh"
    echo ""
    echo "Or download from: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ Error: Not authenticated with GitHub CLI"
    echo ""
    echo "Please login first:"
    echo "   gh auth login"
    echo ""
    exit 1
fi

echo "✅ GitHub CLI authenticated"
echo ""

# Load .env file
echo "📖 Reading environment variables from .env..."
set -a
source .env
set +a
echo ""

# Define secrets to sync
declare -A SECRETS=(
    ["AWS_REGION"]="$AWS_REGION"
    ["LOG_LEVEL"]="$LOG_LEVEL"
    ["CORS_ORIGINS"]="${CORS_ORIGINS:-*}"
    ["SUPABASE_URL"]="$SUPABASE_URL"
    ["SUPABASE_ANON_KEY"]="$SUPABASE_ANON_KEY"
    ["SUPABASE_HOST"]="$SUPABASE_HOST"
    ["SUPABASE_USER"]="$SUPABASE_USER"
    ["SUPABASE_PASSWORD"]="$SUPABASE_PASSWORD"
    ["SUPABASE_PORT"]="$SUPABASE_PORT"
    ["SUPABASE_DATABASE"]="$SUPABASE_DATABASE"
    ["SUPABASE_USE_POOLER"]="$SUPABASE_USE_POOLER"
    ["AWS_ACCESS_KEY_ID"]="$AWS_ACCESS_KEY_ID"
    ["AWS_SECRET_ACCESS_KEY"]="$AWS_SECRET_ACCESS_KEY"
    ["AWS_S3_BUCKET"]="$AWS_S3_BUCKET"
    ["AWS_S3_BASE_URL"]="$AWS_S3_BASE_URL"
    ["BRANCH_BASE_URL"]="${BRANCH_BASE_URL:-}"
)

# Validate required secrets
MISSING_SECRETS=()
for key in "${!SECRETS[@]}"; do
    if [ -z "${SECRETS[$key]}" ] && [ "$key" != "BRANCH_BASE_URL" ]; then
        MISSING_SECRETS+=("$key")
    fi
done

if [ ${#MISSING_SECRETS[@]} -gt 0 ]; then
    echo "❌ Error: The following required secrets are missing or empty in .env:"
    for key in "${MISSING_SECRETS[@]}"; do
        echo "   - $key"
    done
    echo ""
    echo "Please check your .env file and ensure all required variables are set."
    exit 1
fi

# Show preview
echo "📋 Secrets to be uploaded to GitHub:"
echo ""
for key in "${!SECRETS[@]}"; do
    value="${SECRETS[$key]}"
    if [ -z "$value" ]; then
        echo "   ⚠️  $key: <empty>"
    elif [[ "$key" == *"PASSWORD"* ]] || [[ "$key" == *"SECRET"* ]] || [[ "$key" == *"KEY"* ]]; then
        echo "   ✅ $key: ******* (${#value} chars)"
    elif [ ${#value} -gt 40 ]; then
        echo "   ✅ $key: ${value:0:30}... (${#value} chars)"
    else
        echo "   ✅ $key: $value"
    fi
done
echo ""

read -p "Upload these secrets to GitHub? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Upload secrets to GitHub
echo ""
echo "🚀 Uploading secrets to GitHub..."
echo ""

SUCCESS_COUNT=0
FAIL_COUNT=0

for key in "${!SECRETS[@]}"; do
    value="${SECRETS[$key]}"

    # Skip empty optional secrets
    if [ -z "$value" ] && [ "$key" == "BRANCH_BASE_URL" ]; then
        echo "   ⏭️  Skipping $key (empty)"
        continue
    fi

    echo -n "   Setting $key... "

    if echo "$value" | gh secret set "$key" 2>/dev/null; then
        echo "✅"
        ((SUCCESS_COUNT++))
    else
        echo "❌"
        ((FAIL_COUNT++))
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo "✅ All secrets uploaded successfully! ($SUCCESS_COUNT secrets)"
    echo ""
    echo "📝 Next steps:"
    echo "   1. Verify secrets in GitHub:"
    echo "      https://github.com/Mani-Arjava/git_auction_demo/settings/secrets/actions"
    echo ""
    echo "   2. Trigger deployment by pushing to main:"
    echo "      git push origin main"
    echo ""
    echo "   3. Or trigger manually:"
    echo "      gh workflow run fly-deploy.yml"
    echo ""
    echo "   4. Watch deployment:"
    echo "      https://github.com/Mani-Arjava/git_auction_demo/actions"
    echo ""
    echo "🎉 Auto-deployment is now configured!"
else
    echo "⚠️  Upload completed with errors"
    echo "   Success: $SUCCESS_COUNT"
    echo "   Failed: $FAIL_COUNT"
    echo ""
    echo "Please check the errors above and try again."
    exit 1
fi
