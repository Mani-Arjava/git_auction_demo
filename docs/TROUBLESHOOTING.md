# Troubleshooting Guide

## ✅ SOLVED: Internal Server Error (500) on Lambda

### Problem
After deploying, API Gateway returned:
```
Internal Server Error
```

### Root Cause
**Compiled binary modules** (`.so` files) were built for **macOS ARM64** instead of **Linux ARM64**.

Python packages like `pydantic-core`, `uvloop`, `httptools` contain compiled C extensions that are platform-specific. Lambda runs on Linux ARM64, but the build was creating macOS ARM64 binaries.

### Error in CloudWatch
```
ModuleNotFoundError: No module named 'pydantic_core._pydantic_core'
```

The `.so` file existed but was incompatible with Lambda's Linux runtime.

### Solution
Updated `scripts/build.sh` to install **Linux ARM64** compatible packages:

```bash
# Before (WRONG - installs macOS binaries)
uv pip install -r requirements.txt --target package

# After (CORRECT - installs Linux ARM64 binaries)
uv pip install -r requirements.txt --target package \
  --python-platform aarch64-unknown-linux-gnu \
  --python-version 3.12
```

### Verification
Check that binaries are Linux ARM64:
```bash
file lambda/phobos/package/pydantic_core/_pydantic_core.*.so
# Output: ELF 64-bit LSB shared object, ARM aarch64
```

Not macOS:
```bash
# WRONG output would be:
# Mach-O 64-bit dynamically linked shared library arm64
```

### Commands to Fix
```bash
# 1. Rebuild with correct platform
make clean
make build

# 2. Redeploy
make deploy

# 3. Test
curl https://YOUR-API-URL/prod/
```

---

## Common Issues

### 1. Docker Daemon Error
**Error:**
```
docker: Cannot connect to the Docker daemon
```

**Cause:** CDK using Docker bundling

**Solution:** We've fixed this - now using S3/ZIP deployment (no Docker needed)

---

### 2. Package Size Too Large
**Error:**
```
Unzipped size must be smaller than 262144000 bytes
```

**Cause:** Lambda has 250MB limit for unzipped packages

**Check size:**
```bash
du -sh lambda/phobos/package/
```

**Solutions:**
- Remove unused dependencies from `pyproject.toml`
- Use Lambda layers for large libraries
- Consider using Docker images (up to 10GB)

---

### 3. Import Errors
**Error:**
```
ModuleNotFoundError: No module named 'app'
```

**Cause:** Incorrect handler path or missing files

**Verify:**
```bash
# Check package structure
ls -la lambda/phobos/package/app/

# Check handler
grep "handler = " lambda/phobos/package/app/main.py
```

**Handler must be:** `app.main.handler`

---

### 4. CORS Issues
**Error in browser:**
```
Access to XMLHttpRequest has been blocked by CORS policy
```

**Solution:**
Update `infrastructure/lib/python-lambda-stack.ts`:
```typescript
defaultCorsPreflightOptions: {
  allowOrigins: ['https://yourdomain.com'],  // Specific domain
  allowMethods: apigateway.Cors.ALL_METHODS,
  allowHeaders: ['Content-Type', 'Authorization'],
}
```

---

### 5. Cold Start Timeout
**Error:**
```
Task timed out after 3.00 seconds
```

**Cause:** Lambda timeout too short

**Solution:**
Update `infrastructure/lib/python-lambda-stack.ts`:
```typescript
timeout: cdk.Duration.seconds(30),  // Increase if needed
memorySize: 1024,  // More memory = faster CPU
```

---

### 6. Environment Variables Not Set
**Error:**
```
KeyError: 'DATABASE_URL'
```

**Solution:**
Add to `infrastructure/lib/python-lambda-stack.ts`:
```typescript
environment: {
  PYTHONPATH: '/var/task',
  LOG_LEVEL: 'INFO',
  DATABASE_URL: 'your-value',  // Add your vars
}
```

---

## Debugging CloudWatch Logs

### View Logs
```bash
# Latest logs (requires AWS CLI configured)
aws logs tail /aws/lambda/YOUR-FUNCTION-NAME \
  --region us-west-2 \
  --follow

# Filter errors
aws logs tail /aws/lambda/YOUR-FUNCTION-NAME \
  --region us-west-2 \
  --filter-pattern "ERROR"
```

### Add Logging
```python
import logging
logger = logging.getLogger(__name__)

@app.get("/endpoint")
async def endpoint():
    logger.info("Endpoint called")
    logger.error("Error occurred")
    return {"status": "ok"}
```

---

## Testing Locally

### Test Handler
```bash
# Simulates Lambda environment
python3 scripts/test-lambda-handler.py
```

### Test with SAM
```bash
# If you have AWS SAM CLI
sam local invoke PhobosLambda --event test-event.json
```

---

## Performance Issues

### Monitor Metrics
- **Duration:** Should be < 1000ms warm start
- **Memory Used:** Should be < 50% of allocated
- **Cold Start:** 150-250ms typical

### Optimize
```python
# Cache expensive operations
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_operation():
    return result
```

---

## Build Issues

### UV Not Found
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"
```

### Clean Build
```bash
make clean
rm -rf lambda/phobos/package/
make build
```

---

## Deployment Issues

### Bootstrap Not Done
```bash
make bootstrap
```

### Wrong Region
```bash
# Set in environment or .env
export AWS_REGION=us-west-2
export AWS_PROFILE=your-profile
```

### Check Diff Before Deploy
```bash
make diff
```

---

## Quick Fixes

```bash
# Complete reset
make clean
make build
make deploy

# Test locally first
make test-local

# Run tests
make test

# View what will change
make diff
```

---

## Get Help

1. Check CloudWatch logs
2. Test handler locally
3. Verify package structure
4. Check binary compatibility
5. Review environment variables

---

**Most common fix:** Rebuild with `make clean && make build && make deploy`
