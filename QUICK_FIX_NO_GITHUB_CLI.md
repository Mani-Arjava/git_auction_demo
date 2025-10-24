# Quick Fix: Set Fly.io Secrets Without GitHub CLI

## Skip GitHub - Set Secrets Directly in Fly.io

You don't need to install GitHub CLI (`gh`). You can set secrets directly in Fly.io using `flyctl` which you already have.

---

## Simple Steps:

### 1. Run This One Command

```bash
./scripts/set-flyio-secrets.sh
```

That's it! This script:
- ✅ Reads your local `.env` file
- ✅ Sets all secrets directly in Fly.io app `gbauction`
- ✅ Only requires `flyctl` (no `gh` needed)
- ✅ Triggers automatic deployment with new secrets

### 2. What You'll See

```
🚀 Setting Fly.io secrets from .env file...

📖 Reading environment variables from .env...

✅ Environment variables loaded

📋 Variables to be set in Fly.io:
   - AWS_REGION: ap-south-1
   - LOG_LEVEL: INFO
   - SUPABASE_URL: https://itdpeuznyceklottqpaj...
   - SUPABASE_PASSWORD: ****
   ... (all variables with masked sensitive values)

Continue to set these secrets in Fly.io? (y/n) y

🔐 Setting secrets in Fly.io app 'gbauction'...
   This will trigger a deployment and may take a minute...

Release v2 created
==> Monitoring deployment

... (deployment progress) ...

✅ Secrets set successfully!
```

### 3. Verify Secrets Are Set

```bash
fly secrets list --app gbauction
```

Should show all 16 secrets with digests.

### 4. Check App Status

```bash
# Wait for deployment (1-2 minutes)
fly status --app gbauction

# Check logs
fly logs --app gbauction
```

Look for:
```
✅ Loaded environment variables from...
✅ Database engine created successfully...
```

### 5. Test Your API

```bash
curl https://gbauction.fly.dev/docs
```

Should return HTML (Swagger UI), **not** the database error!

Or visit: https://gbauction.fly.dev/docs

---

## What About GitHub Auto-Deploy?

**This solution sets secrets in Fly.io only**, so:

- ✅ Your app works **RIGHT NOW** on Fly.io
- ❌ GitHub Actions deployments still have empty secrets

**If you want auto-deploy from GitHub later:**
- Install `gh`: `brew install gh`
- Run: `./scripts/sync-github-secrets.sh`
- But that's optional - your app already works!

---

## Troubleshooting

### Script fails: "flyctl not found"

Install Fly.io CLI:
```bash
brew install flyctl
```

### Script fails: "Could not find App"

Create the app first:
```bash
fly apps create gbauction
```

Then run the script again.

### "Required variables are missing"

Check your `.env` file has all values:
```bash
grep -E "AWS_REGION|SUPABASE_URL|AWS_ACCESS_KEY" .env
```

Should show non-empty values.

### Secrets set but app still errors

Wait 2-3 minutes for deployment to complete:
```bash
fly status --app gbauction
```

Force restart if needed:
```bash
fly apps restart gbauction
```

---

## Manual Alternative

If the script doesn't work, set secrets manually (replace with your values from `.env`):

```bash
fly secrets set \
  AWS_REGION="ap-south-1" \
  LOG_LEVEL="INFO" \
  PYTHONPATH="/app" \
  CORS_ORIGINS="*" \
  SUPABASE_URL="https://itdpeuznyceklottqpaj.supabase.co" \
  SUPABASE_ANON_KEY="eyJhbGc..." \
  SUPABASE_HOST="aws-1-ap-south-1.pooler.supabase.com" \
  SUPABASE_USER="postgres.itdpeuznyceklottqpaj" \
  SUPABASE_PASSWORD="YTvctzA89M8a4wf6" \
  SUPABASE_PORT="5432" \
  SUPABASE_DATABASE="postgres" \
  SUPABASE_USE_POOLER="true" \
  AWS_ACCESS_KEY_ID="AKIA..." \
  AWS_SECRET_ACCESS_KEY="your-secret" \
  AWS_S3_BUCKET="phobosdev" \
  AWS_S3_BASE_URL="https://phobosdev.s3.ap-south-1.amazonaws.com" \
  --app gbauction
```

---

## Summary

**One command to fix everything:**

```bash
./scripts/set-flyio-secrets.sh
```

**Your app will work immediately** without needing GitHub CLI or GitHub secrets!

🎉 **No need to install `gh` at all if you just want the app to work on Fly.io!**
