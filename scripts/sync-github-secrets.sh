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

# Check if authenticated (more robust check)
echo "🔑 Checking GitHub CLI authentication..."
if ! gh auth status 2>&1 | grep -q "Logged in"; then
    echo ""
    echo "❌ Error: Not authenticated with GitHub CLI"
    echo ""
    echo "Current status:"
    gh auth status 2>&1 || true
    echo ""
    echo "Please login first:"
    echo "   gh auth login"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Show who is logged in
GITHUB_USER=$(gh api user --jq .login 2>/dev/null || echo "unknown")
echo "✅ Authenticated as: $GITHUB_USER"
echo ""

# Verify we can access the repository
echo "🔍 Verifying repository access..."
if ! gh repo view Mani-Arjava/git_auction_demo &> /dev/null; then
    echo "❌ Error: Cannot access repository 'Mani-Arjava/git_auction_demo'"
    echo ""
    echo "Please check:"
    echo "  - You're logged in to the correct GitHub account"
    echo "  - You have access to this repository"
    echo "  - Repository name is correct"
    echo ""
    exit 1
fi
echo "✅ Repository access confirmed"
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

    # Capture error output
    ERROR_OUTPUT=$(echo "$value" | gh secret set "$key" --repo Mani-Arjava/git_auction_demo 2>&1)
    EXIT_CODE=$?

    if [ $EXIT_CODE -eq 0 ]; then
        echo "✅"
        ((SUCCESS_COUNT++))
    else
        echo "❌"
        echo "      Error: $ERROR_OUTPUT"
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
