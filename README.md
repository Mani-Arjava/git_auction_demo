# Python FastAPI Lambda with AWS CDK

A production-ready Python FastAPI Lambda function deployed using AWS CDK and UV package manager.

## 🏗️ Architecture

```
phobos-backend/
├── lambda/
│   └── phobos/                 # Python FastAPI Lambda
│       ├── app/
│       │   ├── __init__.py
│       │   ├── main.py         # FastAPI app with Mangum handler
│       │   └── api/
│       │       └── routes.py   # API route definitions
│       ├── pyproject.toml      # UV package configuration
│       ├── requirements.txt    # Generated dependencies
│       └── .python-version     # Python version (3.12)
├── infrastructure/             # CDK infrastructure
│   ├── bin/
│   │   └── app.ts             # CDK app entry point
│   ├── lib/
│   │   └── python-lambda-stack.ts  # Stack definition
│   ├── package.json           # Node dependencies
│   ├── tsconfig.json          # TypeScript config
│   └── cdk.json              # CDK configuration
├── scripts/                   # Automation scripts
│   ├── build.sh              # Build script
│   ├── deploy.sh             # Deployment script
│   └── test-local.sh         # Local testing
├── tests/                     # Test suite
├── docs/                      # Documentation
└── Makefile                  # Task automation
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.12+**: Install from [python.org](https://www.python.org/)
2. **UV**: Fast Python package manager (installed automatically)
3. **Node.js**: Version 18+ recommended
4. **AWS CLI**: Configured with credentials
5. **AWS CDK**: Will be installed automatically

### Installation

```bash
# Install all dependencies
make install
```

### Local Development

```bash
# Run FastAPI locally with hot reload
make test-local

# Test the endpoints:
curl http://localhost:8000/
curl http://localhost:8000/hello
curl http://localhost:8000/hello/World
curl http://localhost:8000/health

# View API documentation:
open http://localhost:8000/docs        # Swagger UI
open http://localhost:8000/redoc       # ReDoc
```

### Deployment

```bash
# First time setup (bootstrap CDK)
make bootstrap

# Deploy to AWS
make deploy
```

## 📝 Available Commands

```bash
make help         # Show all available commands
make install      # Install dependencies (uv + npm)
make build        # Build Python Lambda and CDK
make test         # Run tests
make test-local   # Run FastAPI locally
make deploy       # Deploy to AWS
make synth        # Synthesize CDK stack
make destroy      # Destroy AWS resources
make clean        # Clean build artifacts
make diff         # Show CDK diff
make format       # Format code with black
make lint         # Lint code with ruff
make validate     # Validate configuration
```

## 🔧 API Endpoints

- `GET /` - Root endpoint returning welcome message
- `GET /hello` - Default hello endpoint
- `GET /hello/{name}` - Personalized greeting
- `GET /health` - Health check endpoint
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation

## 🏃 Development Workflow

1. **Make changes** to Python code in `lambda/phobos/app/`
2. **Test locally** with `make test-local`
3. **Run tests** with `make test`
4. **Format code** with `make format`
5. **Deploy** with `make deploy`

## 🔍 Monitoring

After deployment, you can:
- View logs in CloudWatch
- Monitor metrics in AWS Lambda console
- Access API Gateway dashboard for request metrics
- Test endpoints using the deployed URL

## 🧪 Testing

```bash
# Run Python unit tests
make test

# Test deployed API
API_URL=$(aws cloudformation describe-stacks \
  --stack-name PythonLambdaStack \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiUrl`].OutputValue' \
  --output text)

curl $API_URL
curl $API_URL/hello/World
curl $API_URL/health
curl $API_URL/docs
```

## 🛠️ Customization

### Adding New Endpoints

1. Edit `lambda/phobos/app/api/routes.py` to add new route handlers
2. FastAPI will automatically update OpenAPI documentation
3. Deploy with `make deploy`

### Environment Variables

Add environment variables in `infrastructure/lib/python-lambda-stack.ts`:

```typescript
environment: {
  PYTHONPATH: '/var/task',
  LOG_LEVEL: 'INFO',
  YOUR_VAR: 'value',
}
```

Or use `.env` file for local development:

```bash
# Copy example file
cp .env.example .env

# Edit with your values
vim .env
```

## 📊 Performance

- **Cold Start**: ~150-250ms (ARM64 + Python 3.12)
- **Warm Response**: <50ms
- **Memory**: 512MB (configurable)
- **Timeout**: 30 seconds (configurable)
- **Architecture**: ARM64 (AWS Graviton2) for 34% cost savings
- **Deployment**: S3/ZIP (no Docker required)

## 🔒 Security

- IAM roles with least privilege
- API Gateway with CORS configuration
- CloudWatch logging enabled
- No hardcoded secrets
- Environment variable management

## 🚨 Troubleshooting

### Internal Server Error (500) After Deploy

**This is usually caused by binary compatibility issues.**

The build script installs Linux ARM64 binaries for Lambda. If you see 500 errors:

```bash
# Rebuild with correct platform binaries
make clean
make build
make deploy
```

The build script uses `--python-platform aarch64-unknown-linux-gnu` to ensure Lambda-compatible binaries.

### Build Issues

```bash
# Clean and rebuild
make clean
make build
```

### UV Installation Issues

```bash
# Manually install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"
```

### Deployment Issues

```bash
# Check AWS credentials
aws sts get-caller-identity

# Bootstrap CDK if needed
make bootstrap

# View CDK diff
make diff
```

### Local Testing Issues

```bash
# Ensure Python 3.12 is installed
python --version

# Reinstall dependencies
cd lambda/phobos
uv pip sync requirements.txt
```

**For detailed troubleshooting, see [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)**

## 📚 Technology Stack

- **Runtime**: Python 3.12
- **Framework**: FastAPI
- **Lambda Adapter**: Mangum
- **Package Manager**: UV (Astral)
- **Infrastructure**: AWS CDK (TypeScript)
- **Testing**: pytest
- **Linting**: Ruff
- **Formatting**: Black

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Mangum (FastAPI + Lambda)](https://mangum.io/)
- [UV Package Manager](https://github.com/astral-sh/uv)
- [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/)
- [AWS Lambda Python](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and formatting
5. Submit a pull request

## 📄 License

MIT
