# Supabase + AWS Lambda Setup Guide

This guide covers how to configure your Phobos FastAPI Lambda backend to work with Supabase database in both local development and AWS Lambda environments.

## 🏗️ Architecture Overview

```
Local Development    →    Supabase Direct Connection
AWS Lambda           →    Supabase Pooler Connection (Recommended)
```

## 🔧 Configuration Setup

### 1. Local Development Configuration

Edit your `.env` file in the project root:

```bash
# Local development - use direct connection
DB_HOST=db.your-project-ref.supabase.co
DB_USER=postgres
DB_PASSWORD=your-supabase-password
DB_PORT=5432
DB_NAME=postgres
```

### 2. AWS Lambda Configuration

Set these environment variables in your Lambda function:

```bash
# Lambda - use pooler connection (recommended)
SUPABASE_USER=postgres
SUPABASE_PASSWORD=your-supabase-password
SUPABASE_HOST=aws-0-us-west-1.pooler.supabase.co
SUPABASE_PORT=6543
SUPABASE_DATABASE=postgres
SUPABASE_USE_POOLER=true
```

## 📋 Getting Supabase Credentials

1. **Go to your Supabase project dashboard**
2. **Project Settings** → **Database**
3. **Connection parameters** contain your direct connection details
4. **Connection pooling** contains your pooler connection details

### Direct Connection String
```
postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

### Pooler Connection String (Recommended for Lambda)
```
postgresql://postgres:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
```

## 🚀 Deployment Options

### Option 1: Direct Connection (Simple Setup)
- **Use for:** Development, low-traffic applications
- **Pros:** Simple configuration
- **Cons:** Limited connection pool, potential connection limits

```bash
# Lambda Environment Variables
SUPABASE_HOST=db.your-project-ref.supabase.co
SUPABASE_PORT=5432
SUPABASE_USE_POOLER=false
```

### Option 2: Pooler Connection (Recommended for Production)
- **Use for:** Production Lambda, high-traffic applications
- **Pros:** Managed connection pool, better performance
- **Cons:** Slightly more complex setup

```bash
# Lambda Environment Variables
SUPABASE_HOST=aws-0-us-west-1.pooler.supabase.co
SUPABASE_PORT=6543
SUPABASE_USE_POOLER=true
```

## 🔒 Security Best Practices

### 1. Environment Variables
- Never commit credentials to Git
- Use AWS Secrets Manager for production secrets
- Rotate database passwords regularly

### 2. Network Security
- Enable VPC for Lambda if required
- Configure security groups to allow Lambda → Supabase traffic
- Use SSL/TLS connections (default in Supabase)

### 3. IAM Permissions
Your Lambda execution role needs:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}
```

## 🎯 Lambda Function Configuration

### Memory & Timeout
```bash
# Recommended settings for database operations
Memory: 512 MB - 1024 MB
Timeout: 30 seconds (adjust based on your queries)
```

### Environment Variables
Copy from `docs/lambda-environment-variables.env` and customize:
- Database connection settings
- AWS credentials
- API configuration

## 📊 Performance Optimization

### Connection Pool Settings
The application automatically configures optimal connection pool settings for Lambda:

```python
# db_config.py - Lambda optimized settings
engine = create_async_engine(
    connection_string,
    pool_size=5,           # Base connections
    max_overflow=10,       # Additional connections under load
    pool_timeout=30,       # Wait time for connection
    pool_recycle=3600,     # Recycle every hour
    connect_args={
        "command_timeout": 60,
        "server_settings": {
            "application_name": "phobos_lambda"
        }
    }
)
```

### Cold Start Optimization
- Keep Lambda warm with scheduled invocations
- Use provisioned concurrency for consistent performance
- Optimize imports and initialization code

## 🧪 Testing Configuration

### Local Testing
```bash
# Test local connection
cd lambda/phobos
uv run python -c "
import asyncio
from app.api.db_connection.db_connection import create_db_and_tables
asyncio.run(create_db_and_tables())
print('✅ Local connection successful!')
"
```

### Lambda Testing
```bash
# Test Lambda configuration
aws lambda invoke \
  --function-name your-phobos-function \
  --payload '{"httpMethod":"GET","path":"/health"}' \
  response.json
```

## 🚨 Troubleshooting

### Common Issues

1. **Connection Timeout**
   ```
   Error: asyncpg.exceptions.CannotConnectNowException
   ```
   **Solution:** Check security groups and VPC configuration

2. **Authentication Failed**
   ```
   Error: asyncpg.exceptions.InvalidPasswordError
   ```
   **Solution:** Verify Supabase credentials and user permissions

3. **Connection Pool Exhausted**
   ```
   Error: sqlalchemy.exc.TimeoutError
   ```
   **Solution:** Increase pool_size or use pooler connection

### Debug Mode
Enable debug logging:
```bash
LOG_LEVEL=DEBUG
```

### Health Check
Test database connectivity:
```bash
curl https://your-lambda-url/health
```

## 📚 Additional Resources

- [Supabase Database Documentation](https://supabase.com/docs/guides/database)
- [Supabase Connection Pooling](https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pooler)
- [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)

## 🔄 Next Steps

1. ✅ Set up Supabase project and get credentials
2. ✅ Configure local development environment
3. ✅ Set up Lambda function with environment variables
4. ✅ Test both local and Lambda connections
5. ✅ Deploy with CDK
6. ✅ Monitor performance and optimize as needed

## 💡 Pro Tips

- Use different Supabase projects for development and production
- Implement circuit breakers for database resilience
- Set up CloudWatch alerts for database connection errors
- Use Supabase's real-time features for live updates (optional)
- Consider Supabase Edge Functions for server-side logic closer to users