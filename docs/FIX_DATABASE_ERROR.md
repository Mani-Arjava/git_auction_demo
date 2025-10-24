# Fix "Database connection not configured" Error

## The Problem

When you call your API at https://gbauction.fly.dev, you get:
```json
{"detail":"Database connection not configured. Please set up database environment variables."}
```

This happens because the environment variables (database credentials, AWS keys, etc.) are not available in the Fly.io deployment.

## Why It Happens

Your app loads environment variables from a `.env` file (via `python-dotenv`). However:

1. **The `.env` file in Docker image is created from GitHub secrets**
2. **You haven't added GitHub secrets yet** → Empty `.env` file → No database config

## Solution: Set Fly.io Secrets

### Quick Fix (Recommended - Works Immediately)

Use the automated script to set all secrets from your local `.env`:

```bash
# From project root directory
./scripts/set-flyio-secrets.sh
```

This script will:
- ✅ Read your local `.env` file
- ✅ Set all secrets in Fly.io app
- ✅ Trigger automatic redeployment
- ✅ Your app will have working database connection

**Note:** Setting secrets triggers a deployment, so your app will restart automatically.

---

### Manual Method (If you prefer)

Set secrets one by one using `flyctl`:

```bash
# Set all required secrets (copy values from your .env file)
fly secrets set \
  AWS_REGION="ap-south-1" \
  LOG_LEVEL="INFO" \
  PYTHONPATH="/app" \
  CORS_ORIGINS="*" \
  SUPABASE_URL="https://itdpeuznyceklottqpaj.supabase.co" \
  SUPABASE_ANON_KEY="your-anon-key" \
  SUPABASE_HOST="aws-1-ap-south-1.pooler.supabase.com" \
  SUPABASE_USER="postgres.itdpeuznyceklottqpaj" \
  SUPABASE_PASSWORD="YTvctzA89M8a4wf6" \
  SUPABASE_PORT="5432" \
  SUPABASE_DATABASE="postgres" \
  SUPABASE_USE_POOLER="true" \
  AWS_ACCESS_KEY_ID="your-aws-key" \
  AWS_SECRET_ACCESS_KEY="your-aws-secret" \
  AWS_S3_BUCKET="phobosdev" \
  AWS_S3_BASE_URL="https://phobosdev.s3.ap-south-1.amazonaws.com" \
  --app gbauction
```

---

## Verify Secrets Are Set

After setting secrets:

### 1. List secrets (names only, values are hidden):
```bash
fly secrets list --app gbauction
```

Expected output:
```
NAME                      DIGEST                           DATE
AWS_ACCESS_KEY_ID         xxxxx...                         1m ago
AWS_REGION                xxxxx...                         1m ago
AWS_S3_BUCKET             xxxxx...                         1m ago
...
```

### 2. Check deployment status:
```bash
fly status --app gbauction
```

Wait for status to show "running" (may take 1-2 minutes).

### 3. View logs:
```bash
fly logs --app gbauction
```

Look for:
```
✅ Loaded environment variables from...
✅ Database engine created successfully...
✅ S3 client created...
```

### 4. Test API:
```bash
curl https://gbauction.fly.dev/docs
```

Should return the FastAPI Swagger UI (not the database error).

---

## Understanding How Secrets Work in Fly.io

### Fly.io Secrets vs .env File

**Two ways to set environment variables:**

1. **Fly.io Secrets** (Recommended for production)
   - Set using `fly secrets set`
   - Stored securely in Fly.io
   - Available as environment variables at runtime
   - Survives deployments

2. **.env File in Docker Image** (Used in our current setup)
   - Created during GitHub Actions workflow
   - Baked into Docker image
   - Loaded by `python-dotenv` in code

**Current Issue:** The `.env` file is created from GitHub secrets, but GitHub secrets are empty.

**Solution:** Either:
- Set Fly.io secrets directly (what we just did ✓)
- OR add GitHub secrets (for future CI/CD auto-deploys)

---

## For Future: Enable Auto-Deploy with GitHub Secrets

To make auto-deployment work (push to GitHub → auto-deploy to Fly.io):

### Add GitHub Secrets

Go to: https://github.com/Mani-Arjava/git_auction_demo/settings/secrets/actions

Add all 16 secrets listed in `docs/GITHUB_SECRETS_SETUP.md`.

Once added, every push to `main` will:
1. Create `.env` from GitHub secrets
2. Build Docker image with `.env`
3. Deploy to Fly.io

---

## Troubleshooting

### Secrets set but still getting error?

**Check if app restarted:**
```bash
fly status --app gbauction
```

**Force restart if needed:**
```bash
fly apps restart gbauction
```

**Wait 1-2 minutes** for deployment to complete.

### "fly: command not found"

Install Fly.io CLI:
```bash
brew install flyctl
```

### "Could not find App"

Make sure you're logged in:
```bash
fly auth login
```

### Secrets show in list but app still errors

The app might be loading `.env` file instead of environment variables. Check logs:
```bash
fly logs --app gbauction
```

Look for:
```
⚠️  .env file not found
```

This is actually GOOD - it means the app will fall back to reading from environment variables (Fly.io secrets).

---

## Summary

**Quick fix:**
```bash
./scripts/set-flyio-secrets.sh
```

**Verify:**
```bash
fly secrets list --app gbauction
fly status --app gbauction
fly logs --app gbauction
curl https://gbauction.fly.dev/docs
```

**Your database connection should now work!** 🎉
