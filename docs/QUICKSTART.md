# Phobos Backend - Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies
```bash
make install
```

This will:
- Install UV package manager
- Install Python dependencies
- Install CDK dependencies

### 2. Test Locally
```bash
make test-local
```

This starts FastAPI on http://localhost:8000

**Test the endpoints:**
```bash
# Root endpoint
curl http://localhost:8000/

# Hello endpoint
curl http://localhost:8000/hello
curl http://localhost:8000/hello/YourName

# Health check
curl http://localhost:8000/health

# API Documentation
open http://localhost:8000/docs
```

### 3. Deploy to AWS
```bash
# First time only (bootstrap CDK)
make bootstrap

# Deploy
make deploy
```

After deployment, you'll get:
- API Gateway URL
- Lambda Function Name
- API Docs URL

## 📝 Quick Commands

```bash
make help         # Show all commands
make test         # Run tests
make build        # Build Lambda + CDK
make format       # Format Python code
make lint         # Lint Python code
make clean        # Clean build artifacts
make destroy      # Delete AWS resources
```

## 🛠️ Development Workflow

1. **Edit code** in `lambda/phobos/app/`
2. **Test locally** with `make test-local`
3. **Run tests** with `make test`
4. **Deploy** with `make deploy`

## 📚 Project Structure

```
lambda/phobos/app/
├── main.py              # FastAPI app
└── api/routes.py        # API routes (add your endpoints here)
```

## 🔧 Adding New Endpoints

Edit `lambda/phobos/app/api/routes.py`:

```python
@router.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"id": user_id, "name": "John Doe"}
```

Deploy:
```bash
make deploy
```

## 🐛 Troubleshooting

### Local server won't start
```bash
# Clean and reinstall
cd lambda/phobos
rm -rf .venv
cd ../..
make test-local
```

### Build fails
```bash
make clean
make build
```

### Deployment issues
```bash
# Check AWS credentials
aws sts get-caller-identity

# Bootstrap CDK
make bootstrap
```

## 📊 What's Deployed

- **Lambda Function** (Python 3.12, ARM64)
- **API Gateway** with CORS enabled
- **CloudWatch Logs** (1 week retention)

## 🎯 Next Steps

1. Add database connection (see `.env.example`)
2. Implement authentication
3. Add more endpoints in `routes.py`
4. Set up CI/CD pipeline
5. Configure custom domain

---

**Need help?** Check the [full README](../README.md) or [API documentation](api.md)
