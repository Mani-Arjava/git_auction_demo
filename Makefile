# =============================================
# Phobos Backend - Python FastAPI Lambda
# Makefile for Development and Deployment
# =============================================

# Load environment variables if .env exists
-include .env
export

# Colors for output
RED=\033[0;31m
GREEN=\033[0;32m
YELLOW=\033[1;33m
BLUE=\033[0;34m
NC=\033[0m # No Color

# AWS Profile Configuration
AWS_PROFILE ?= default

.PHONY: help install build test test-local deploy destroy clean synth bootstrap diff validate env-setup env-validate quick-start db-clear db-init db-reset db-list

# Default target
.DEFAULT_GOAL := help

# =============================================
# HELP
# =============================================

help: ## 📋 Display this help message
	@echo ""
	@echo "$(BLUE)🚀 Phobos Backend - Python FastAPI Lambda$(NC)"
	@echo "$(BLUE)===========================================$(NC)"
	@echo ""
	@echo "$(YELLOW)Development Commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -v -E 'env-|help' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Environment Commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E 'env-' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Environment Variables:$(NC)"
	@echo "  $(GREEN)AWS_PROFILE$(NC)     AWS profile to use (default: default)"
	@echo ""

# =============================================
# INSTALLATION
# =============================================

install: ## 📦 Install all dependencies
	@echo "$(BLUE)📦 Installing uv package manager...$(NC)"
	@command -v uv >/dev/null 2>&1 || (curl -LsSf https://astral.sh/uv/install.sh | sh && export PATH="$$HOME/.cargo/bin:$$PATH")
	@echo "$(BLUE)📦 Installing Python dependencies...$(NC)"
	@cd lambda/phobos && uv pip compile pyproject.toml -o requirements.txt && uv pip sync requirements.txt
	@echo "$(BLUE)📦 Installing CDK dependencies...$(NC)"
	@cd infrastructure && npm install
	@echo "$(GREEN)✅ All dependencies installed!$(NC)"

# =============================================
# BUILD
# =============================================

build: ## 🔨 Build Python Lambda and CDK
	@echo "$(BLUE)🔨 Building project...$(NC)"
	@chmod +x scripts/build.sh
	@./scripts/build.sh

# =============================================
# TESTING
# =============================================

test: ## 🧪 Run tests
	@echo "$(BLUE)🧪 Running Python tests...$(NC)"
	@cd lambda/phobos && uv run pytest tests/ -v --cov=app --cov-report=term-missing || true
	@echo "$(BLUE)🧪 Running CDK tests...$(NC)"
	@cd infrastructure && npm test || true
	@echo "$(GREEN)✅ All tests complete!$(NC)"

test-local: ## 🚀 Run FastAPI locally for testing
	@chmod +x scripts/test-local.sh
	@./scripts/test-local.sh

# =============================================
# DEPLOYMENT
# =============================================

deploy: ## 🚀 Deploy to AWS
	@chmod +x scripts/deploy.sh
	@AWS_PROFILE=$(AWS_PROFILE) ./scripts/deploy.sh

deploy-env: ## 🔧 Deploy environment variables to Lambda
	@chmod +x scripts/deploy-env.sh
	@./scripts/deploy-env.sh

synth: ## 📋 Synthesize CDK stack
	@cd infrastructure && AWS_PROFILE=$(AWS_PROFILE) npm run synth

bootstrap: ## 🔧 Bootstrap CDK (first time setup)
	@cd infrastructure && AWS_PROFILE=$(AWS_PROFILE) npx cdk bootstrap

diff: ## 🔍 Show CDK diff
	@cd infrastructure && AWS_PROFILE=$(AWS_PROFILE) npm run diff

destroy: ## ⚠️  Destroy AWS resources
	@echo "$(RED)⚠️  WARNING: This will delete all AWS resources!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo ""; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		cd infrastructure && AWS_PROFILE=$(AWS_PROFILE) npm run destroy; \
	fi

# =============================================
# CLEANUP
# =============================================

clean: ## 🧹 Clean build artifacts
	@echo "$(BLUE)🧹 Cleaning build artifacts...$(NC)"
	@rm -rf lambda/phobos/__pycache__ lambda/phobos/.pytest_cache lambda/phobos/.coverage
	@rm -rf lambda/phobos/app/__pycache__ lambda/phobos/app/api/__pycache__
	@rm -rf infrastructure/node_modules infrastructure/cdk.out infrastructure/dist
	@find infrastructure -name "*.js" -not -path "*/node_modules/*" -delete
	@find infrastructure -name "*.d.ts" -not -path "*/node_modules/*" -delete
	@find infrastructure -name "*.js.map" -not -path "*/node_modules/*" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✅ Clean complete!$(NC)"

# =============================================
# VALIDATION
# =============================================

validate: ## ✅ Validate configuration
	@echo "$(BLUE)✅ Validating configuration...$(NC)"
	@command -v uv >/dev/null 2>&1 && echo "$(GREEN)✓ uv installed$(NC)" || echo "$(RED)✗ uv not installed$(NC)"
	@command -v node >/dev/null 2>&1 && echo "$(GREEN)✓ Node.js installed$(NC)" || echo "$(RED)✗ Node.js not installed$(NC)"
	@command -v aws >/dev/null 2>&1 && echo "$(GREEN)✓ AWS CLI installed$(NC)" || echo "$(RED)✗ AWS CLI not installed$(NC)"
	@cd lambda/phobos && python --version 2>&1 | grep -q "3.12" && echo "$(GREEN)✓ Python 3.12 found$(NC)" || echo "$(YELLOW)⚠ Python 3.12 not found$(NC)"

# =============================================
# FORMATTING & LINTING
# =============================================

format: ## 🎨 Format Python code with black
	@echo "$(BLUE)🎨 Formatting Python code...$(NC)"
	@cd lambda/phobos && uv run black app/ tests/
	@echo "$(GREEN)✅ Formatting complete!$(NC)"

lint: ## 🔍 Lint Python code with ruff
	@echo "$(BLUE)🔍 Linting Python code...$(NC)"
	@cd lambda/phobos && uv run ruff check app/ tests/
	@echo "$(GREEN)✅ Linting complete!$(NC)"

# =============================================
# ENVIRONMENT COMMANDS
# =============================================

env-setup: ## ⚙️  Setup environment configuration
	@if [ ! -f .env ]; then \
		echo "$(YELLOW)📝 Creating .env file from template...$(NC)"; \
		cp .env.example .env; \
		echo "$(GREEN)✅ .env file created!$(NC)"; \
		echo "$(YELLOW)⚠️  Please edit .env file with your configuration$(NC)"; \
	else \
		echo "$(BLUE)ℹ️  .env file already exists$(NC)"; \
	fi

env-validate: ## ✅ Validate environment configuration
	@echo "$(BLUE)✅ Validating environment configuration...$(NC)"
	@if [ -z "$(AWS_PROFILE)" ]; then echo "$(YELLOW)⚠️  AWS_PROFILE not set$(NC)"; else echo "$(GREEN)✅ AWS_PROFILE: $(AWS_PROFILE)$(NC)"; fi
	@if [ -z "$(AWS_REGION)" ]; then echo "$(YELLOW)⚠️  AWS_REGION not set$(NC)"; else echo "$(GREEN)✅ AWS_REGION: $(AWS_REGION)$(NC)"; fi

# =============================================
# QUICK START
# =============================================

quick-start: env-setup install ## 🚀 Quick start setup (env + install)
	@echo "$(GREEN)🎉 Quick start completed!$(NC)"
	@echo "$(BLUE)Next steps:$(NC)"
	@echo "  1. Edit .env file with your configuration"
	@echo "  2. Run 'make test-local' to start local development server"
	@echo "  3. Run 'make deploy' to deploy to AWS"
	@echo "  4. Visit the API documentation at the deployed URL + /docs"

# =============================================
# DATABASE MANAGEMENT
# =============================================

db-list: ## 📋 List all database tables
	@echo "$(BLUE)📋 Listing database tables...$(NC)"
	@cd lambda/phobos && .venv/bin/python ../../scripts/db-manage.py list

db-clear: ## ⚠️  Drop all database tables (destructive!)
	@echo "$(RED)⚠️  WARNING: This will DROP ALL TABLES!$(NC)"
	@cd lambda/phobos && .venv/bin/python ../../scripts/db-manage.py drop

db-init: ## 🗄️  Create all database tables from models
	@echo "$(BLUE)🗄️  Creating database tables...$(NC)"
	@cd lambda/phobos && .venv/bin/python ../../scripts/db-manage.py create

db-reset: ## 🔄 Reset database (drop + recreate all tables)
	@echo "$(RED)⚠️  WARNING: This will RESET the entire database!$(NC)"
	@cd lambda/phobos && .venv/bin/python ../../scripts/db-manage.py reset
