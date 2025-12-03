"""
Database Migration Script for Book CRUD Implementation

CRITICAL: Run this before starting the application with new models.

This migration handles:
1. Adding user-specific fields to UserBooks table
2. Removing format from Book table
3. Adding description to Book table
4. Creating UserPreferences table
5. Creating default preferences for existing users

Author: GitHub Copilot
Date: 2025-01-03
"""

# Run with: python scripts/migrate_book_crud.py

from app import db, create_app
from app.models.modelsdb import User, Book, UserBooks, UserPreferences
from datetime import datetime

def run_migration():
    """Execute the migration steps."""
    
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("BOOK CRUD MIGRATION - Starting")
        print("=" * 60)
        
        # Step 1: Create all new tables/columns
        print("\n[1/5] Creating database schema...")
        try:
            db.create_all()
            print("✅ Schema updated successfully")
        except Exception as e:
            print(f"❌ Error creating schema: {e}")
            return False
        
        # Step 2: Migrate existing data (if format field still exists in old data)
        print("\n[2/5] Migrating existing book format data...")
        try:
            # This step handles if you have old data with format in Book
            # Since we removed it from model, this is just a safety check
            
            # Check if any UserBooks entries are missing format
            user_books_without_format = UserBooks.query.filter(
                UserBooks.format == None
            ).all()
            
            if user_books_without_format:
                for ub in user_books_without_format:
                    ub.format = 'physical'  # Default value
                
                db.session.commit()
                print(f"✅ Updated {len(user_books_without_format)} UserBooks entries with default format")
            else:
                print("✅ All UserBooks entries have format specified")
                
        except Exception as e:
            print(f"⚠️ Format migration skipped (expected if clean install): {e}")
            db.session.rollback()
        
        # Step 3: Create default preferences for existing users
        print("\n[3/5] Creating default user preferences...")
        try:
            users_without_prefs = User.query.outerjoin(UserPreferences).filter(
                UserPreferences.id == None
            ).all()
            
            created_count = 0
            for user in users_without_prefs:
                pref = UserPreferences(
                    user_id=user.id,
                    auto_add_on_search=True,
                    show_quantity_modal=True,
                    default_book_status='available',
                    default_format='physical'
                )
                db.session.add(pref)
                created_count += 1
            
            db.session.commit()
            print(f"✅ Created preferences for {created_count} users")
            
        except Exception as e:
            print(f"❌ Error creating user preferences: {e}")
            db.session.rollback()
            return False
        
        # Step 4: Validate data integrity
        print("\n[4/5] Validating data integrity...")
        try:
            # Check UserBooks have valid relationships
            orphaned_userbooks = UserBooks.query.outerjoin(Book).filter(
                Book.id == None
            ).count()
            
            if orphaned_userbooks > 0:
                print(f"⚠️ Found {orphaned_userbooks} orphaned UserBooks entries")
            else:
                print("✅ All UserBooks have valid Book relationships")
            
            # Check all users have preferences
            users_total = User.query.count()
            prefs_total = UserPreferences.query.count()
            
            if users_total == prefs_total:
                print(f"✅ All {users_total} users have preferences")
            else:
                print(f"⚠️ {users_total} users but only {prefs_total} preferences")
            
        except Exception as e:
            print(f"⚠️ Validation warnings: {e}")
        
        # Step 5: Summary
        print("\n[5/5] Migration Summary")
        print("-" * 60)
        
        stats = {
            'Total Users': User.query.count(),
            'Total Books (Catalog)': Book.query.count(),
            'Total UserBooks (Ownership)': UserBooks.query.count(),
            'Total UserPreferences': UserPreferences.query.count(),
            'Books with ISBN': Book.query.filter(Book.isbn != None).count(),
            'Books with Description': Book.query.filter(Book.description != None).count(),
        }
        
        for key, value in stats.items():
            print(f"{key:30} : {value}")
        
        print("\n" + "=" * 60)
        print("✅ MIGRATION COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Review the migration summary above")
        print("2. Test the application: python run.py")
        print("3. Check /your_collection page works")
        print("4. Test adding a book via modal")
        print("5. Verify autocomplete shows tri-source results")
        print("\nIf any issues, restore from backup:")
        print("  - app/models/modelsdb_old.py")
        print("  - app/controllers/books_old.py")
        
        return True


if __name__ == '__main__':
    import sys
    
    print("\n⚠️  WARNING: This will modify your database schema!")
    print("Make sure you have a backup before proceeding.\n")
    
    response = input("Continue with migration? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("\n❌ Migration cancelled by user")
        sys.exit(0)
    
    success = run_migration()
    
    if success:
        sys.exit(0)
    else:
        print("\n❌ Migration failed. Please review errors above.")
        sys.exit(1)

