# 📚 Biblioteca Web

**Biblioteca Web** is a personal digital library management system built with Flask and PostgreSQL. It lets you catalogue your book collection, track your reading progress, lend books to friends, and discover new titles via the OpenLibrary API — all from a responsive, dark-themed web interface.

---

## ✨ Features

- **Book catalogue** — Add, edit, and organise every book you own (physical, e-book, PDF, or audiobook).
- **Automatic shelf codes** — Each book gets a unique code derived from author, genre, and title (e.g. `J140c`).
- **Smart search & autocomplete** — Searches your local collection first, then falls back to the OpenLibrary API with paginated results.
- **Genre dropdown with codes** — 1 000-entry DDC-style genre list (codes 000–999), filterable and keyboard-navigable.
- **ISBN validation** — Real-time ISBN-10/13 checksum validation in the browser.
- **Reading status tracking** — Mark books as *Unread*, *Reading*, or *Read*, with a dedicated reading log.
- **Collection status** — Flag books as *Available*, *Borrowed*, *Wishlist*, or *Ex-Libris*.
- **Loan management** — Record who borrowed a book and when.
- **User authentication** — Secure sign-up/login with session management and CSRF protection.
- **Rate limiting** — Built-in request throttling (200 req/day, 50 req/hour per IP).
- **Accessible UI** — WCAG 2.1 AA compliant; full keyboard navigation support.
- **Responsive design** — Works on desktop, tablet, and mobile.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, Flask 3.0 |
| Database | PostgreSQL 13, SQLAlchemy 2.0 |
| Auth | Flask-Login, Flask-WTF (CSRF) |
| Caching | Flask-Caching |
| Rate limiting | Flask-Limiter |
| Frontend | Jinja2 templates, vanilla JavaScript, CSS3 |
| External API | [OpenLibrary](https://openlibrary.org/developers/api) |
| Dev environment | Docker Compose, Gunicorn |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or later
- Docker & Docker Compose (recommended)
- PostgreSQL 13+ (if running without Docker)

### Option A — Docker (recommended)

```bash
git clone https://github.com/lari-ember/biblioteca-web.git
cd biblioteca-web

# Copy and edit environment variables
cp .env.example .env   # adjust SECRET_KEY, DATABASE_URL, etc.

# Start the app and database
docker-compose -f docker-compose.dev.yml up --build
```

The application will be available at **http://localhost:8080**.

### Option B — Local setup

```bash
git clone https://github.com/lari-ember/biblioteca-web.git
cd biblioteca-web

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements.txt
pip install -r requirements-dev.txt

# Set required environment variables
export SECRET_KEY="your-secret-key"
export DATABASE_URL="postgresql://user:password@localhost:5432/biblioteca"
export FLASK_APP=run.py
export FLASK_ENV=development

flask run --port 8080
```

---

## ⚙️ Environment Variables

| Variable | Description | Default (dev only) |
|---|---|---|
| `SECRET_KEY` | Flask secret key for sessions | `dev-secret-key-fallback` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:senha_dev@db:5432/biblioteca` |
| `FLASK_ENV` | `development` or `production` | `development` |

> ⚠️ Never use the default values in production.

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

Run only fast unit tests:

```bash
pytest tests/ -v -m "not slow and not integration"
```

Check test coverage:

```bash
pytest --cov=app tests/
```

---

## 📁 Project Structure

```
biblioteca-web/
├── app/
│   ├── __init__.py          # Application factory
│   ├── controllers/         # Route handlers (blueprints)
│   │   ├── auth.py          # Authentication routes
│   │   ├── books.py         # Book management & API routes
│   │   └── routes.py        # Core / miscellaneous routes
│   ├── models/
│   │   ├── modelsdb.py      # SQLAlchemy models (User, Book, UserBooks, …)
│   │   ├── forms.py         # WTForms form definitions
│   │   ├── book_search.py   # OpenLibrary search helpers
│   │   └── code_book.py     # Shelf code generation
│   ├── security/            # Security middleware & headers
│   ├── services/            # Business logic services
│   ├── static/              # CSS, JavaScript, images
│   ├── templates/           # Jinja2 HTML templates
│   ├── translations/        # i18n string files
│   └── utils/               # Shared utility functions
├── config/                  # Environment configuration files
├── data/                    # Sample/seed data
├── docs/                    # Extended documentation
├── nginx/                   # Nginx reverse-proxy config
├── scripts/                 # Utility / maintenance scripts
├── tests/                   # Pytest test suite
├── config.py                # Flask app configuration
├── docker-compose.dev.yml   # Development Docker Compose
├── Dockerfile.dev           # Development Docker image
├── pyproject.toml           # Project metadata & tool config
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
└── run.py                   # Application entry point
```

---

## 🔑 Key API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Home / landing page |
| `GET/POST` | `/login` | User login |
| `GET/POST` | `/register` | User sign-up |
| `GET` | `/your_collection` | Personal book collection |
| `GET/POST` | `/register_new_book` | Add a new book |
| `GET/POST` | `/edit_book/<id>` | Edit book details |
| `GET` | `/search` | Full-text book search |
| `GET` | `/autocomplete` | Autocomplete (local + OpenLibrary) |
| `GET` | `/api/genres` | Genre list with DDC shelf codes |
| `GET` | `/health` | Health check |

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a pull request.

1. Fork the repository.
2. Create a feature branch: `git checkout -b feat/your-feature`.
3. Commit your changes following the project conventions.
4. Push to your fork and open a pull request.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👩‍💻 Author

**Larissa Ember** — [larissaember0@gmail.com](mailto:larissaember0@gmail.com)
