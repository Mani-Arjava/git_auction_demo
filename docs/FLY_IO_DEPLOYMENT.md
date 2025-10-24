# Fly.io Auto-Deployment Setup

## Overview

This repository is configured for automatic deployment to Fly.io when code is pushed to the `main` branch. The FastAPI application runs as a web service on Fly.io infrastructure.

## Prerequisites ✓

You've already completed these steps:
- ✅ Installed Fly.io CLI
- ✅ Created Fly.io account
- ✅ Created Fly.io app (`gbauction`)
- ✅ Generated Fly.io API token
- ✅ Added `FLY_API_TOKEN` to GitHub secrets

## Configuration Files

All deployment files are located in `lambda/phobos/`:

### 1. Dockerfile (`lambda/phobos/Dockerfile`)
Builds Python 3.12 image with FastAPI and runs uvicorn on port 8080.

### 2. fly.toml (`lambda/phobos/fly.toml`)
Fly.io configuration:
- **App name:** `gbauction`
- **Region:** `bom` (Mumbai)
- **Port:** 8080 (internal)
- **Memory:** 1GB
- **Auto-scaling:** Stops when idle, starts on request

### 3. GitHub Actions Workflow (`.github/workflows/fly-deploy.yml`)
Triggers on push to `main` branch

## Required GitHub Secrets

### Add secrets at: `https://github.com/Mani-Arjava/git_auction_demo/settings/secrets/actions`

Click "New repository secret" and add each:

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `FLY_API_TOKEN` | Fly.io deploy token | ✅ Already added |
| `AWS_REGION` | AWS region | `ap-south-1` |
| `LOG_LEVEL` | Application log level | `INFO` |
| `CORS_ORIGINS` | CORS allowed origins | `*` |
| `SUPABASE_URL` | Supabase project URL | `https://xxx.supabase.co` |
| `SUPABASE_ANON_KEY` | Supabase anonymous key | `eyJhbGc...` |
| `SUPABASE_HOST` | Supabase database host | `aws-1-ap-south-1.pooler.supabase.com` |
| `SUPABASE_USER` | Supabase database user | `postgres.xxx` |
| `SUPABASE_PASSWORD` | Supabase database password | Your password |
| `SUPABASE_PORT` | Supabase database port | `5432` |
| `SUPABASE_DATABASE` | Supabase database name | `postgres` |
| `SUPABASE_USE_POOLER` | Use connection pooler | `true` |
| `AWS_ACCESS_KEY_ID` | AWS access key | `AKIA...` |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | Your secret key |
| `AWS_S3_BUCKET` | S3 bucket name | `phobosdev` |
| `AWS_S3_BASE_URL` | S3 base URL | `https://bucket.s3.region.amazonaws.com` |
| `BRANCH_BASE_URL` | Branch service URL | URL or empty |

## Deployment Process

### Automatic Deployment (Recommended)

Once secrets are configured:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

GitHub Actions will automatically:
1. Checkout code
2. Setup Fly.io CLI
3. Deploy from `lambda/phobos` directory
4. Set environment secrets
5. Report deployment status

### Manual Deployment (Optional)

```bash
# From lambda/phobos directory
cd lambda/phobos
fly deploy

# Or from root directory
fly deploy --config lambda/phobos/fly.toml
```

## Accessing Your Application

- **Production URL:** https://gbauction.fly.dev
- **API Docs:** https://gbauction.fly.dev/docs
- **Health Check:** `/docs` endpoint (checked every 30s)

## Monitoring Commands

```bash
# View live logs
fly logs --app gbauction

# Check status
fly status --app gbauction

# List secrets (names only)
fly secrets list --app gbauction

# Update a secret
fly secrets set KEY=value --app gbauction

# Restart app
fly apps restart gbauction
```

## Troubleshooting

### Deployment Fails

**Check GitHub Actions:**
1. Go to repository → **Actions** tab
2. Click on failed workflow
3. Review error logs

**Common issues:**
- Missing GitHub secrets → Add them in Settings
- Invalid `FLY_API_TOKEN` → Regenerate: `fly tokens create deploy`
- Port mismatch → Ensure Dockerfile uses 8080

### App Not Starting

```bash
# Check logs
fly logs --app gbauction

# Common issues:
# - Missing environment variables
# - Database connection errors
# - Python import errors
```

### Health Check Failing

```bash
# Restart app
fly apps restart gbauction

# Check if /docs endpoint works
curl https://gbauction.fly.dev/docs
```

## Local Testing

Test Docker build locally before deploying:

```bash
cd lambda/phobos

# Build image
docker build -t gbauction .

# Run locally
docker run -p 8080:8080 --env-file ../../.env gbauction

# Access at http://localhost:8080/docs
```

## Cost Management

Your configuration (1GB memory) is on paid tier.

**To reduce costs:**

```bash
# Reduce memory to 512MB
fly scale memory 512 --app gbauction

# Stop app when not needed
fly apps stop gbauction

# Start when needed
fly apps start gbauction
```

**Auto-scaling is enabled:**
- Stops automatically when idle
- Starts automatically on first request
- Minimum machines: 0 (saves costs)

## Rollback

If deployment breaks:

```bash
# View releases
fly releases --app gbauction

# Rollback to previous
fly releases rollback <version> --app gbauction
```

## Quick Reference

```bash
# Auto-deploy
git push origin main

# Manual deploy
cd lambda/phobos && fly deploy

# Logs
fly logs --app gbauction

# Status
fly status --app gbauction

# Secrets
fly secrets set KEY=value --app gbauction

# SSH into instance
fly ssh console --app gbauction

# Restart
fly apps restart gbauction
```

## Next Steps

1. **Add all GitHub secrets** (see table above)
2. **Push to main branch** to trigger first deployment
3. **Monitor deployment** in GitHub Actions
4. **Verify app** at https://gbauction.fly.dev/docs
5. **Check logs** with `fly logs --app gbauction`

## Support

- **Fly.io Docs:** https://fly.io/docs
- **GitHub Actions:** https://github.com/Mani-Arjava/git_auction_demo/actions
- **Application URL:** https://gbauction.fly.dev
