# GitHub Secrets Setup Guide

## Required GitHub Secrets for Fly.io Deployment

You need to add the following secrets to your GitHub repository to enable automatic deployment.

### How to Add Secrets

1. Go to: https://github.com/Mani-Arjava/git_auction_demo/settings/secrets/actions
2. Click **"New repository secret"**
3. Enter the **Name** and **Secret** value
4. Click **"Add secret"**
5. Repeat for all secrets below

---

## Secrets List

Based on your `.env` file, add these secrets:

### ✅ Already Added
| Secret Name | Status |
|-------------|--------|
| `FLY_API_TOKEN` | ✅ Already configured |

### 📝 Need to Add

Copy the values from your local `.env` file and add them as GitHub secrets:

| Secret Name | Value from your .env | Description |
|-------------|----------------------|-------------|
| `AWS_REGION` | `ap-south-1` | AWS region |
| `LOG_LEVEL` | `INFO` | Application log level |
| `CORS_ORIGINS` | `*` | CORS allowed origins |
| `SUPABASE_URL` | `https://itdpeuznyceklottqpaj.supabase.co` | Your Supabase project URL |
| `SUPABASE_ANON_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` | Your Supabase anon key |
| `SUPABASE_HOST` | `aws-1-ap-south-1.pooler.supabase.com` | Supabase database host |
| `SUPABASE_USER` | `postgres.itdpeuznyceklottqpaj` | Supabase database user |
| `SUPABASE_PASSWORD` | `YTvctzA89M8a4wf6` | Supabase database password |
| `SUPABASE_PORT` | `5432` | Supabase database port |
| `SUPABASE_DATABASE` | `postgres` | Supabase database name |
| `SUPABASE_USE_POOLER` | `true` | Use connection pooler |
| `AWS_ACCESS_KEY_ID` | `AKIA...` | Your AWS access key (copy from .env) |
| `AWS_SECRET_ACCESS_KEY` | `your-secret-key` | Your AWS secret key (copy from .env) |
| `AWS_S3_BUCKET` | `phobosdev` | Your S3 bucket name |
| `AWS_S3_BASE_URL` | `https://phobosdev.s3.ap-south-1.amazonaws.com` | S3 base URL |
| `BRANCH_BASE_URL` | `http://localhost:8000` | Branch service URL (or leave empty) |

---

## Quick Add Commands (Alternative Method)

If you prefer using GitHub CLI (`gh`), you can add secrets from command line:

```bash
# Install gh if not already installed: brew install gh

# Login to GitHub
gh auth login

# Add each secret
gh secret set AWS_REGION -b"ap-south-1"
gh secret set LOG_LEVEL -b"INFO"
gh secret set CORS_ORIGINS -b"*"
gh secret set SUPABASE_URL -b"https://itdpeuznyceklottqpaj.supabase.co"
gh secret set SUPABASE_ANON_KEY -b"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
gh secret set SUPABASE_HOST -b"aws-1-ap-south-1.pooler.supabase.com"
gh secret set SUPABASE_USER -b"postgres.itdpeuznyceklottqpaj"
gh secret set SUPABASE_PASSWORD -b"YTvctzA89M8a4wf6"
gh secret set SUPABASE_PORT -b"5432"
gh secret set SUPABASE_DATABASE -b"postgres"
gh secret set SUPABASE_USE_POOLER -b"true"
gh secret set AWS_ACCESS_KEY_ID -b"YOUR_AWS_ACCESS_KEY"
gh secret set AWS_SECRET_ACCESS_KEY -b"YOUR_AWS_SECRET_KEY"
gh secret set AWS_S3_BUCKET -b"phobosdev"
gh secret set AWS_S3_BASE_URL -b"https://phobosdev.s3.ap-south-1.amazonaws.com"
gh secret set BRANCH_BASE_URL -b"http://localhost:8000"
```

---

## Verification

After adding all secrets:

1. **List secrets** (names only, values are hidden):
   ```bash
   gh secret list
   ```

2. **Trigger deployment** by pushing to main:
   ```bash
   git push origin main
   ```

3. **Watch GitHub Actions**: https://github.com/Mani-Arjava/git_auction_demo/actions

4. **Check logs** if deployment fails - missing secrets will show as empty values

---

## Security Notes

- ⚠️ **NEVER commit these values to git**
- ⚠️ **Rotate AWS keys** shown in this doc (they were exposed earlier)
- ✅ GitHub secrets are encrypted and only accessible during workflow runs
- ✅ Secret values are masked in workflow logs

---

## What Happens During Deployment

1. GitHub Actions checks out your code
2. Creates `.env` file from these secrets
3. Copies `.env` to `lambda/phobos/.env`
4. Builds Docker image (includes `.env`)
5. Deploys to Fly.io

Your app will read environment variables from the `.env` file baked into the Docker image.
