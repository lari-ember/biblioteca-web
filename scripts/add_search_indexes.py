#!/usr/bin/env python3
"""
Database migration script to add search indexes safely.

Adds:
- idx_book_search on Book(title, author) for autocomplete performance
- idx_metrics_endpoint_time on APIMetrics(endpoint, timestamp) for analytics

Run this script to apply indexes to existing database without breaking data.
"""
import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.modelsdb import Book, APIMetrics
from sqlalchemy import text


def add_indexes():
    """Add search performance indexes to database."""
    app = create_app()
    
    with app.app_context():
        print("🔍 Checking database connection...")
        try:
            db.session.execute(text('SELECT 1'))
            print("✅ Database connected successfully")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
        
        print("\n📊 Adding search indexes...")
        
        try:
            # Check if idx_book_search exists
            result = db.session.execute(text(
                "SELECT indexname FROM pg_indexes WHERE indexname = 'idx_book_search'"
            )).fetchone()
            
            if result:
                print("ℹ️  Index 'idx_book_search' already exists, skipping")
            else:
                print("🔨 Creating index 'idx_book_search' on books(title, author)...")
                db.session.execute(text(
                    "CREATE INDEX CONCURRENTLY idx_book_search ON books(title, author)"
                ))
                db.session.commit()
                print("✅ Index 'idx_book_search' created successfully")
            
            # Check if idx_metrics_endpoint_time exists
            result = db.session.execute(text(
                "SELECT indexname FROM pg_indexes WHERE indexname = 'idx_metrics_endpoint_time'"
            )).fetchone()
            
            if result:
                print("ℹ️  Index 'idx_metrics_endpoint_time' already exists, skipping")
            else:
                # First ensure the table exists
                result = db.session.execute(text(
                    "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'api_metrics')"
                )).fetchone()
                
                if not result[0]:
                    print("📋 Creating api_metrics table...")
                    db.create_all()
                    print("✅ Table created")
                
                print("🔨 Creating index 'idx_metrics_endpoint_time' on api_metrics(endpoint, timestamp)...")
                db.session.execute(text(
                    "CREATE INDEX CONCURRENTLY idx_metrics_endpoint_time ON api_metrics(endpoint, timestamp)"
                ))
                db.session.commit()
                print("✅ Index 'idx_metrics_endpoint_time' created successfully")
            
            print("\n🎉 Migration completed successfully!")
            return True
            
        except Exception as e:
            print(f"\n❌ Migration failed: {e}")
            db.session.rollback()
            return False


if __name__ == '__main__':
    print("=" * 60)
    print("Database Index Migration Script")
    print("=" * 60)
    print()
    
    success = add_indexes()
    
    if success:
        print("\n✅ All indexes added successfully")
        sys.exit(0)
    else:
        print("\n❌ Migration failed")
        sys.exit(1)

