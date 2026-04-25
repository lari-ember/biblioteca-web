"""
Add book metadata columns for country_of_origin and original_language.

Run with:
    python scripts/migrate_book_metadata.py
"""

from sqlalchemy import inspect, text
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app, db


def run_migration():
    app = create_app()
    with app.app_context():
        inspector = inspect(db.engine)
        columns = {col['name'] for col in inspector.get_columns('books')}
        pending = []

        if 'country_of_origin' not in columns:
            pending.append("ALTER TABLE books ADD COLUMN country_of_origin VARCHAR(80)")
        if 'original_language' not in columns:
            pending.append("ALTER TABLE books ADD COLUMN original_language VARCHAR(40)")

        if not pending:
            print('No schema changes needed. Migration already applied.')
            return

        for statement in pending:
            db.session.execute(text(statement))

        db.session.commit()
        print(f'Migration completed. Applied {len(pending)} schema change(s).')


if __name__ == '__main__':
    run_migration()

