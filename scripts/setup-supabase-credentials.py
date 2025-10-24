#!/usr/bin/env python3
"""
Supabase Credentials Setup Script for Phobos Backend

This script helps you set up and test Supabase database credentials.
"""

import os
import sys
from pathlib import Path

def get_project_root():
    """Get the project root directory"""
    return Path(__file__).parent.parent

def load_env_file():
    """Load environment variables from .env file"""
    project_root = get_project_root()
    env_file = project_root / ".env"

    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        print(f"✅ Loaded environment from {env_file}")
    else:
        print(f"❌ .env file not found at {env_file}")
        return False
    return True

def check_current_config():
    """Check current Supabase configuration"""
    print("\n📋 Current Supabase Configuration:")
    print("=" * 50)

    required_vars = [
        'SUPABASE_HOST',
        'SUPABASE_USER',
        'SUPABASE_PASSWORD',
        'SUPABASE_PORT',
        'SUPABASE_DATABASE',
        'SUPABASE_URL',
        'SUPABASE_ANON_KEY'
    ]

    config = {}
    all_set = True

    for var in required_vars:
        value = os.getenv(var, 'NOT SET')
        config[var] = value

        if var == 'SUPABASE_PASSWORD':
            status = "✅ SET" if value and value != 'your-supabase-password-here' else "❌ NOT SET"
        elif var in ['SUPABASE_HOST', 'SUPABASE_URL']:
            status = "✅ SET" if value and 'supabase.co' in value else "❌ NOT SET"
        elif var == 'SUPABASE_ANON_KEY':
            status = "✅ SET" if value and len(value) > 50 else "❌ NOT SET"
        else:
            status = "✅ SET" if value and value != 'NOT SET' else "❌ NOT SET"

        print(f"{var:20} : {status}")
        if var == 'SUPABASE_PASSWORD' and value and value != 'your-supabase-password-here':
            print(f"{'':20}   Length: {len(value)} characters")
        elif var != 'SUPABASE_PASSWORD':
            print(f"{'':20}   Value: {value[:50]}{'...' if len(value) > 50 else ''}")

        if value == 'NOT SET' or (var == 'SUPABASE_PASSWORD' and value == 'your-supabase-password-here'):
            all_set = False

    return config, all_set

def generate_connection_string(config):
    """Generate the database connection string"""
    if not config.get('SUPABASE_PASSWORD') or config['SUPABASE_PASSWORD'] == 'your-supabase-password-here':
        return None

    return (
        f"postgresql+asyncpg://{config['SUPABASE_USER']}:{config['SUPABASE_PASSWORD']}"
        f"@{config['SUPABASE_HOST']}:{config['SUPABASE_PORT']}/{config['SUPABASE_DATABASE']}"
    )

def test_database_connection():
    """Test the database connection using the application's db_config"""
    try:
        # Add the lambda directory to Python path
        lambda_dir = get_project_root() / "lambda" / "phobos"
        sys.path.insert(0, str(lambda_dir))

        from app.api.db_connection.db_config import engine

        if engine:
            print("✅ Database engine created successfully")
            return True
        else:
            print("❌ Database engine not created - check configuration")
            return False

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure dependencies are installed: cd lambda/phobos && uv pip install -e .")
        return False
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def print_setup_instructions():
    """Print instructions for setting up the password"""
    print("\n🔧 Setup Instructions:")
    print("=" * 50)
    print("1. Go to your Supabase Dashboard:")
    print("   https://supabase.com/dashboard/project/itdpeuznyceklottqpaj/settings/database")
    print()
    print("2. Scroll down to 'Connection string' section")
    print("3. Click 'Connect' button to reveal the connection string")
    print("4. Copy the password from the connection string:")
    print("   Format: postgresql://postgres:[PASSWORD]@db.itdpeuznyceklottqpaj.supabase.co:5432/postgres")
    print()
    print("5. Update your .env file:")
    print("   Replace: SUPABASE_PASSWORD=your-supabase-password-here")
    print("   With:    SUPABASE_PASSWORD=your-actual-password")
    print()
    print("6. Run this script again to test the connection")

def main():
    print("🚀 Supabase Credentials Setup for Phobos Backend")
    print("=" * 60)

    # Load environment variables
    if not load_env_file():
        sys.exit(1)

    # Check current configuration
    config, all_set = check_current_config()

    # Generate connection string if password is set
    connection_string = generate_connection_string(config)
    if connection_string:
        print(f"\n🔗 Generated Connection String:")
        print(f"   {connection_string}")

    # Test database connection
    print(f"\n🧪 Testing Database Connection:")
    print("=" * 30)
    connection_works = test_database_connection()

    # Print results and next steps
    print(f"\n📊 Summary:")
    print("=" * 20)
    if all_set and connection_works:
        print("✅ All credentials are properly configured!")
        print("✅ Database connection is working!")
        print("\n🎉 Your Phobos Backend is ready to use!")
        print("\nNext steps:")
        print("  • Run 'make test-local' to start the development server")
        print("  • Run 'make build && make deploy' to deploy to AWS Lambda")
    else:
        print("❌ Configuration needs attention")
        if not all_set:
            print_setup_instructions()

        if not connection_works:
            print("\n🔍 Connection Issues:")
            print("   • Check if all environment variables are set")
            print("   • Verify the password is correct")
            print("   • Ensure dependencies are installed")
            print("   • Check network connectivity")

if __name__ == "__main__":
    main()