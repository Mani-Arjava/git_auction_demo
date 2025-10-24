# Automatically Sync .env to GitHub Secrets

## Quick Start

Instead of manually copying each value from `.env` to GitHub, use this automated script:

```bash
./scripts/sync-github-secrets.sh
```

This reads your local `.env` and uploads all values as GitHub repository secrets automatically.

---

## Prerequisites

### 1. Install GitHub CLI

**macOS:**
```bash
brew install gh
```

**Linux:**
```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

**Windows:**
```bash
winget install --id GitHub.cli
```

Or download from: https://cli.github.com/

### 2. Authenticate with GitHub

```bash
gh auth login
```

Follow the prompts:
- Select: **GitHub.com**
- Select: **HTTPS**
- Authenticate in browser: **Yes**
- Login with your GitHub account

Verify authentication:
```bash
gh auth status
```

Should show:
```
✓ Logged in to github.com as Mani-Arjava
```

---

## How to Use

### Step 1: Ensure .env File is Complete

Check your `.env` file has all required values:

```bash
cat .env
```

Required variables:
- `AWS_REGION`
- `LOG_LEVEL`
- `CORS_ORIGINS`
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_HOST`
- `SUPABASE_USER`
- `SUPABASE_PASSWORD`
- `SUPABASE_PORT`
- `SUPABASE_DATABASE`
- `SUPABASE_USE_POOLER`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_S3_BUCKET`
- `AWS_S3_BASE_URL`
- `BRANCH_BASE_URL` (optional)

### Step 2: Run the Sync Script

```bash
./scripts/sync-github-secrets.sh
```

### Step 3: Review Preview

The script will show you what will be uploaded (with sensitive values masked):

```
📋 Secrets to be uploaded to GitHub:

   ✅ AWS_REGION: ap-south-1
   ✅ LOG_LEVEL: INFO
   ✅ SUPABASE_URL: https://itdpeuznyceklottqpaj...
   ✅ SUPABASE_PASSWORD: ******* (16 chars)
   ✅ AWS_ACCESS_KEY_ID: ******* (20 chars)
   ...

Upload these secrets to GitHub? (y/n)
```

### Step 4: Confirm Upload

Type `y` and press Enter.

The script will upload each secret:

```
🚀 Uploading secrets to GitHub...

   Setting AWS_REGION... ✅
   Setting LOG_LEVEL... ✅
   Setting SUPABASE_URL... ✅
   Setting SUPABASE_PASSWORD... ✅
   ...

✅ All secrets uploaded successfully! (16 secrets)
```

---

## Verify Secrets Are Set

### Option 1: GitHub Web UI

Go to: https://github.com/Mani-Arjava/git_auction_demo/settings/secrets/actions

You should see all 16 secrets listed (values are hidden).

### Option 2: GitHub CLI

```bash
gh secret list
```

Expected output:
```
AWS_ACCESS_KEY_ID     Updated 2024-10-24
AWS_REGION            Updated 2024-10-24
AWS_S3_BUCKET         Updated 2024-10-24
...
SUPABASE_PASSWORD     Updated 2024-10-24
```

---

## Test Auto-Deployment

### Trigger Deployment

Push any change to `main` branch:

```bash
echo "# Test" >> README.md
git add README.md
git commit -m "Test auto-deployment with secrets"
git push origin main
```

### Watch Deployment

**GitHub Actions:**
https://github.com/Mani-Arjava/git_auction_demo/actions

Click on the latest workflow run to see:
1. ✅ Secrets are no longer empty in the `.env` creation step
2. ✅ Docker build succeeds
3. ✅ Deployment to Fly.io succeeds

**Check Logs:**
```bash
fly logs --app gbauction
```

Look for:
```
✅ Loaded environment variables from /app/.env
✅ Database engine created successfully
✅ S3 client created
```

**Test API:**
```bash
curl https://gbauction.fly.dev/docs
```

Should return Swagger UI HTML (not database error).

---

## Update Secrets Later

If you change values in `.env`, re-run the script:

```bash
./scripts/sync-github-secrets.sh
```

It will update existing secrets with new values.

---

## Troubleshooting

### "gh: command not found"

Install GitHub CLI:
```bash
brew install gh
```

### "Not authenticated with GitHub CLI"

Login first:
```bash
gh auth login
```

### "Error: The following required secrets are missing"

Check your `.env` file has all values:
```bash
grep -E "AWS_REGION|SUPABASE_URL" .env
```

### Secrets uploaded but deployment still fails

1. **Check workflow run**: https://github.com/Mani-Arjava/git_auction_demo/actions
2. **Look for `.env` creation step** - values should NOT be empty
3. **Check logs**: `fly logs --app gbauction`

### "Permission denied" error

Make script executable:
```bash
chmod +x scripts/sync-github-secrets.sh
```

---

## Security Notes

- ✅ Secrets are encrypted in GitHub
- ✅ Secret values are masked in workflow logs
- ✅ Only workflow runs can access secrets
- ⚠️ Never commit `.env` to git (already in `.gitignore`)
- ⚠️ Rotate AWS keys periodically

---

## What Happens Next

After syncing secrets to GitHub:

1. **Every push to `main`** triggers automatic deployment
2. **GitHub Actions** creates `.env` from secrets
3. **Docker image** is built with environment variables
4. **Fly.io** deploys the new version
5. **Your app** has all credentials and works

No manual intervention needed! 🎉

---

## Alternative: Manual Method

If you prefer manual setup, see: `docs/GITHUB_SECRETS_SETUP.md`

But the automated script is much faster and less error-prone.
