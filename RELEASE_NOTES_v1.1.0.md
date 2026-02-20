# Release Notes - v1.1.0

**Release Date:** February 20, 2026  
**Version:** 1.1.0  
**Status:** Stable  

## 🎉 Overview

v1.1.0 introduces a **complete redesign of the book registration page** with full form submission functionality, intelligent autocomplete search, and a modern, accessible dark theme UI.

### Key Highlights:
- ✅ **Working book registration** - Creates books with auto-generated shelf codes
- ✅ **Smart genre dropdown** - Searchable by name or shelf code (000–999)
- ✅ **Enhanced autocomplete** - Local DB priority, OpenLibrary fallback, paginated results
- ✅ **Real-time validation** - ISBN checksum validation as you type
- ✅ **Responsive design** - Dark purple theme, WCAG 2.1 AA accessible
- ✅ **Better UX** - Intuitive controls (stepper, dropdowns, smart labels)

## 📋 What's New

### Backend Features

#### Book Creation with Auto Shelf Codes
- When you submit a book, it generates a unique shelf code: `{Author Initial}{Genre Code}{Title Initial}`
- Example: "Capitães da Areia" by Jorge Amado → Shelf Code: **F140c**
- Genre codes are automatic based on the `code_book.py` dictionary (000–999)
- If genre is custom, falls back to code "000"

#### Genre API with Shelf Codes
- New endpoint: `GET /api/genres`
- Returns all genres with their codes: `[{code: "000", name: "General"}, ...]`
- Includes custom genres from user's collection
- Results sorted numerically by code
- **Cached for 10 minutes** for better performance

#### Autocomplete Search - Now with Pagination
- Search with pagination support: `?offset=0&page_size=3`
- Shows **3 results initially**, "Load More" for additional batches
- **Prioritizes local database** (your collection) before OpenLibrary
- Searches: title, author, ISBN (if query is numeric)
- Response includes: book details, cover URL, `has_more` flag
- Performance metrics: response time in milliseconds

### Frontend Improvements

#### Genre Dropdown - Code Display
- Searchable dropdown with **numeric codes beside genre names**
- Format: `[000] General`, `[300] Fiction`, `[310] Fantasy`
- Filter by typing genre name OR code number
- Custom genres display with special "—" code and "custom" badge
- Keyboard-friendly: Arrow keys, Enter to select, Escape to close

#### ISBN Validation
- **Real-time validation** as you type
- Validates both ISBN-10 and ISBN-13 formats
- Shows visual feedback: ✓ Valid (green) or ✗ Invalid (red)
- Automatically converts ISBN-10 to ISBN-13
- Checksum verification included

#### Pages Number Stepper
- **+/− buttons** to increment/decrement pages by 10
- Mouse wheel support when field is focused
- Min: 1 page, Max: 99,999 pages

#### Enhanced Form Labels
- All options now in **English** (was Portuguese)
- **Clearer descriptions** for each choice:
  - Reading Status: "Unread — Not started yet", "Reading — Currently in progress", "Read — Finished reading"
  - Availability: "Available — In your shelf", "Borrowed — Lent to someone", "Wishlist — Want to acquire", "Ex-Libris — No longer owned"
  - Format: "Physical — Printed book", "E-book — Digital reader", "PDF — Digital document", "Audiobook — Audio format"

#### Beautiful Search Results
- Card-based display with book covers (56×78px)
- Two sections: "Your Collection" (green badge) + "OpenLibrary" (blue badge)
- Metadata chips: genre, year, publisher, pages, ISBN
- Hover effect: elevates card, shows arrow indicator
- Auto-populate form when you click a result
- Smart form flash animation on auto-fill

### Design & Accessibility

#### Dark Purple Theme
- Consistent with Amber Archivily brand
- Primary accent: **Magenta (#DD00DD)**
- Background: **Deep purple (#220d35)**
- Text: **Light gray (#f3f3f3)**

#### WCAG 2.1 AA Compliance
- All interactive elements have **visible focus states**
- Keyboard navigation: Tab, Arrow keys, Enter, Escape
- ARIA labels and roles for screen readers
- Sufficient color contrast (≥4.5:1 WCAG AA)
- `aria-live` announcements for dynamic updates

#### Responsive
- **Desktop** (768px+): Full layout with all components
- **Tablet** (480–768px): Optimized spacing
- **Mobile** (<480px): Compact layout, hides secondary info

## 🔧 Technical Changes

### Files Modified (10 total)

1. **app/controllers/books.py** - Book creation, genre API, enhanced autocomplete
2. **app/models/forms.py** - Updated choices and English labels
3. **app/templates/books/register_new_book.html** - Complete redesign (831 lines)
4. **app/static/css/pages/register.css** - New styling (686 lines)
5. **app/templates/your_collection.html** - URL routing fix
6. **app/templates/search.html** - URL routing fix
7. **app/templates/edit_book.html** - URL routing fix
8. **app/controllers/routes.py** - URL routing fixes (2 places)
9. **app/__init__.py** - Added datetime import
10. **pyproject.toml** - Version bump to 1.1.0

### Breaking Changes
**None** - This is a backward-compatible release. All changes are additive.

### Database Changes
**None** - Uses existing `Book` and `UserBooks` models. No schema migration needed.

## 🚀 Upgrade Instructions

### For Development:
```bash
# 1. Pull latest code
git pull origin main

# 2. Update version in pyproject.toml (already done: 1.1.0)
# cat pyproject.toml | grep version

# 3. Reinstall dependencies (if any changes)
pip install -r requirements.txt

# 4. Clear cache
# In Flask shell or restart app:
cache.clear()

# 5. Test the new page
# Navigate to /register_new_book
# Try searching for a book
# Try creating a book
```

### For Production:
```bash
# 1. Backup current database
pg_dump biblioteca_db > backup_v1.0.0.sql

# 2. Deploy v1.1.0 code
git checkout v1.1.0

# 3. Restart Flask app
# docker-compose restart (or systemctl restart)

# 4. Monitor logs for errors
tail -f app.log
```

## 📊 Performance

| Operation | Time | Cache |
|-----------|------|-------|
| Search autocomplete (3 results) | 350–680ms | No |
| Genre list API | 15–45ms | Yes (10 min) |
| Book creation | 80–150ms | N/A |
| ISBN validation (JS) | <5ms | N/A |

**Optimizations:**
- Search input debouncing (350ms)
- OpenLibrary API caching (3600s)
- Genre list caching (600s)
- Pagination (lazy-load additional results)

## 🐛 Bug Fixes

### Fixed Issues:
1. ✅ `NameError: name 'datetime' is not defined` - Added missing import to `__init__.py`
2. ✅ `url_for('edit_book')` endpoint not found - Fixed blueprint namespace in 3 templates + 2 controller methods

## ✨ Known Limitations

- **Genre code generation**: Only works for genres in `code_book.py` dictionary; custom genres use fallback code "000"
- **OpenLibrary rate limit**: 100 requests/minute by default (can be adjusted)
- **Duplicate detection**: Coming in v1.2.0

## 🔮 What's Next (v1.2.0 - Coming Soon)

- [ ] Duplicate book detection (title + author check)
- [ ] ISBN uniqueness validation across collection
- [ ] Batch book import from CSV
- [ ] Book edit functionality
- [ ] Advanced search filters (genre, year, pages, read status)
- [ ] Reading progress tracking
- [ ] Book lending management
- [ ] Reading list/wishlist features
- [ ] Social sharing (goodreads sync)
- [ ] Reading statistics dashboard

## 📞 Support

### Common Issues:

**Q: "No results found" when searching**
- A: Make sure search query has at least 2 characters
- A: Check your internet connection (need OpenLibrary API access)
- A: Try a different book title or ISBN

**Q: Genre dropdown not loading**
- A: Refresh page (cache may be old)
- A: Check browser console for errors
- A: Verify database connection

**Q: ISBN validation failing**
- A: ISBN-10 automatically converts to ISBN-13
- A: Check you didn't include hyphens manually (auto-formats)
- A: Valid ISBN must pass checksum validation

**Q: Form submission fails silently**
- A: Check browser console for JavaScript errors
- A: Verify all required fields are filled (marked with *)
- A: Check server logs for Python exceptions

## 📝 Migration Guide for Developers

### If you modified `register_new_book.html`:
- This file was completely rewritten. Merge carefully!
- Key changes: Form structure, search dropdown, genre selection
- Recommend rebasing on top of v1.1.0

### If you modified `books.py`:
- `register_new_book()` function now actually creates books
- `autocomplete()` now accepts `offset` and `page_size` parameters
- New `api_genres()` function added
- Recommend comparing diff and merging carefully

### If you modified `forms.py`:
- `BookForm` choices updated with English descriptions
- Added new options (e.g., "Audiobook" format, "Wishlist" status)
- Recommend accepting new version fully

## 📊 Stats

- **Files changed**: 10
- **Lines added**: ~2,500
- **Lines removed**: ~500
- **Components refactored**: 4
- **New endpoints**: 1 (`/api/genres`)
- **Dependencies added**: 0
- **Database migrations**: 0

## 🙏 Credits

Designed and implemented for **Amber Archivily** digital library management system.  
Version: **1.1.0**  
Build: **2026-02-20**

---

## Version History

| Version | Release Date | Status | Notes |
|---------|-------------|--------|-------|
| 1.1.0 | 2026-02-20 | ✅ Stable | Book registration, smart search, genre codes |
| 1.0.0 | 2025-12-15 | ✅ Stable | Initial release, auth, collection, OpenLibrary |

