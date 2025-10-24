# Complete Deployment Guide: FastAPI on Fly.io with GitHub Actions

## End-to-End Setup from Scratch to Production

This guide covers everything from initial setup to a fully deployed FastAPI application on Fly.io with automated deployments via GitHub Actions.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Setup](#project-setup)
3. [Environment Configuration](#environment-configuration)
4. [Fly.io Setup](#flyio-setup)
5. [Deploy to Fly.io](#deploy-to-flyio)
6. [Set Environment Secrets](#set-environment-secrets)
7. [GitHub Actions Auto-Deploy (Optional)](#github-actions-auto-deploy-optional)
8. [Verification](#verification)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Install Required Tools

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Fly.io CLI
brew install flyctl

# Install Git (if not already installed)
brew install git

# Optional: Install GitHub CLI (only if you want auto-deploy from GitHub)
brew install gh
```

### Verify Installations

```bash
flyctl version    # Should show: flyctl v0.x.x
git --version     # Should show: git version 2.x
gh --version      # Should show: gh version 2.x (optional)
```

### Create Accounts

- [ ] **GitHub Account**: https://github.com/signup
- [ ] **Fly.io Account**: https://fly.io/app/sign-up
- [ ] **Supabase Account** (if using): https://supabase.com
- [ ] **AWS Account** (if using S3): https://aws.amazon.com

---

## Project Setup

### 1. Clone/Create Repository

```bash
# If cloning existing repo
git clone https://github.com/Mani-Arjava/git_auction_demo.git
cd git_auction_demo

# Or if creating new repo
mkdir my-fastapi-app
cd my-fastapi-app
git init
```

### 2. Verify Project Structure

```bash
tree -L 2
```

Expected structure:
```
.
├── .env                          # Environment variables (DO NOT COMMIT)
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore file
├── lambda/
│   └── phobos/
│       ├── Dockerfile            # Docker configuration
│       ├── fly.toml              # Fly.io configuration
│       ├── app/                  # FastAPI application
│       └── pyproject.toml        # Python dependencies
├── .github/
│   └── workflows/
│       └── fly-deploy.yml        # GitHub Actions workflow
└── scripts/
    ├── set-flyio-secrets.sh      # Script to set Fly.io secrets
    └── sync-github-secrets.sh    # Script to sync to GitHub secrets
```

---

## Environment Configuration

### 1. Create .env File

```bash
# Copy example file
cp .env.example .env
```

### 2. Edit .env with Your Values

```bash
# Open in your editor
nano .env
# or
code .env
```

### 3. Required Environment Variables

Fill in these values in your `.env` file:

```bash
# ====================
# AWS Configuration
# ====================
AWS_REGION=ap-south-1
AWS_PROFILE=phobos

# ====================
# Application Configuration
# ====================
NODE_ENV=development
LOG_LEVEL=INFO
PYTHONPATH=/var/task

# ====================
# API Configuration
# ====================
API_TITLE=Phobos Backend API
API_VERSION=1.0.0
CORS_ORIGINS=*

# ====================
# Supabase Configuration
# ====================
SUPABASE_URL=https://YOUR_PROJECT.supabase.co
SUPABASE_ANON_KEY=eyJhbGc...

# ====================
# Supabase Database Configuration
# ====================
SUPABASE_HOST=aws-1-ap-south-1.pooler.supabase.com
SUPABASE_USER=postgres.YOUR_PROJECT
SUPABASE_PASSWORD=YOUR_PASSWORD
SUPABASE_PORT=5432
SUPABASE_DATABASE=postgres
SUPABASE_USE_POOLER=true

# ====================
# AWS S3 Configuration
# ====================
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
AWS_S3_BUCKET=your-bucket-name
AWS_S3_BASE_URL=https://your-bucket.s3.ap-south-1.amazonaws.com

# ====================
# Microservices Configuration
# ====================
BRANCH_BASE_URL=http://localhost:8000
```

### 4. Verify .env is in .gitignore

```bash
grep "^\.env$" .gitignore
```

Should return: `.env`

**IMPORTANT:** Never commit `.env` to git!

---

## Fly.io Setup

### 1. Login to Fly.io

```bash
fly auth login
```

- Browser will open
- Login with your Fly.io account
- Confirm authentication

### 2. Verify Authentication

```bash
fly auth whoami
```

Should show your email.

### 3. Create Fly.io App

```bash
fly apps create gbauction
```

**Or specify organization:**
```bash
fly apps create gbauction --org your-org-name
```

### 4. Verify App Created

```bash
fly apps list
```

Should show `gbauction` in the list.

---

## Deploy to Fly.io

### Option A: Manual First Deployment

```bash
# Navigate to lambda/phobos directory
cd lambda/phobos

# Deploy
fly deploy --config fly.toml

# Wait for deployment (2-3 minutes)
```

**Expected output:**
```
==> Verifying app config
--> Verified app config
==> Building image
...
==> Pushing image to fly
...
==> Creating release
--> Release v1 created
==> Monitoring deployment
...
--> v1 deployed successfully
```

### Option B: Deploy via GitHub Actions

Skip to [GitHub Actions Auto-Deploy](#github-actions-auto-deploy-optional) section.

---

## Set Environment Secrets

**After first deployment, your app won't work yet because it has no environment variables.**

You'll see this error:
```json
{"detail":"Database connection not configured. Please set up database environment variables."}
```

**Choose ONE method below:**

### Method 1: Direct Fly.io Secrets (Recommended - Quick Fix)

This is the **fastest way** to get your app working.

#### Step 1: Run the Script

```bash
# From project root
./scripts/set-flyio-secrets.sh
```

#### Step 2: Review Preview

```
📋 Variables to be set in Fly.io:
   - AWS_REGION: ap-south-1
   - LOG_LEVEL: INFO
   - SUPABASE_URL: https://itdpeuznyceklottqpaj...
   - SUPABASE_PASSWORD: ****
   ...

Continue to set these secrets in Fly.io? (y/n)
```

#### Step 3: Confirm

Type `y` and press Enter.

#### Step 4: Wait for Deployment

```
🚀 Uploading secrets to GitHub...
   Setting AWS_REGION... ✅
   Setting LOG_LEVEL... ✅
   ...

✅ All secrets uploaded successfully!
```

Deployment takes 1-2 minutes.

#### Step 5: Verify Secrets

```bash
fly secrets list --app gbauction
```

Should show all 16 secrets.

**✅ Your app should now work!**

Skip to [Verification](#verification) section.

---

### Method 2: Manual Secret Setting

If the script doesn't work, set secrets manually:

```bash
fly secrets set \
  AWS_REGION="ap-south-1" \
  LOG_LEVEL="INFO" \
  PYTHONPATH="/app" \
  API_TITLE="Phobos Backend API" \
  API_VERSION="1.0.0" \
  CORS_ORIGINS="*" \
  SUPABASE_URL="https://YOUR_PROJECT.supabase.co" \
  SUPABASE_ANON_KEY="eyJhbGc..." \
  SUPABASE_HOST="aws-1-ap-south-1.pooler.supabase.com" \
  SUPABASE_USER="postgres.YOUR_PROJECT" \
  SUPABASE_PASSWORD="YOUR_PASSWORD" \
  SUPABASE_PORT="5432" \
  SUPABASE_DATABASE="postgres" \
  SUPABASE_USE_POOLER="true" \
  AWS_ACCESS_KEY_ID="AKIA..." \
  AWS_SECRET_ACCESS_KEY="YOUR_SECRET_KEY" \
  AWS_S3_BUCKET="your-bucket" \
  AWS_S3_BASE_URL="https://your-bucket.s3.ap-south-1.amazonaws.com" \
  --app gbauction
```

Replace `YOUR_*` placeholders with actual values from your `.env` file.

---

## GitHub Actions Auto-Deploy (Optional)

This section is **optional**. Only do this if you want automatic deployments when you push to GitHub.

**If you just want the app to work, skip this section.**

### Why You Need This

- ✅ Automatic deployment on every `git push`
- ✅ CI/CD pipeline
- ✅ Team collaboration

### Prerequisites

```bash
# Install GitHub CLI
brew install gh

# Login to GitHub
gh auth login
```

Follow prompts:
- Select: **GitHub.com**
- Protocol: **HTTPS**
- Authenticate: **Yes** (browser opens)

### Verify Authentication

```bash
gh auth status
```

Should show: `✓ Logged in to github.com as YourUsername`

### Sync Secrets to GitHub

```bash
./scripts/sync-github-secrets.sh
```

This uploads all secrets from your `.env` to GitHub repository secrets.

### Verify Secrets in GitHub

```bash
gh secret list
```

Or visit: https://github.com/Mani-Arjava/git_auction_demo/settings/secrets/actions

Should show all 16 secrets.

### Test Auto-Deployment

```bash
# Make a change
echo "# Test" >> README.md
git add README.md
git commit -m "Test auto-deployment"
git push origin main
```

### Monitor Deployment

Visit: https://github.com/Mani-Arjava/git_auction_demo/actions

Click on the latest workflow run to see:
- ✅ .env file created with real values (not empty)
- ✅ Docker image built
- ✅ Deployed to Fly.io

---

## Verification

### 1. Check App Status

```bash
fly status --app gbauction
```

**Expected output:**
```
App
  Name     = gbauction
  Owner    = personal
  Hostname = gbauction.fly.dev
  ...

Instances
ID       PROCESS VERSION REGION  STATE   CHECKS  LAST UPDATED
xxx      app     v2      bom     running 1 total 30s ago
```

Status should be: **running**

### 2. Check Logs

```bash
fly logs --app gbauction
```

**Look for these success messages:**
```
✅ Loaded environment variables from /app/.env
✅ Database engine created successfully with session pooler connection
✅ S3 client created using explicit credentials
```

**If you see errors:**
```
⚠️  Database connection not configured
```
→ Go back to [Set Environment Secrets](#set-environment-secrets)

### 3. Test API Endpoints

```bash
# Test health endpoint
curl https://gbauction.fly.dev/docs
```

Should return HTML (Swagger UI page).

**Or visit in browser:**
- https://gbauction.fly.dev/docs (Swagger UI)
- https://gbauction.fly.dev/redoc (ReDoc)

### 4. Test API Functionality

In Swagger UI (https://gbauction.fly.dev/docs):
- Click on any endpoint
- Click "Try it out"
- Click "Execute"
- Should return data (not error)

---

## Troubleshooting

### Issue: "Database connection not configured"

**Cause:** Environment secrets not set

**Solution:**
```bash
# Check if secrets are set
fly secrets list --app gbauction

# If empty, set them
./scripts/set-flyio-secrets.sh

# Force restart
fly apps restart gbauction
```

---

### Issue: "fly: command not found"

**Cause:** Fly.io CLI not installed

**Solution:**
```bash
brew install flyctl
```

---

### Issue: "Could not find App"

**Cause:** App doesn't exist

**Solution:**
```bash
fly apps create gbauction
```

---

### Issue: ".env: line 22: Backend: command not found"

**Cause:** `.env` has spaces in values without quotes

**Solution:**
Already fixed in the latest script. Pull latest changes:
```bash
git pull origin main
./scripts/set-flyio-secrets.sh
```

---

### Issue: GitHub Actions shows empty .env values

**Cause:** GitHub secrets not added

**Solution:**
```bash
# Install GitHub CLI
brew install gh

# Login
gh auth login

# Sync secrets
./scripts/sync-github-secrets.sh

# Verify
gh secret list
```

---

### Issue: Deployment slow or stuck

**Cause:** Normal for first deployment

**Solution:** Wait 2-3 minutes. Check logs:
```bash
fly logs --app gbauction --follow
```

---

### Issue: "Permission denied" when running scripts

**Cause:** Script not executable

**Solution:**
```bash
chmod +x scripts/set-flyio-secrets.sh
chmod +x scripts/sync-github-secrets.sh
```

---

### Issue: Health check failing

**Cause:** App not responding on `/docs` endpoint

**Solution:**
```bash
# Check logs
fly logs --app gbauction

# Restart app
fly apps restart gbauction

# Check status
fly status --app gbauction
```

---

## Command Reference

### Fly.io Commands

```bash
# Authentication
fly auth login
fly auth whoami
fly auth logout

# App Management
fly apps list
fly apps create APP_NAME
fly status --app APP_NAME
fly apps restart APP_NAME
fly apps destroy APP_NAME

# Secrets Management
fly secrets list --app APP_NAME
fly secrets set KEY=value --app APP_NAME
fly secrets unset KEY --app APP_NAME

# Deployment
fly deploy --app APP_NAME
fly deploy --config path/to/fly.toml

# Logs & Monitoring
fly logs --app APP_NAME
fly logs --app APP_NAME --follow
fly status --app APP_NAME

# SSH Access
fly ssh console --app APP_NAME
fly ssh console --app APP_NAME -C "env"
```

### GitHub CLI Commands

```bash
# Authentication
gh auth login
gh auth status
gh auth logout

# Secrets Management
gh secret list
gh secret set SECRET_NAME
gh secret remove SECRET_NAME

# Repository
gh repo view
gh workflow list
gh run list
```

### Git Commands

```bash
# Push to trigger deployment
git add .
git commit -m "Your message"
git push origin main

# View remote
git remote -v

# Check status
git status
```

---

## Project Structure Explained

```
fly_io_github_auction/
├── .env                              # Local environment variables (NOT in git)
├── .env.example                      # Template for .env
├── .gitignore                        # Files to ignore in git
├── .dockerignore                     # Files to ignore in Docker build
│
├── lambda/phobos/                    # Application directory
│   ├── Dockerfile                    # Docker configuration for Fly.io
│   ├── fly.toml                      # Fly.io app configuration
│   ├── .dockerignore                 # Docker-specific ignores
│   ├── pyproject.toml                # Python dependencies
│   ├── requirements.txt              # Compiled dependencies
│   │
│   └── app/                          # FastAPI application code
│       ├── main.py                   # Lambda handler (not used on Fly.io)
│       ├── main_uvicorn.py           # Local development server
│       └── api/
│           ├── server/app.py         # FastAPI app instance
│           ├── routes.py             # API routes
│           └── db_connection/        # Database configuration
│
├── .github/workflows/
│   └── fly-deploy.yml                # GitHub Actions CI/CD
│
├── scripts/
│   ├── set-flyio-secrets.sh          # Set secrets in Fly.io
│   ├── sync-github-secrets.sh        # Sync secrets to GitHub
│   └── diagnose-flyio.sh             # Diagnostic tool
│
└── docs/
    ├── COMPLETE_DEPLOYMENT_GUIDE.md  # This file
    ├── FIX_DATABASE_ERROR.md
    ├── GITHUB_SECRETS_SETUP.md
    └── ...
```

---

## Deployment Flow

### Manual Deployment

```
Local Code Changes
    ↓
git commit & push
    ↓
Developer runs: fly deploy
    ↓
Fly.io builds Docker image
    ↓
Fly.io deploys to production
    ↓
App runs with Fly.io secrets
```

### Auto-Deployment (GitHub Actions)

```
Local Code Changes
    ↓
git commit & push to main
    ↓
GitHub Actions triggered
    ↓
Workflow creates .env from GitHub secrets
    ↓
Docker image built in GitHub
    ↓
Deployed to Fly.io
    ↓
App runs with Fly.io secrets
```

---

## Environment Variables Flow

### Development (Local)

```
.env file
    ↓
Loaded by python-dotenv
    ↓
Available in app
```

### Production (Fly.io)

```
Fly.io Secrets
    ↓
Injected as environment variables
    ↓
Available in app at runtime
```

### GitHub Actions

```
GitHub Repository Secrets
    ↓
Used in workflow to create .env
    ↓
.env baked into Docker image
    ↓
Available in app
```

---

## Success Checklist

- [ ] Fly.io account created
- [ ] `flyctl` installed and authenticated
- [ ] `.env` file configured with all values
- [ ] Fly.io app created (`gbauction`)
- [ ] First deployment completed
- [ ] Fly.io secrets set (all 16)
- [ ] App status shows "running"
- [ ] Logs show database connected
- [ ] API docs accessible at https://gbauction.fly.dev/docs
- [ ] API endpoints return data (not errors)
- [ ] **Optional:** GitHub secrets configured
- [ ] **Optional:** Auto-deployment tested

---

## Next Steps

After successful deployment:

1. **Monitor your app:**
   ```bash
   fly logs --app gbauction --follow
   ```

2. **Scale if needed:**
   ```bash
   fly scale count 2 --app gbauction
   ```

3. **Add custom domain:**
   ```bash
   fly certs add yourdomain.com --app gbauction
   ```

4. **Set up alerts:**
   - Configure in Fly.io dashboard
   - Set up uptime monitoring

5. **Review costs:**
   ```bash
   fly dashboard
   ```

---

## Getting Help

- **Fly.io Docs:** https://fly.io/docs
- **Fly.io Community:** https://community.fly.io
- **GitHub Issues:** Report bugs in your repository
- **Logs:** Always check `fly logs` first

---

## Summary

**Minimum steps to get app working:**

1. Install `flyctl`
2. Create `.env` with your credentials
3. `fly auth login`
4. `fly apps create gbauction`
5. `./scripts/set-flyio-secrets.sh`
6. Done! App works at https://gbauction.fly.dev

**To add auto-deployment:**

7. Install `gh`
8. `gh auth login`
9. `./scripts/sync-github-secrets.sh`
10. Done! Push to GitHub auto-deploys

---

**🎉 Congratulations! Your FastAPI app is now deployed on Fly.io!**
