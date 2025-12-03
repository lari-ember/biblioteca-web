# Quick Start Guide - Book CRUD Implementation

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL running
- Existing biblioteca-web installation

### Installation Steps

#### 1. Backup Current Database
```bash
# Create database backup
pg_dump -U postgres biblioteca > backup_$(date +%Y%m%d).sql

# Or with Docker:
docker exec -t biblioteca_db pg_dump -U postgres biblioteca > backup_$(date +%Y%m%d).sql
```

#### 2. Run Database Migration
```bash
cd /home/larisssa/Documentos/codigos/biblioteca/biblioteca-web

# Run migration script
python scripts/migrate_book_crud.py
```

**Expected Output:**
```
============================================================
BOOK CRUD MIGRATION - Starting
============================================================

[1/5] Creating database schema...
✅ Schema updated successfully

[2/5] Migrating existing book format data...
✅ Updated 0 UserBooks entries with default format

[3/5] Creating default user preferences...
✅ Created preferences for X users

[4/5] Validating data integrity...
✅ All UserBooks have valid Book relationships
✅ All X users have preferences

[5/5] Migration Summary
------------------------------------------------------------
Total Users                    : X
Total Books (Catalog)          : X
Total UserBooks (Ownership)    : X
Total UserPreferences          : X
Books with ISBN                : X
Books with Description         : X

============================================================
✅ MIGRATION COMPLETED SUCCESSFULLY
============================================================
```

#### 3. Update Forms (Required)
Update `app/models/forms.py` - BookForm needs adjustment:

```python
# OLD (in forms.py)
class BookForm(FlaskForm):
    # ...
    read = SelectField('Read', choices=[('read', 'Read'), ('unread', 'Unread')])
    status = SelectField('Status', choices=[('available', 'Available'), ...])
    format = SelectField('Format', choices=[('physical', 'Physical'), ...])

# KEEP AS IS for now, but these will be moved to modal in templates
# The controller now expects these fields for backward compatibility
```

#### 4. Start the Application
```bash
# Development mode
python run.py

# Or with Docker
docker-compose up
```

#### 5. Test the Implementation

##### Test 1: Autocomplete
1. Go to `/register_new_book`
2. Type in search box (min 3 chars)
3. Should see three sections:
   - 📚 Your Collection
   - 🌐 Shared Catalog
   - 🔍 External APIs (OpenLibrary)

##### Test 2: Add Existing Book to Collection
1. Search for a book in shared catalog
2. Click "Add to Collection"
3. Modal should open with:
   - Book info displayed
   - Quantity field (default 1)
   - Format selector
   - Status selector
   - Acquisition notes
4. Fill form and submit
5. Book should appear in Your Collection

##### Test 3: View Collection
1. Go to `/your_collection`
2. Should see:
   - All your books
   - User-specific columns: quantity, format, status, read_status
   - Pagination (if >20 books)

##### Test 4: Edit Book
1. From Your Collection, click Edit
2. Should only edit user-specific fields:
   - Status
   - Read Status
   - Format
   - Quantity
   - Notes
3. Book info (title, author, etc.) should be READ-ONLY

##### Test 5: Delete Book
1. From Your Collection, click Delete
2. Confirm deletion
3. Book removed from YOUR collection
4. Book STILL EXISTS in shared catalog

---

## 📋 Feature Checklist

### Phase 1 - Core (Complete) ✅
- [x] Updated database schema
- [x] Created UserPreferences model
- [x] Implemented duplicate detection
- [x] Created metadata service
- [x] Implemented SEO decorator
- [x] Created all CRUD routes
- [x] Created accessible modal component

### Phase 2 - Templates (Next)
- [ ] Update `register_new_book.html` with new autocomplete
- [ ] Update `your_collection.html` to show new fields
- [ ] Update `view_book.html` with modal integration
- [ ] Update `base.html` with SEO metadata injection
- [ ] Update `search.html` to distinguish owned books

### Phase 3 - User Settings
- [ ] Create settings page
- [ ] Create preferences form
- [ ] Create settings template
- [ ] Add navigation link

---

## 🔧 Troubleshooting

### Issue: Migration fails with "column already exists"
**Solution**: Database already partially migrated. Either:
1. Restore from backup and re-run
2. Skip to manual schema fixes

### Issue: Import error "No module named metadata_service"
**Solution**: Restart Python/Flask to reload modules:
```bash
# Kill existing process
pkill -f "python run.py"

# Restart
python run.py
```

### Issue: Modal doesn't open
**Solution**: Include modal template in base.html:
```html
<!-- In base.html, before </body> -->
{% include 'components/add_book_modal.html' %}
```

### Issue: Autocomplete returns empty results
**Check**:
1. OpenLibrary API is accessible: `curl https://openlibrary.org/search.json?q=test`
2. Check app logs for rate limiting
3. Verify user is logged in

### Issue: Books missing format/quantity fields
**Solution**: Run data fix:
```python
from app import db
from app.models.modelsdb import UserBooks

# Fix missing formats
UserBooks.query.filter(UserBooks.format == None).update({'format': 'physical'})

# Fix missing quantities
UserBooks.query.filter(UserBooks.quantity == None).update({'quantity': 1})

db.session.commit()
```

---

## 📝 Configuration

### Optional: Adjust Rate Limits
Edit `app/services/metadata_service.py`:
```python
class MetadataService:
    REQUESTS_PER_MINUTE = 100  # Change this
    CACHE_TTL = 86400  # 24 hours
```

### Optional: Change Default Preferences
Edit `app/models/modelsdb.py`:
```python
class UserPreferences(db.Model):
    auto_add_on_search = db.Column(db.Boolean, default=True)  # Change
    show_quantity_modal = db.Column(db.Boolean, default=True)  # Change
    default_book_status = db.Column(db.String(20), default='available')
    default_format = db.Column(db.String(20), default='physical')
```

---

## 🎨 Customization

### Add Custom Book Status
1. Update UserBooks model:
```python
# In modelsdb.py
status = db.Column(db.String(20), nullable=False, default='available')
# Add validation if needed
```

2. Update modal template:
```html
<!-- In add_book_modal.html -->
<select id="statusSelect" name="status">
    <option value="available">Available</option>
    <option value="borrowed">Borrowed</option>
    <option value="ex-libris">Ex-Libris</option>
    <option value="your_status">Your Custom Status</option>
</select>
```

### Add Custom Format
Same process as above, edit the format selector.

---

## 🚨 Known Limitations

### Current Limitations:
1. **No bulk operations** - Can't add multiple books at once
2. **Basic search** - No advanced filters yet
3. **Single API source** - Only OpenLibrary (Google Books TODO)
4. **No export** - Can't export collection to CSV/JSON yet
5. **No recommendations** - No book suggestions based on collection

### Planned for Phase 4+:
- Bulk import from CSV
- Export to BibTeX, CSV, JSON
- Google Books API integration
- Advanced search with filters
- Book recommendations
- Collection statistics dashboard

---

## 📚 API Reference

### Metadata Service
```python
from app.services.metadata_service import get_metadata_service

service = get_metadata_service()

# Search OpenLibrary
results = service.search_openlibrary("Harry Potter", limit=10)

# Get book by ISBN
book = service.get_book_by_isbn("9780747532743")

# Get cover URL
url = service.get_cover_url(isbn="9780747532743", size='L')
```

### Duplicate Detection
```python
from app.controllers.books import check_duplicate_book

result = check_duplicate_book(
    title="Harry Potter",
    author="J.K. Rowling",
    isbn="9780747532743"
)

if result['exact']:
    print("Exact match found!")
elif result['similar']:
    print(f"Similar books: {len(result['similar'])}")
```

---

## 🐛 Debugging

### Enable Debug Logging
```python
# In config.py or run.py
import logging

logging.basicConfig(level=logging.DEBUG)
```

### Check Database State
```python
from app import db, create_app
from app.models.modelsdb import Book, UserBooks, UserPreferences

app = create_app()
with app.app_context():
    print(f"Books: {Book.query.count()}")
    print(f"UserBooks: {UserBooks.query.count()}")
    print(f"Preferences: {UserPreferences.query.count()}")
    
    # Check specific user
    from flask_login import current_user
    user = User.query.first()
    print(f"User {user.username} has {len(user.user_books)} books")
    print(f"Preferences: {user.preferences}")
```

### Test Metadata Service
```python
from app.services.metadata_service import get_metadata_service

service = get_metadata_service()

# Test search
results = service.search_openlibrary("test", limit=1)
print(results)

# Test ISBN lookup
book = service.get_book_by_isbn("9780747532743")
print(book)
```

---

## 📞 Support

### Getting Help:
1. Check `BOOK_CRUD_IMPLEMENTATION.md` for detailed docs
2. Review error logs in `app.log`
3. Check Flask debug output in terminal

### Reporting Issues:
Include:
- Error message
- Stack trace
- Steps to reproduce
- Browser console errors (if UI issue)

---

## ✅ Success Criteria

Your implementation is working if:
- ✅ Migration completed without errors
- ✅ Can search and see tri-source results
- ✅ Can add book via modal
- ✅ Collection page shows user-specific fields
- ✅ Can edit user-specific attributes
- ✅ Delete removes from collection but not catalog
- ✅ No console errors
- ✅ Autocomplete responds quickly (<500ms)

---

**Last Updated**: 2025-01-03  
**Version**: 1.0.0  
**Author**: GitHub Copilot

For detailed implementation info, see: `BOOK_CRUD_IMPLEMENTATION.md`

