a# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.4] - 2026-02-22

### Added

#### UI/UX Visual Enhancements - Register New Book Page

**CSS Styling (`app/static/css/pages/register.css`):**
- ✅ **Glassmorphism Effects**: Added `backdrop-filter: blur(8px-10px)` to major containers (autocomplete results, result cards, genre dropdown, no-results message) for modern frosted glass appearance
- ✅ **Enhanced Border System**: Updated all components with 2px solid borders for better visual separation:
  - Primary cards: `rgba(221, 0, 221, 0.35)` magenta border
  - Search input: `rgba(221, 0, 221, 0.35)` border
  - Form fields: `rgba(221, 0, 221, 0.25)` border
  - Result items: `rgba(221, 0, 221, 0.3)` border with 1.5px thickness
  - Load more button: `rgba(221, 0, 221, 0.4)` border
  - Genre dropdown: `rgba(221, 0, 221, 0.4)` border with glassmorphism
  - Warning elements: `rgba(255, 107, 107, 0.4)` red border
- ✅ **3D Hover Effects**: Result items now lift on hover with:
  - `transform: translateY(-4px)` for floating effect
  - Enhanced shadow: `0 8px 24px rgba(221, 0, 221, 0.2)`
  - Smooth 0.3s transition timing
  - Visual feedback indicating interactivity
- ✅ **Dual-Layer Shadow System**: Implemented professional shadow depth:
  - Drop shadows for elevation effect
  - Inset highlights (0.08-0.12 alpha white) for subtle top lighting
  - Default: `0 4px 12px`, Hover: `0 8px 24px`, Containers: `0 12px 36px`
- ✅ **Search Input Text Color**: Changed text color to pure white (`#ffffff`) with improved placeholder contrast (`rgba(255, 255, 255, 0.5)`)

#### Search Algorithm Improvement

**Backend (`app/controllers/books.py`):**
- ✅ **Title-Based Search Prioritization**: Changed local database search from "contains anywhere" (`%query%`) to "starts with" (`query%`) pattern
  - Results now prioritize titles beginning with search query
  - Example: "a casa" returns only "A CASA", "A CASA PEQUENA", etc., not "BANCO MERCANTIL C.A. S.A.C.A"
  - Author search remains flexible with "contains anywhere" pattern for name variations
  - ISBN search maintains "contains" pattern for formatting flexibility

#### Template Infrastructure

**Base Template (`app/templates/base.html`):**
- ✅ **Added `{% block head %}` Block**: Enables child templates to inject page-specific CSS
  - Positioned before closing `</head>` tag
  - Allows proper template inheritance for page-specific styling
  - Fixed register.css loading issue

#### Placeholder Image System

**Frontend (`app/templates/books/register_new_book.html`):**
- ✅ **Random Generic Placeholder Images**: Implemented smart fallback for books without covers:
  - Array of 4 existing generic images: `cine_metah.jpg`, `elevator_painting.jpg`, `jalaish-ill.png`, `wallpaper.jpg`
  - Random selection function: `getRandomPlaceholder()` with fair 25% distribution per image
  - Applied to both primary image and fallback: `item.cover_url || getRandomPlaceholder()`
  - Eliminates 404 errors for missing placeholder
  - Adds visual diversity to autocomplete results
  - Works seamlessly with lazy loading

### Changed

- **CSS Components**: All border styles updated to 2px thickness with consistent magenta color scheme
- **Visual Design**: More polished, modern appearance with glassmorphism and 3D effects
- **Search Results**: Improved relevance with title-based prioritization
- **Placeholder Handling**: Dynamic image selection instead of static file

### Improved

- **Visual Hierarchy**: Clearer element separation with enhanced borders and depth
- **User Engagement**: 3D hover effects and glassmorphism create more interactive feel
- **Search Accuracy**: Title search now returns more relevant results first
- **Design Consistency**: All UI elements follow unified styling system
- **Accessibility**: Enhanced contrast and focus states maintained

### Fixed

- **Template Inheritance**: Child templates can now properly extend `base.html` with page-specific CSS
- **Placeholder Images**: No more 404 errors; all books without covers display generic images successfully
- **Search Results**: No more irrelevant results when typing specific titles

---

## [1.1.0] - 2026-02-20

### Added

#### Book Registration Page - Complete Redesign

**Backend:**
- ✅ **Form Submission Implementation** (`app/controllers/books.py`):
  - Implemented actual book creation with automatic shelf code generation
  - Creates `Book` record with all metadata (title, author, publisher, year, pages, genre, ISBN, cover URL)
  - Creates `UserBooks` link with user-specific attributes (status, read_status, format, acquisition_date)
  - Automatic shelf code generation: `{AuthorInitial}{GenreCode}{TitleInitial}` (e.g., `F140c`)
  - Fallback code generation for custom genres using code `000`
  - Cache invalidation to ensure new book appears immediately in collection
  - Success flash message with book title, author, and generated code
  - Graceful error handling with detailed flash messages
  - Form validation error display for each field

- ✅ **Genre API Endpoint** (`app/controllers/books.py` - `/api/genres`):
  - Returns all genres from `book_genres` dictionary (codes 000–999)
  - Genres sorted numerically by code
  - Returns format: `[{code: "000", name: "General"}, {code: "001", name: "Essay"}, ...]`
  - Includes user's custom genres (not in master list) as separate category
  - Caching with 10-minute TTL (600 seconds) for performance

- ✅ **Autocomplete Endpoint Improvements** (`app/controllers/books.py` - `/autocomplete`):
  - Pagination support with `offset` and `page_size` parameters
  - Returns results in batches of 3 (configurable)
  - `has_more` flag to indicate if more results available
  - Prioritizes local database search before OpenLibrary fallback
  - ISBN search support (searches ISBN field if query is numeric)
  - Combined results: local collection first, then OpenLibrary suggestions
  - Performance metrics: response time in milliseconds
  - Detailed logging for debugging

**Frontend:**
- ✅ **Genre Dropdown - Enhanced UX** (`app/templates/books/register_new_book.html`):
  - Filterable/searchable genre dropdown with code display
  - Format: `[000] General`, `[300] Fiction`, etc.
  - Real-time filtering by genre name or code number
  - Custom genres display with "custom" tag and "—" code badge
  - "New genre" hint when user types non-existent genre name
  - Keyboard navigation (Arrow Up/Down, Enter, Escape)
  - Smart text extraction from option HTML

- ✅ **ISBN Validation** (`app/templates/books/register_new_book.html`):
  - Live validation for ISBN-10 and ISBN-13
  - Real-time checksum validation
  - Visual feedback: ✓ Valid or ✗ Invalid with icon
  - Auto-format as user types
  - Optional field with helpful placeholder example
  - Fallback gracefully if invalid

- ✅ **Pages Stepper** (`app/templates/books/register_new_book.html`):
  - +/- buttons for incrementing/decrementing pages by 10
  - Mouse wheel support when field is focused
  - Min: 1 page, Max: 99,999 pages
  - Number-only input mode

- ✅ **Book Search Results** (`app/templates/books/register_new_book.html`):
  - Beautiful card-based result display with book covers
  - "Your Collection" and "OpenLibrary" sections with icons
  - Metadata chips: pages, ISBN, genre, year, publisher
  - Badge distinction: "Your Collection" (green), "OpenLibrary" (blue)
  - Arrow indicator on hover showing result is selectable
  - Pagination with "Load More" button (shows 3 results initially)
  - Auto-hides when query < 2 characters
  - "No results found" message when applicable

- ✅ **Form Field Styling** (`app/templates/books/register_new_book.html`):
  - All fields translated to English (was Portuguese)
  - Clearer, more descriptive option labels with icons:
    - Reading Status: "📚 Unread", "📖 Reading", "✅ Read" → "Unread — Not started yet", etc.
    - Availability: "🟢 Available", "🔄 Borrowed", "⭐ Wishlist", "📤 Ex-Libris" → "Available — In your shelf", etc.
    - Format: "📕 Physical", "📱 E-book", "📄 PDF", "🎧 Audiobook" → "Physical — Printed book", etc.

**CSS/Design:**
- ✅ **Complete Visual Redesign** (`app/static/css/pages/register.css`):
  - Dark purple theme consistent with Amber Archivily brand:
    - Background: `#351235` / `rgba(34, 13, 53, 0.96)`
    - Accent: `#DD00DD` (magenta)
    - Text: `#f3f3f3` (light gray)
  - Search results initially hidden (no "noise" on page load)
  - Clear visual hierarchy with section labels and dividers
  - Genre code badges: monospaced, magenta-accented, 36px wide
  - ISBN validation status indicators with icons
  - Pages stepper buttons with intuitive +/- icons
  - "Load More" button with gradient and hover effects
  - All interactive elements have visible focus states (WCAG 2.1 AA)
  - Responsive design: desktop (768px+), tablet (480-768px), mobile (<480px)
  - Custom scrollbar styling in dropdown menus
  - Field flash animation when auto-populated from search results
  - Improved contrast ratios for accessibility

**Accessibility (WCAG 2.1 AA):**
- ✅ ARIA labels for all interactive elements
- ✅ Role attributes: `combobox`, `listbox`, `option`, `presentation`
- ✅ `aria-expanded`, `aria-controls`, `aria-activedescendant` for dropdown management
- ✅ `aria-live="polite"` for dynamic content updates
- ✅ Visible focus indicators on all interactive elements
- ✅ Keyboard navigation support (Tab, Arrow keys, Enter, Escape)
- ✅ Semantic HTML structure with proper heading hierarchy
- ✅ Skip link support (existing base.html)
- ✅ Screen reader friendly error messages

### Fixed

- ✅ **Import Errors** (`app/__init__.py`):
  - Added missing `from datetime import datetime` import
  - Fixed `NameError: name 'datetime' is not defined` in `timeago_filter` function

- ✅ **URL Routing Issues** (`app/templates/*.html`):
  - Fixed `url_for('edit_book', ...)` → `url_for('books.edit_book', ...)`
  - Fixed `url_for('your_collection', ...)` → `url_for('books.your_collection', ...)`
  - Updated in: `your_collection.html`, `search.html`, `edit_book.html`
  - Updated redirects in `app/controllers/routes.py`

- ✅ **Form Choices** (`app/models/forms.py`):
  - Removed emoji from form choice labels (was inconsistent)
  - Updated `ReadingStatus`, `Availability`, and `Format` choices with descriptive text
  - Added default values to SelectFields

### Changed

- ✅ **Form Implementation** (`app/models/forms.py`):
  - `BookForm.read`: Renamed to "Reading Status" with clearer options
  - `BookForm.status`: Renamed to "Availability" with more intuitive descriptions
  - `BookForm.format`: Updated with "Audiobook" option
  - All labels now in English (was pt-BR)

- ✅ **Page Visibility** (`app/templates/books/register_new_book.html`):
  - Search results container: hidden by default with `display:none`
  - "Load More" button: hidden initially
  - "No results" message: hidden initially
  - Only show when search query ≥ 2 characters

- ✅ **API Response Format** (`app/controllers/books.py`):
  - `/api/genres`: Changed from string list to object array with codes
  - Format change: `["General", "Fiction"]` → `[{code: "000", name: "General"}, ...]`

### Technical Details

#### Files Modified

1. **`app/controllers/books.py`** (363 lines)
   - Updated `register_new_book()`: Form submission with actual DB creation
   - Enhanced `autocomplete()`: Pagination support, better logging
   - New `api_genres()`: Genre API with shelf codes

2. **`app/models/forms.py`** (77 lines)
   - Updated `BookForm` with new choices and English labels

3. **`app/templates/books/register_new_book.html`** (831 lines)
   - Complete rewrite with new UI/UX
   - Added genre dropdown with code display
   - Enhanced search results rendering
   - ISBN validation and pages stepper
   - 500+ lines of JavaScript for interactivity

4. **`app/static/css/pages/register.css`** (686 lines)
   - Complete redesign from scratch
   - Dark purple theme with magenta accents
   - Responsive layout
   - Focus state styling for accessibility

5. **`app/templates/your_collection.html`**
   - Fixed `url_for('books.edit_book', ...)`

6. **`app/templates/search.html`**
   - Fixed `url_for('books.edit_book', ...)`

7. **`app/templates/edit_book.html`**
   - Fixed `url_for('books.edit_book', ...)`

8. **`app/controllers/routes.py`**
   - Fixed `url_for('books.your_collection', ...)`

9. **`app/__init__.py`**
   - Added `from datetime import datetime` import

10. **`pyproject.toml`**
    - Version bump: `1.0.0` → `1.1.0`

#### Database Changes

- ✅ No database schema changes (uses existing `Book` and `UserBooks` models)
- ✅ Shelf code generation: `generate_book_code()` from `code_book.py`
- ✅ Automatic genre code mapping (000–999)

#### Performance Improvements

- ✅ Pagination: Show 3 results initially, lazy-load more
- ✅ Cache: 10-minute TTL on genre list
- ✅ Debounce: 350ms delay on search input
- ✅ Query optimization: Single query per local search + single API call per offset

#### Browser Support

- ✅ Modern browsers (Chrome, Firefox, Safari, Edge)
- ✅ ES2015+ JavaScript (no IE11 support)
- ✅ CSS Grid and Flexbox
- ✅ Smooth scroll behavior

### Known Limitations

- Genre code generation only works for genres in `book_genres` dictionary
- Custom genres use fallback code "000"
- OpenLibrary API has rate limit (100 requests/minute by default)
- ISBN validation doesn't check against existing books (will be added in v1.2.0)

### Next Steps (v1.2.0)

- [ ] Duplicate book detection (title + author)
- [ ] ISBN uniqueness check
- [ ] Batch book import from CSV
- [ ] Book edit functionality
- [ ] Advanced search filters
- [ ] Reading progress tracking
- [ ] Book lending management
- [ ] Reading list/wishlist features

---

## [1.0.0] - 2025-12-15

### Initial Release

- User authentication and authorization
- Book collection management
- OpenLibrary API integration
- Search functionality
- User preferences
- Responsive design
- Dark theme support

