import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
import boto3

# Load environment variables based on environment
if os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
    # Running in Lambda - environment variables are already loaded
    pass
else:
    # Local development - load from project root .env
    # Handle different execution contexts (local testing vs module import)

    # Try multiple approaches to find the .env file
    possible_env_paths = [
        # When running from lambda/phobos directory
        Path(__file__).parent.parent.parent.parent.parent / ".env",
        # When running from project root
        Path.cwd() / ".env",
        # When running from tests or other directories
        Path.cwd().parent / ".env",
        Path.cwd().parent.parent / ".env",
        # Absolute fallback (adjust for your system)
        Path("/Users/karthik/SourceCode/phobos-backend/.env")
    ]

    env_loaded = False
    for env_path in possible_env_paths:
        if env_path.exists():
            load_dotenv(env_path)
            print(f"✅ Loaded environment variables from {env_path}")
            env_loaded = True
            break

    if not env_loaded:
        print("⚠️  .env file not found. Please create one from .env.example")

# Supabase database configuration
db_config = {
    "user": os.getenv("SUPABASE_USER"),
    "password": os.getenv("SUPABASE_PASSWORD"),
    "host": os.getenv("SUPABASE_HOST"),
    "port": os.getenv("SUPABASE_PORT", "5432"),
    "database": os.getenv("SUPABASE_DATABASE", "postgres"),
    "use_pooler": os.getenv("SUPABASE_USE_POOLER", "false").lower() == "true"
}

# Build connection string
def build_connection_string(config):
    """Build PostgreSQL connection string for both direct and pooler connections"""
    if config["use_pooler"]:
        # Use Supabase pooler connection format
        # Format: postgresql+asyncpg://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
        return f"postgresql+asyncpg://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
    else:
        # Direct connection
        return f"postgresql+asyncpg://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"

# Create database engine
try:
    connection_string = build_connection_string(db_config)

    # Only create engine if all required parameters are present
    if all(val is not None and val != "" for val in db_config.values()):
        # Import NullPool for transaction mode compatibility
        from sqlalchemy.pool import NullPool

        # Enhanced engine configuration for Lambda with transaction mode support
        if db_config["use_pooler"]:
            # Session mode (pooler) configuration - simpler and works well
            engine = create_async_engine(
                connection_string,
                # Connection pool settings optimized for Lambda
                pool_size=5,  # Number of connections to maintain
                max_overflow=10,  # Additional connections under load
                pool_timeout=30,  # Seconds to wait for connection
                pool_recycle=3600,  # Recycle connections every hour
                # Lambda-specific settings
                connect_args={
                    "command_timeout": 60,  # Command timeout in seconds
                    "server_settings": {
                        "application_name": "phobos_lambda" if os.getenv("AWS_LAMBDA_FUNCTION_NAME") else "phobos_local"
                    },
                    "ssl": "require"  # Ensure SSL connection for security
                }
            )
            print(f"✅ Database engine created successfully with session pooler connection")
        else:
            # Direct connection configuration (fallback)
            engine = create_async_engine(
                connection_string,
                # Connection pool settings optimized for Lambda
                pool_size=5,  # Number of connections to maintain
                max_overflow=10,  # Additional connections under load
                pool_timeout=30,  # Seconds to wait for connection
                pool_recycle=3600,  # Recycle connections every hour
                # Lambda-specific settings
                connect_args={
                    "command_timeout": 60,  # Command timeout in seconds
                    "server_settings": {
                        "application_name": "phobos_lambda" if os.getenv("AWS_LAMBDA_FUNCTION_NAME") else "phobos_local"
                    },
                    "ssl": "require"  # Ensure SSL connection for security
                }
            )
            print(f"✅ Database engine created successfully with direct connection")
    else:
        raise ValueError("Missing database configuration parameters")

except Exception as e:
    # For testing without a real database or if configuration fails
    engine = None
    print(f"⚠️  Database connection not configured: {e}")
    print("   Using mock engine for testing. Please check your environment variables.")

# for AWS S3

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
AWS_S3_BASE_URL = os.getenv("AWS_S3_BASE_URL")

# Create S3 client
# In Lambda: Uses IAM role automatically (no credentials needed)
# Locally: Uses credentials from .env or AWS profile
try:
    if os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
        # Running in Lambda - use IAM role (no explicit credentials)
        s3_client = boto3.client("s3", region_name=AWS_REGION)
        print("✅ S3 client created using Lambda IAM role")
    else:
        # Running locally - use explicit credentials if available
        if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=AWS_REGION,
            )
            print("✅ S3 client created using explicit credentials")
        else:
            # Fall back to AWS profile from environment
            s3_client = boto3.client("s3", region_name=AWS_REGION)
            print("✅ S3 client created using AWS profile")
except Exception as e:
    s3_client = None
    print(f"⚠️  S3 client not configured: {e}")
    print("   S3 operations will not be available.")
