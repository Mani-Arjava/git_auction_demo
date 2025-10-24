#!/bin/bash
# Verify deployment is working correctly

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "🔍 Verifying Phobos Backend Deployment"
echo "======================================"
echo ""

# Get API URL from CloudFormation
echo "${YELLOW}Getting API URL from CloudFormation...${NC}"
API_URL=$(aws cloudformation describe-stacks \
  --stack-name PythonLambdaStack \
  --profile ${AWS_PROFILE:-default} \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiUrl`].OutputValue' \
  --output text 2>/dev/null)

if [ -z "$API_URL" ]; then
    echo "${RED}❌ Could not find API URL. Is the stack deployed?${NC}"
    exit 1
fi

echo "${GREEN}✅ API URL: $API_URL${NC}"
echo ""

# Test endpoints
echo "${YELLOW}Testing endpoints...${NC}"
echo ""

# Test root
echo "1. Testing root endpoint (/)..."
RESPONSE=$(curl -s -w "\n%{http_code}" "$API_URL")
STATUS=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$STATUS" -eq 200 ]; then
    echo "${GREEN}✅ Root endpoint working${NC}"
    echo "   Response: $BODY"
else
    echo "${RED}❌ Root endpoint failed (HTTP $STATUS)${NC}"
    echo "   Response: $BODY"
fi
echo ""

# Test hello
echo "2. Testing hello endpoint (/hello)..."
RESPONSE=$(curl -s -w "\n%{http_code}" "${API_URL}hello")
STATUS=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$STATUS" -eq 200 ]; then
    echo "${GREEN}✅ Hello endpoint working${NC}"
    echo "   Response: $BODY"
else
    echo "${RED}❌ Hello endpoint failed (HTTP $STATUS)${NC}"
    echo "   Response: $BODY"
fi
echo ""

# Test hello with name
echo "3. Testing hello with name (/hello/TestUser)..."
RESPONSE=$(curl -s -w "\n%{http_code}" "${API_URL}hello/TestUser")
STATUS=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$STATUS" -eq 200 ] && echo "$BODY" | grep -q "TestUser"; then
    echo "${GREEN}✅ Hello with name working${NC}"
    echo "   Response: $BODY"
else
    echo "${RED}❌ Hello with name failed (HTTP $STATUS)${NC}"
    echo "   Response: $BODY"
fi
echo ""

# Test health
echo "4. Testing health endpoint (/health)..."
RESPONSE=$(curl -s -w "\n%{http_code}" "${API_URL}health")
STATUS=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$STATUS" -eq 200 ] && echo "$BODY" | grep -q "healthy"; then
    echo "${GREEN}✅ Health endpoint working${NC}"
    echo "   Response: $BODY"
else
    echo "${RED}❌ Health endpoint failed (HTTP $STATUS)${NC}"
    echo "   Response: $BODY"
fi
echo ""

# Test OpenAPI docs
echo "5. Testing OpenAPI docs (/openapi.json)..."
RESPONSE=$(curl -s -w "\n%{http_code}" "${API_URL}openapi.json")
STATUS=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$STATUS" -eq 200 ] && echo "$BODY" | grep -q "openapi"; then
    echo "${GREEN}✅ OpenAPI docs working${NC}"
    TITLE=$(echo "$BODY" | python3 -c "import sys, json; print(json.load(sys.stdin).get('info', {}).get('title', 'N/A'))" 2>/dev/null || echo "N/A")
    echo "   API Title: $TITLE"
else
    echo "${RED}❌ OpenAPI docs failed (HTTP $STATUS)${NC}"
fi
echo ""

echo "======================================"
echo "${GREEN}✅ Verification complete!${NC}"
echo ""
echo "📚 Documentation URLs:"
echo "   Swagger UI: ${API_URL}docs"
echo "   ReDoc:      ${API_URL}redoc"
echo ""
