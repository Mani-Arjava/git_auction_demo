# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Phobos Backend** is a production-ready Python FastAPI Lambda function deployed using AWS CDK with UV package management. This is a template/base backend for Python Lambda applications using S3/ZIP deployment (no Docker required).

## Critical Build Architecture

### Binary Compatibility Requirement

**CRITICAL:** Lambda runs on Linux ARM64, but builds may happen on macOS/Windows. The build script MUST install Linux ARM64 compatible binaries for packages with C extensions.

```bash
# CORRECT - builds Linux ARM64 binaries
uv pip install -r requirements.txt --target package \
  --python-platform aarch64-unknown-linux-gnu \
  --python-version 3.12

# WRONG - builds macOS/local platform binaries
uv pip install -r requirements.txt --target package
```

**Why:** Python packages like `pydantic-core`, `uvloop`, `httptools` contain compiled `.so` files that are platform-specific. Installing without `--python-platform` creates incompatible binaries that cause `ModuleNotFoundError` in Lambda.

**Verify:** `file lambda/phobos/package/pydantic_core/_pydantic_core.*.so` should show "ARM aarch64" not "Mach-O" or "x86_64".

### Deployment Method: S3/ZIP (Not Docker)

The CDK stack uses **S3/ZIP deployment**, not Docker bundling:

```typescript
// infrastructure/lib/python-lambda-stack.ts
code: lambda.Code.fromAsset(path.join(__dirname, '../../lambda/phobos/package'))
```

The `package/` directory is pre-built by `scripts/build.sh`, then CDK zips and uploads to S3. **Never add Docker bundling configuration** - it was explicitly removed to avoid Docker dependencies.

### Build Process Flow

1. `make build` runs `scripts/build.sh`
2. UV installs Linux ARM64 dependencies to `lambda/phobos/package/`
3. Application code copied to `lambda/phobos/package/app/`
4. CDK compiles TypeScript infrastructure
5. `make deploy` → CDK zips `package/` → uploads to S3 → Lambda deploys

**Always run `make build` before `make deploy`** - the package directory must exist with correct binaries.

## Common Development Commands

### Local Development
```bash
make test-local          # Run FastAPI locally on http://localhost:8000
                        # Uses .venv with local development dependencies
                        # Auto-reloads on code changes

make test               # Run pytest with coverage
make format             # Format with black
make lint               # Lint with ruff
```

### Build & Deploy
```bash
make build              # ALWAYS run before deploy
                       # Builds Linux ARM64 package + compiles CDK TypeScript

make deploy            # Build → synth → deploy to AWS
                      # Uses AWS_PROFILE environment variable

make synth             # Generate CloudFormation without deploying
make diff              # Preview infrastructure changes
```

### First-Time Setup
```bash
make bootstrap         # CDK bootstrap (once per AWS account/region)
make install          # Install uv, Python deps, and CDK deps
make quick-start      # env-setup + install
```

### Cleanup
```bash
make clean            # Remove build artifacts, __pycache__, etc.
make destroy          # Delete all AWS resources (prompts for confirmation)
```

### Single Test Execution
```bash
cd lambda/phobos
uv run pytest tests/test_main.py::test_hello_with_name -v
```

## Architecture

### Lambda Handler Flow

```
API Gateway Request
    ↓
Lambda Runtime (ARM64 Linux, Python 3.12)
    ↓
app.main.handler (Mangum wrapper)
    ↓
FastAPI app instance
    ↓
Routes in app/api/routes.py
```

**Handler path:** `app.main.handler` (defined in CDK stack)
- `app` = directory in package
- `main` = main.py module
- `handler` = Mangum instance created at module level

### FastAPI Application Structure

```python
# lambda/phobos/app/main.py
app = FastAPI(...)                    # Main app instance
app.include_router(router)           # Include routes from api/routes.py
handler = Mangum(app)                # Lambda adapter (module-level)
```

Routes are defined in `app/api/routes.py` using APIRouter:
```python
router = APIRouter()

@router.get("/hello/{name}")
async def hello_name(name: str):
    # Pydantic models for validation
    return HelloResponse(message=f"Hello, {name}!", name=name)
```

### CDK Infrastructure Pattern

**Single Stack:** `PythonLambdaStack` in `infrastructure/lib/python-lambda-stack.ts`

Components:
- **Lambda Function:** ARM64, Python 3.12, 512MB, 30s timeout
- **API Gateway:** REST API with Lambda proxy integration
- **CloudWatch Logs:** 1 week retention
- **CORS:** Enabled for all origins (configure for production)

**Proxy Integration:** `{proxy+}` resource handles all paths, FastAPI routes internally.

### Package Structure

```
lambda/phobos/package/          # Built by scripts/build.sh (gitignored)
├── app/                        # Application code
│   ├── main.py                # FastAPI app + Lambda handler
│   └── api/routes.py          # Route definitions
├── fastapi/                   # Dependencies (Linux ARM64 binaries)
├── pydantic/
├── mangum/
└── ... (all deps from requirements.txt)
```

**IMPORTANT:** `package/` is the deployment artifact. CDK points to this directory. Never commit it to git.

## Adding New Features

### New API Endpoint

1. Edit `lambda/phobos/app/api/routes.py`:
```python
class UserResponse(BaseModel):
    id: int
    name: str

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    return UserResponse(id=user_id, name="Example")
```

2. Test locally: `make test-local` → http://localhost:8000/docs
3. Add test in `tests/test_routes.py`
4. Deploy: `make build && make deploy`

### Environment Variables

**Lambda:** Edit `infrastructure/lib/python-lambda-stack.ts`:
```typescript
environment: {
  PYTHONPATH: '/var/task',
  LOG_LEVEL: 'INFO',
  DATABASE_URL: 'value',  // Add here
}
```

**Local:** Use `.env` file (copied from `.env.example`)

### Dependencies

1. Add to `lambda/phobos/pyproject.toml`:
```toml
dependencies = [
    "fastapi>=0.109.0",
    "new-package>=1.0.0",  # Add here
]
```

2. Rebuild: `make clean && make build`
3. Verify in package: `ls lambda/phobos/package/ | grep new-package`

## Testing Strategy

### Local Testing (Fast Iteration)
- `make test-local` → FastAPI with uvicorn
- Access Swagger UI at http://localhost:8000/docs
- Uses local Python environment, no Lambda simulation

### Unit Tests
- Location: `tests/test_*.py`
- Uses FastAPI TestClient (simulates requests without network)
- Run: `make test` or `cd lambda/phobos && uv run pytest -v`

### Deployed API Testing
- Get URL from CloudFormation outputs after `make deploy`
- Use `scripts/verify-deployment.sh` for automated testing
- Check CloudWatch logs: `aws logs tail /aws/lambda/FUNCTION_NAME --follow`

## Common Issues & Solutions

### 500 Internal Server Error After Deploy
**Cause:** Binary incompatibility (macOS binaries deployed to Linux Lambda)

**Fix:**
```bash
make clean
make build  # Rebuilds with Linux ARM64 binaries
make deploy
```

**Verify:** `file lambda/phobos/package/pydantic_core/_pydantic_core.*.so` shows "ARM aarch64"

### Package Not Found Errors During Build
CDK expects `lambda/phobos/package/` to exist. If deployment fails with package path errors:
```bash
make build  # Creates package directory
```

### Import Errors in Lambda
Check handler path matches: `app.main.handler`
- Directory structure must be: `package/app/main.py`
- Handler variable must exist: `handler = Mangum(app)`

### Docker Daemon Errors
This project doesn't use Docker. If you see Docker errors, someone added Docker bundling to CDK. Remove it:
```typescript
// WRONG - do not add this
code: lambda.Code.fromAsset(..., { bundling: { ... } })

// CORRECT - simple asset path
code: lambda.Code.fromAsset(path.join(__dirname, '../../lambda/phobos/package'))
```

## UV Package Manager

This project uses UV instead of pip for faster, deterministic builds.

**Key commands:**
- `uv pip compile pyproject.toml -o requirements.txt` - Generate lockfile
- `uv pip install -r requirements.txt --target package --python-platform aarch64-unknown-linux-gnu` - Install for Lambda
- `uv run pytest` - Run tests in UV environment
- `uv venv` - Create virtual environment

**Why UV:**
- 10-100x faster than pip
- Platform-specific installs for cross-compilation
- Built-in lockfile generation

## Deployment Outputs

After `make deploy`, CloudFormation provides:
- **ApiUrl:** `https://{id}.execute-api.{region}.amazonaws.com/prod/`
- **ApiDocsUrl:** `{ApiUrl}docs` (Swagger UI)
- **LambdaFunctionName:** For CloudWatch logs
- **LambdaFunctionArn:** For IAM policies

Access docs at deployed URL + `/docs` for interactive API testing.

## Performance Considerations

- **Cold start:** 150-250ms (ARM64 + Python 3.12)
- **Package size:** ~20MB (well under 250MB limit)
- **Memory:** 512MB allocated, typically uses ~100MB
- **ARM64:** 34% cost savings vs x86_64

**Optimization tips:**
- Keep dependencies minimal
- Use Pydantic models for validation (pre-compiled)
- Cache expensive operations with `@lru_cache`
- Monitor with CloudWatch metrics

## AWS Profile Configuration

Set AWS_PROFILE for all AWS operations:
```bash
export AWS_PROFILE=your-profile
make deploy

# Or inline
AWS_PROFILE=your-profile make deploy
```

Default is `default` profile from `~/.aws/credentials`.

## Documentation

- `README.md` - User-facing quickstart
- `docs/DEPLOYMENT.md` - S3/ZIP deployment details
- `docs/TROUBLESHOOTING.md` - Common issues and fixes
- `docs/QUICKSTART.md` - Condensed getting started
- `docs/api.md` - API endpoint documentation

Refer to troubleshooting guide for solved issues before debugging.
