#!/usr/bin/env python3
"""
Test Lambda handler locally to debug issues
"""
import sys
import os

# Add package directory to path (simulates Lambda environment)
package_dir = os.path.join(
    os.path.dirname(__file__), "..", "lambda", "phobos", "package"
)
sys.path.insert(0, package_dir)

print(f"Python path: {sys.path[0]}")
print(f"Package dir exists: {os.path.exists(package_dir)}")
print(f"App dir exists: {os.path.exists(os.path.join(package_dir, 'app'))}")
print()

try:
    # Import the handler (what Lambda does)
    from app.main import handler

    print("✅ Successfully imported handler")
    print(f"Handler type: {type(handler)}")
    print()

    # Test with a simple API Gateway event
    test_event = {
        "httpMethod": "GET",
        "path": "/",
        "headers": {},
        "queryStringParameters": None,
        "body": None,
        "isBase64Encoded": False,
        "requestContext": {"requestId": "test-request-id"},
    }

    print("Testing handler with GET / request...")
    response = handler(test_event, {})

    print(f"✅ Handler executed successfully!")
    print(f"Status Code: {response.get('statusCode')}")
    print(f"Body: {response.get('body')}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
