# Deployment Guide - S3/ZIP (No Docker Required)

## ✅ Deployment Method: S3/ZIP

This project uses **S3/ZIP deployment** for Lambda, which means:
- ✅ No Docker required
- ✅ Fast local builds with UV
- ✅ Direct S3 upload of pre-built package
- ✅ Matches Rust backend deployment pattern

## 🏗️ How It Works

### Build Process
1. **UV installs dependencies** to `lambda/phobos/package/`
2. **App code is copied** to `lambda/phobos/package/app/`
3. **CDK packages as ZIP** and uploads to S3
4. **Lambda runs from S3** (no containers)

### CDK Configuration
```typescript
// No Docker bundling!
code: lambda.Code.fromAsset(path.join(__dirname, '../../lambda/phobos/package'))
```

This is a simple asset path - CDK zips it and uploads to S3.

## 🚀 Deployment Steps

### First Time Setup

```bash
# 1. Bootstrap CDK (once per AWS account/region)
make bootstrap
```

### Every Deployment

```bash
# 2. Build package locally (no Docker)
make build

# 3. Deploy to AWS
make deploy
```

## 📦 What Gets Deployed

The `lambda/phobos/package/` directory contains:
```
package/
├── app/                    # Your FastAPI code
│   ├── main.py
│   └── api/routes.py
├── fastapi/                # Dependency
├── mangum/                 # Dependency
├── pydantic/               # Dependency
└── ... (all dependencies)
```

This entire directory is:
1. ✅ Zipped by CDK
2. ✅ Uploaded to S3
3. ✅ Deployed to Lambda

## 🔍 Verification

After build, check package size:
```bash
du -sh lambda/phobos/package/
# Should be < 50MB (well under 250MB Lambda limit)
```

View package contents:
```bash
ls -la lambda/phobos/package/
```

## 🐛 Troubleshooting

### "Docker daemon not running" Error
❌ **Old approach:** Used Docker bundling
✅ **Fixed:** Now uses local UV + S3/ZIP

### Build Fails
```bash
# Clean and rebuild
make clean
make build
```

### Deployment Fails
```bash
# Check AWS credentials
aws sts get-caller-identity

# Ensure bootstrap
make bootstrap

# View what will be deployed
make synth
```

## 📊 Deployment Size

Typical package sizes:
- **Dependencies:** ~15-20MB
- **App code:** <1MB
- **Total ZIP:** ~20MB
- **Lambda limit:** 250MB (plenty of room!)

## ⚡ Performance

### Cold Start
- **ARM64 + Python 3.12:** ~150-250ms
- **No container overhead:** Faster than Docker images

### Build Time
- **Local build:** 10-20 seconds
- **CDK synth:** 5-10 seconds
- **Deploy:** 30-60 seconds
- **Total:** ~1-2 minutes

## 🔄 Update Workflow

```bash
# 1. Make code changes in lambda/phobos/app/

# 2. Test locally
make test-local

# 3. Build package
make build

# 4. Deploy
make deploy
```

## 🆚 Comparison: S3/ZIP vs Docker

| Feature | S3/ZIP (Current) | Docker Images |
|---------|------------------|---------------|
| Build Speed | ⚡ Fast (10-20s) | 🐌 Slow (2-5min) |
| Docker Required | ✅ No | ❌ Yes |
| Size Limit | 250MB | 10GB |
| Cold Start | ⚡ Fast | 🐌 Slower |
| Complexity | ✅ Simple | ❌ Complex |

## 📚 Related Commands

```bash
make build        # Build package locally
make synth        # Generate CloudFormation (no deploy)
make diff         # Show what will change
make deploy       # Deploy to AWS
make destroy      # Delete all resources
```

## ✅ Best Practices

1. ✅ Always run `make build` before `make deploy`
2. ✅ Test locally with `make test-local` first
3. ✅ Use `make diff` to preview changes
4. ✅ Keep dependencies minimal
5. ✅ Monitor package size (`du -sh lambda/phobos/package/`)

---

**No Docker needed! 🎉**
