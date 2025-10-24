#!/bin/bash
set -e

echo "🐍 Building Python FastAPI Lambda function..."

# Get script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Navigate to lambda directory
cd "$PROJECT_ROOT/lambda/phobos"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Generate requirements.txt if needed
echo "📦 Generating requirements.txt..."
uv pip compile pyproject.toml -o requirements.txt

# Clean previous build
echo "🧹 Cleaning previous build..."
rm -rf package
mkdir -p package

# Install dependencies to package directory for Linux ARM64 (Lambda runtime)
echo "📦 Installing dependencies for Linux ARM64 (Lambda runtime)..."
# Use --python-platform to install Linux ARM64 compatible packages
uv pip install -r requirements.txt --target package --python-platform aarch64-unknown-linux-gnu --python-version 3.12

# Copy application code to package directory
echo "📋 Copying application code..."
cp -r app package/

# Verify package contents
echo "✅ Package contents:"
ls -la package/ | head -10
echo ""

echo "✅ Python Lambda build complete!"
echo "📦 Package ready at: lambda/phobos/package/"

# Navigate to infrastructure directory
cd "$PROJECT_ROOT/infrastructure"

# Install CDK dependencies
echo "📦 Installing CDK dependencies..."
npm install

# Build TypeScript
echo "🔨 Building CDK TypeScript..."
npm run build

echo "✅ Infrastructure build complete!"
echo "🎉 Build process finished successfully!"
