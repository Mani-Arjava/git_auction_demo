# Phobos Backend API Documentation

## Overview

The Phobos Backend API is a production-ready FastAPI application deployed on AWS Lambda with API Gateway.

## Base URL

**Local Development:** `http://localhost:8000`
**Production:** `https://your-api-id.execute-api.region.amazonaws.com/prod`

## Authentication

Currently, the API is open. For production use, consider implementing:
- API Keys
- JWT Authentication
- AWS IAM Authentication

## Endpoints

### Root Endpoint

**GET /**

Returns basic API information.

**Response:**
```json
{
  "message": "Welcome to Phobos Backend API",
  "version": "1.0.0",
  "status": "healthy"
}
```

---

### Health Check

**GET /health**

Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "service": "phobos-backend"
}
```

---

### Hello (Default)

**GET /hello**

Returns a default greeting message.

**Response:**
```json
{
  "message": "Hello from Phobos Backend!",
  "name": "World"
}
```

---

### Hello (Personalized)

**GET /hello/{name}**

Returns a personalized greeting.

**Path Parameters:**
- `name` (string, required): The name to greet

**Example Request:**
```bash
curl https://api.example.com/hello/Alice
```

**Response:**
```json
{
  "message": "Hello, Alice!",
  "name": "Alice"
}
```

**Error Response (400):**
```json
{
  "detail": "Name cannot be empty"
}
```

---

### API Documentation

**GET /docs**

Interactive Swagger UI documentation.

**GET /redoc**

Alternative ReDoc documentation.

**GET /openapi.json**

OpenAPI schema in JSON format.

---

## Response Formats

All responses are in JSON format with appropriate HTTP status codes.

### Success Response

- **200 OK**: Request successful
- **201 Created**: Resource created
- **204 No Content**: Successful with no response body

### Error Response

- **400 Bad Request**: Invalid request parameters
- **404 Not Found**: Resource not found
- **405 Method Not Allowed**: HTTP method not supported
- **500 Internal Server Error**: Server error

---

## CORS

The API supports Cross-Origin Resource Sharing (CORS) with the following configuration:

- **Allowed Origins:** `*` (configurable)
- **Allowed Methods:** All
- **Allowed Headers:** `Content-Type`, `Authorization`, `X-Requested-With`, `Accept`
- **Credentials:** Enabled

---

## Rate Limiting

Currently not implemented. Consider adding rate limiting for production:

- AWS API Gateway throttling
- Lambda concurrency limits
- Application-level rate limiting

---

## Examples

### cURL Examples

```bash
# Root endpoint
curl https://api.example.com/

# Health check
curl https://api.example.com/health

# Hello endpoints
curl https://api.example.com/hello
curl https://api.example.com/hello/World

# API documentation
curl https://api.example.com/openapi.json
```

### Python Examples

```python
import requests

# Root endpoint
response = requests.get("https://api.example.com/")
print(response.json())

# Hello with name
response = requests.get("https://api.example.com/hello/Alice")
print(response.json())
```

### JavaScript Examples

```javascript
// Using fetch
const response = await fetch("https://api.example.com/hello/Alice");
const data = await response.json();
console.log(data);

// Using axios
const { data } = await axios.get("https://api.example.com/hello/Alice");
console.log(data);
```

---

## Adding New Endpoints

To add new endpoints:

1. Define route in `lambda/phobos/app/api/routes.py`
2. Create Pydantic models for request/response validation
3. Add tests in `tests/`
4. Update this documentation
5. Deploy with `make deploy`

Example:

```python
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    # Implementation
    return UserResponse(id=user_id, name="John", email="john@example.com")
```

---

## Performance

- **Cold Start:** ~150-250ms
- **Warm Response:** <10ms
- **Memory:** 512MB
- **Timeout:** 30 seconds
- **Architecture:** ARM64 (Graviton2)

---

## Monitoring

### CloudWatch Logs

```bash
# View Lambda logs
aws logs tail /aws/lambda/PythonLambdaStack-PhobosLambda --follow

# Filter errors
aws logs filter-pattern /aws/lambda/PythonLambdaStack-PhobosLambda --filter-pattern "ERROR"
```

### CloudWatch Metrics

Key metrics to monitor:
- Invocations
- Errors
- Duration
- Throttles
- Concurrent executions

---

## Support

For issues or questions, please contact the development team or create an issue in the repository.
