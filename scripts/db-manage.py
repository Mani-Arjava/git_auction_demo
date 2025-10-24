#!/usr/bin/env python3
"""
Database Management Script for Phobos Backend
Handles database table creation, deletion, and reset operations
"""

import sys
import asyncio
import os
from pathlib import Path

# Add the lambda/phobos directory to Python path
project_root = Path(__file__).parent.parent
lambda_path = project_root / "lambda" / "phobos"
sys.path.insert(0, str(lambda_path))

from sqlmodel import SQLModel
from app.api.db_connection.db_config import engine


async def drop_all_tables():
    """Drop ALL tables in the database (not just SQLModel metadata tables)"""
    if not engine:
        print("❌ Database engine not configured. Check your .env file.")
        sys.exit(1)

    # Prevent running in production
    if os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
        print("❌ Cannot run database operations in Lambda/production environment!")
        sys.exit(1)

    print("🗑️  Dropping all database tables...")
    try:
        from sqlalchemy import text

        async with engine.begin() as conn:
            # First, get all tables in the public schema
            result = await conn.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_type = 'BASE TABLE'
                ORDER BY table_name
            """))
            tables = result.fetchall()

            if not tables:
                print("ℹ️  No tables found to drop")
                return True

            print(f"📋 Found {len(tables)} tables to drop:")
            for table in tables:
                print(f"   - {table[0]}")

            print("\n🗑️  Dropping tables...")
            # Drop all tables with CASCADE to handle foreign keys
            for table in tables:
                table_name = table[0]
                await conn.execute(text(f'DROP TABLE IF EXISTS "{table_name}" CASCADE'))
                print(f"   ✓ Dropped {table_name}")

        print("\n✅ All tables dropped successfully!")
        return True
    except Exception as e:
        print(f"❌ Error dropping tables: {e}")
        import traceback
        traceback.print_exc()
        return False


async def create_all_tables():
    """Create all tables defined in SQLModel metadata"""
    if not engine:
        print("❌ Database engine not configured. Check your .env file.")
        sys.exit(1)

    print("🏗️  Creating all database tables...")
    try:
        # Import all table models to register them with SQLModel metadata
        from app.api.model.appraiser.appraiser_table import AppraiserTable
        from app.api.model.bank.bank_table import BankTable
        from app.api.model.branch.branch_table import BranchTable
        from app.api.model.reappraisal_service.reappraisal_service_table import ReappraisalServiceTable
        from app.api.model.advance.advance_table import AdvanceTable
        from app.api.model.reimbursement.reimbursement_table import ReimbursementTable
        from app.api.model.payout_cycle.payout_cycle_table import PayoutCycleTable
        from app.api.model.payout_statement.payout_statement_table import PayoutStatementTable

        async with engine.begin() as conn:
            # Create all tables
            await conn.run_sync(SQLModel.metadata.create_all)

        print("✅ All tables created successfully!")
        print("\n📋 Tables created:")
        print("   - appraiser")
        print("   - bank")
        print("   - branch")
        print("   - reappraisal_service")
        print("   - advance")
        print("   - reimbursement")
        print("   - payout_cycle")
        print("   - payout_statement")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        import traceback
        traceback.print_exc()
        return False


async def list_tables():
    """List all tables in the database"""
    if not engine:
        print("❌ Database engine not configured. Check your .env file.")
        sys.exit(1)

    print("📋 Listing database tables...")
    try:
        from sqlalchemy import text

        async with engine.begin() as conn:
            result = await conn.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = result.fetchall()

            if tables:
                print(f"\n✅ Found {len(tables)} tables:")
                for table in tables:
                    print(f"   - {table[0]}")
            else:
                print("\n⚠️  No tables found in database")

        return True
    except Exception as e:
        print(f"❌ Error listing tables: {e}")
        return False


async def main():
    """Main entry point for database management"""

    if len(sys.argv) < 2:
        print("❌ Missing command argument")
        print("\nUsage:")
        print("  python scripts/db-manage.py [command]")
        print("\nCommands:")
        print("  drop    - Drop all tables (destructive!)")
        print("  create  - Create all tables from models")
        print("  reset   - Drop and recreate all tables")
        print("  list    - List all tables in database")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "drop":
        print("⚠️  WARNING: This will DROP ALL TABLES in your database!")
        print("⚠️  All data will be permanently deleted!")
        confirm = input("\nType 'DROP' to confirm: ")
        if confirm != "DROP":
            print("❌ Operation cancelled")
            sys.exit(0)

        success = await drop_all_tables()
        sys.exit(0 if success else 1)

    elif command == "create":
        success = await create_all_tables()
        sys.exit(0 if success else 1)

    elif command == "reset":
        print("⚠️  WARNING: This will DROP and RECREATE ALL TABLES!")
        print("⚠️  All data will be permanently deleted!")
        confirm = input("\nType 'RESET' to confirm: ")
        if confirm != "RESET":
            print("❌ Operation cancelled")
            sys.exit(0)

        print("\n" + "="*50)
        success = await drop_all_tables()
        if success:
            print("\n" + "="*50)
            success = await create_all_tables()

        sys.exit(0 if success else 1)

    elif command == "list":
        success = await list_tables()
        sys.exit(0 if success else 1)

    else:
        print(f"❌ Unknown command: {command}")
        print("\nAvailable commands: drop, create, reset, list")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
