# Manual Fly.io Secrets Setup (Step-by-Step)

## If Automated Script Fails

If `./scripts/set-flyio-secrets.sh` doesn't work, follow these manual steps.

---

## Step 1: Diagnose the Issue

Run the diagnostic script:

```bash
./scripts/diagnose-flyio.sh
```

This will:
- ✅ Check if you're logged in
- ✅ List all your apps
- ✅ Verify `gbauction` app exists
- ✅ Test setting a secret
- ✅ Show you exactly what's wrong

---

## Step 2: Verify App Exists

```bash
fly apps list
```

**If `gbauction` is NOT in the list:**

```bash
# Create the app
fly apps create gbauction

# Or specify organization if you have multiple
fly apps create gbauction --org your-org-name
```

**If app exists, check its status:**

```bash
fly status --app gbauction
```

---

## Step 3: Set Secrets One by One

If bulk setting fails, set secrets individually to see which one causes issues:

### Copy values from your .env file and run these commands:

```bash
# Application Config
fly secrets set AWS_REGION="ap-south-1" --app gbauction
fly secrets set LOG_LEVEL="INFO" --app gbauction
fly secrets set PYTHONPATH="/app" --app gbauction
fly secrets set API_TITLE="Phobos Backend API" --app gbauction
fly secrets set API_VERSION="1.0.0" --app gbauction
fly secrets set CORS_ORIGINS="*" --app gbauction

# Supabase Config (replace with YOUR values from .env)
fly secrets set SUPABASE_URL="https://itdpeuznyceklottqpaj.supabase.co" --app gbauction
fly secrets set SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." --app gbauction
fly secrets set SUPABASE_HOST="aws-1-ap-south-1.pooler.supabase.com" --app gbauction
fly secrets set SUPABASE_USER="postgres.itdpeuznyceklottqpaj" --app gbauction
fly secrets set SUPABASE_PASSWORD="YTvctzA89M8a4wf6" --app gbauction
fly secrets set SUPABASE_PORT="5432" --app gbauction
fly secrets set SUPABASE_DATABASE="postgres" --app gbauction
fly secrets set SUPABASE_USE_POOLER="true" --app gbauction

# AWS Config (replace with YOUR values from .env)
fly secrets set AWS_ACCESS_KEY_ID="AKIA..." --app gbauction
fly secrets set AWS_SECRET_ACCESS_KEY="your-secret-key" --app gbauction
fly secrets set AWS_S3_BUCKET="phobosdev" --app gbauction
fly secrets set AWS_S3_BASE_URL="https://phobosdev.s3.ap-south-1.amazonaws.com" --app gbauction

# Optional
fly secrets set BRANCH_BASE_URL="http://localhost:8000" --app gbauction
```

### After Each Command:
- ✅ Check if it succeeded (no error message)
- ✅ Note which secret failed if any error occurs

### Note About Deployments:
**Each `fly secrets set` triggers a deployment!** This is normal but can be slow.

**To avoid multiple deployments**, set all secrets at once:

```bash
fly secrets set \
  AWS_REGION="ap-south-1" \
  LOG_LEVEL="INFO" \
  PYTHONPATH="/app" \
  API_TITLE="Phobos Backend API" \
  API_VERSION="1.0.0" \
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

## Step 4: Verify Secrets Are Set

```bash
fly secrets list --app gbauction
```

**Expected output:**
```
NAME                      DIGEST                           DATE
AWS_ACCESS_KEY_ID         xxxxxxxxxxxx                     1m ago
AWS_REGION                xxxxxxxxxxxx                     1m ago
...
SUPABASE_PASSWORD         xxxxxxxxxxxx                     1m ago
...
```

**If still empty after setting:**
- Check you're using `--app gbauction` in all commands
- Verify you're logged into correct Fly.io account
- Check if app is in different organization

---

## Step 5: Check Deployment

```bash
# Wait for deployment to finish (1-2 minutes)
fly status --app gbauction

# Watch deployment logs
fly logs --app gbauction
```

Look for:
```
✅ Loaded environment variables from...
✅ Database engine created successfully...
```

---

## Step 6: Test API

```bash
curl https://gbauction.fly.dev/docs
```

Should return HTML (Swagger UI), not the database error.

---

## Common Issues

### Issue: "Error: Could not find App"

**Solution:**
```bash
fly apps create gbauction
```

Then try setting secrets again.

### Issue: "Error: You don't have permission"

**Solution:**
- Check which organization owns the app: `fly status --app gbauction`
- Switch to correct org or get permissions from org admin

### Issue: Secrets set but app still shows database error

**Solution:**
- Wait 2-3 minutes for deployment to complete
- Force restart: `fly apps restart gbauction`
- Check logs: `fly logs --app gbauction`

### Issue: Command fails with "Error: invalid argument"

**Solution:**
- Check for special characters in values that need escaping
- Try wrapping values in single quotes: `'value'` instead of `"value"`
- Or escape special characters: `\$` for `$`

---

## Alternative: Use Fly.io Dashboard

If CLI isn't working, use the web dashboard:

1. Go to https://fly.io/dashboard
2. Select `gbauction` app
3. Go to **Secrets** section
4. Click **Add Secret**
5. Add each secret name and value
6. Save (triggers deployment)

---

## Get Help

If still having issues:

**Check app configuration:**
```bash
fly config show --app gbauction
```

**View detailed logs:**
```bash
fly logs --app gbauction -a
```

**Check deployments:**
```bash
fly releases --app gbauction
```

**SSH into running instance:**
```bash
fly ssh console --app gbauction
env | grep SUPABASE  # Check if secrets are loaded
```
