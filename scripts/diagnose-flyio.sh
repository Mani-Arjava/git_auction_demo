#!/bin/bash
# Diagnostic script to troubleshoot Fly.io secrets issue
# Usage: ./scripts/diagnose-flyio.sh

echo "🔍 Diagnosing Fly.io setup..."
echo ""

# Check if flyctl is installed
if ! command -v flyctl &> /dev/null; then
    echo "❌ flyctl is not installed"
    exit 1
fi

# Check authentication
echo "1️⃣  Checking Fly.io authentication..."
flyctl auth whoami
echo ""

# List all apps
echo "2️⃣  Listing all your Fly.io apps..."
flyctl apps list
echo ""

# Check if gbauction app exists
echo "3️⃣  Checking if 'gbauction' app exists..."
if flyctl status --app gbauction &> /dev/null; then
    echo "✅ App 'gbauction' exists"
    echo ""
    echo "App details:"
    flyctl status --app gbauction
    echo ""
else
    echo "❌ App 'gbauction' does NOT exist"
    echo ""
    echo "You need to create the app first:"
    echo "   fly apps create gbauction"
    echo ""
    echo "Or if you want to specify an organization:"
    echo "   fly apps create gbauction --org your-org-name"
    echo ""
    exit 1
fi

# Try to list secrets
echo "4️⃣  Listing current secrets..."
flyctl secrets list --app gbauction
echo ""

# Try setting a test secret
echo "5️⃣  Testing secret setting (will set a test secret)..."
echo "   Setting TEST_DIAGNOSTIC=working..."
flyctl secrets set TEST_DIAGNOSTIC="working" --app gbauction
TEST_EXIT_CODE=$?
echo ""

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✅ Test secret set successfully!"
    echo ""
    echo "Verifying..."
    flyctl secrets list --app gbauction
    echo ""

    # Remove test secret
    echo "Removing test secret..."
    flyctl secrets unset TEST_DIAGNOSTIC --app gbauction
    echo ""

    echo "✅ Diagnosis complete - everything looks good!"
    echo ""
    echo "You can now run: ./scripts/set-flyio-secrets.sh"
else
    echo "❌ Failed to set test secret (exit code: $TEST_EXIT_CODE)"
    echo ""
    echo "This indicates a problem with Fly.io secrets functionality."
    echo "Please check:"
    echo "  - You have permissions for this app"
    echo "  - The app is in the correct organization"
    echo "  - Your Fly.io auth token is valid"
fi
