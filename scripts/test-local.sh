#!/bin/bash
set -e

echo "🧪 Starting local FastAPI development server..."

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

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    uv venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
uv pip install -r requirements.txt --quiet

echo ""
echo "✅ Server starting on http://localhost:8000"
echo ""
echo "📚 API Documentation available at:"
echo "   • Swagger UI: http://localhost:8000/docs"
echo "   • ReDoc:      http://localhost:8000/redoc"
echo ""
echo "🧪 Test endpoints:"
echo "   • curl http://localhost:8000/"
echo "   • curl http://localhost:8000/getall"
echo "   • curl http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run uvicorn directly
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
