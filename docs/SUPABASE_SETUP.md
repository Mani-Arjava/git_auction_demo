# Supabase Setup Guide for Phobos Backend

## Overview
This guide explains how to configure Supabase credentials for the Phobos Backend Python FastAPI Lambda application.

## Prerequisites
- Supabase project created at https://supabase.com/dashboard
- Project URL: `https://itdpeuznyceklottqpaj.supabase.co`

## Step 1: Get Database Password

1. Go to [Supabase Dashboard](https://supabase.com/dashboard/project/itdpeuznyceklottqpaj/settings/database)
2. Scroll down to "Connection string" section
3. Click "Connect" button to reveal connection string
4. Copy the password from the connection string
5. The connection string format is: `postgresql://postgres:[PASSWORD]@db.itdpeuznyceklottqpaj.supabase.co:5432/postgres`

## Step 2: Update Local Environment

Update the `.env` file in the project root:

```bash
# Replace this line:
SUPABASE_PASSWORD=your-supabase-password-here

# With your actual password:
SUPABASE_PASSWORD=your-actual-supabase-password
```

## Step 3: Test Database Connection

After setting the password, test the connection:

```bash
cd lambda/phobos
uv run python -c "
from app.api.db_connection.db_config import engine
print('Database engine:', '✅ Connected' if engine else '❌ Not connected')
"
```

## Step 4: Lambda Deployment Configuration

For AWS Lambda deployment, you have two options:

### Option A: Update CDK Stack (Recommended)
Edit `infrastructure/lib/python-lambda-stack.ts` and replace:
```typescript
SUPABASE_PASSWORD: process.env.SUPABASE_PASSWORD || 'your-supabase-password-here',
```

### Option B: Use AWS Secrets Manager
1. Create a secret in AWS Secrets Manager with the Supabase password
2. Grant Lambda function access to the secret
3. Modify the code to fetch the secret at runtime

## Step 5: Environment Variables Reference

### Local Development (.env)
```bash
# Database Configuration
SUPABASE_HOST=db.itdpeuznyceklottqpaj.supabase.co
SUPABASE_USER=postgres
SUPABASE_PASSWORD=your-actual-password
SUPABASE_PORT=5432
SUPABASE_DATABASE=postgres
SUPABASE_USE_POOLER=false

# API Configuration
SUPABASE_URL=https://itdpeuznyceklottqpaj.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml0ZHBldXpueWNla2xvdHRxcGFqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk4ODQwNzcsImV4cCI6MjA3NTQ2MDA3N30.PEikOnGSrTbMscsJCem79cfTy7Ye3NOzCMuM5AfH9Vg
```

### Lambda Environment Variables
The Lambda function automatically receives these variables from the CDK stack configuration.

## Step 6: Connection Pooling (Optional)

For production, consider using Supabase pooler:

```bash
# Update to use pooler (recommended for Lambda)
SUPABASE_HOST=aws-0-us-west-1.pooler.supabase.co
SUPABASE_PORT=6543
SUPABASE_USE_POOLER=true
```

## Step 7: Test Local Development Server

```bash
make test-local
```

The server should start at http://localhost:8000 with database connectivity.

## Troubleshooting

### Issue: "Database connection not configured"
- **Cause**: Missing or incorrect SUPABASE_PASSWORD
- **Fix**: Update .env file with correct password from Supabase dashboard

### Issue: "FATAL: password authentication failed"
- **Cause**: Incorrect password
- **Fix**: Reset password in Supabase dashboard > Database Settings

### Issue: Connection timeouts
- **Cause**: Network issues or incorrect host/port
- **Fix**: Verify SUPABASE_HOST and SUPABASE_PORT values

### Issue: Lambda function can't connect to database
- **Cause**: Environment variables not properly set in Lambda
- **Fix**: Update CDK stack and redeploy, or use AWS Secrets Manager

## Security Notes

- Never commit actual passwords to version control
- Use AWS Secrets Manager for production deployments
- Consider using connection pooling for better performance
- Enable SSL for all database connections (default with Supabase)

## Database Schema

The current database schema includes these tables:
- `appraiser` - Appraiser information
- `reappraisal_service` - Reappraisal services
- `reappraisal_service_advance` - Advances for services
- `reappraisal_service_reimbursement` - Reimbursements
- `payout_cycle` - Payout cycles
- `payout_statement` - Payout statements
- `advance_settlement` - Advance settlements
- `charge_settlement` - Charge settlements
- `reimbursement_settlement` - Reimbursement settlements

## Next Steps

1. Set your actual Supabase password in the .env file
2. Test the database connection locally
3. Run `make build && make deploy` to deploy to Lambda
4. Verify the deployment using the provided API URL