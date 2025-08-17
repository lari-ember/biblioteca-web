# 📚 Biblioteca Web - Personal Library Management System

> A comprehensive digital library management system built with Flask, featuring automated book metadata retrieval, user authentication, and advanced book organization capabilities.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-green.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](https://www.docker.com/)

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Architecture Overview](#-architecture-overview)
- [Configuration](#-configuration)
- [Testing](#-testing)
- [Performance Optimization](#-performance-optimization)
- [Deployment](#-deployment)
- [API Documentation](#-api-documentation)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)
- [Security](#-security)
- [Additional Resources](#-additional-resources)

## 🌟 Features

### 📖 Book Management
- **Smart Book Registration**: Automatic ISBN lookup and metadata retrieval from Open Library API
- **Intelligent Cover Detection**: Automatic book cover fetching with fallback mechanisms
- **Advanced Cataloging System**: Dewey-inspired classification with custom genre codes
- **Reading Progress Tracking**: Monitor current readings with page progress and completion dates
- **Book Lending System**: Track borrowed and lent books between users

### 👤 User Experience
- **Secure Authentication**: Flask-Login with password hashing and session management
- **Personal Collections**: Private book libraries with customizable organization
- **Advanced Search**: Multi-field search with filters (author, genre, year, format, etc.)
- **Reading Analytics**: Track pages read, completion dates, and reading statistics

### 🔧 Technical Features
- **RESTful API Design**: Clean, maintainable route structure
- **Database Migrations**: SQLAlchemy ORM with relationship management
- **Caching Layer**: Flask-Caching for improved performance
- **Security Headers**: CSRF protection and secure session handling
- **Docker Support**: Complete containerization with PostgreSQL and Nginx
- **Responsive Design**: Mobile-friendly CSS with modern UI components

## 🚀 Quick Start

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- [Git](https://git-scm.com/)
- Python 3.10+ (for local development)

### 1. Clone and Setup
```bash
git clone https://github.com/lari-ember/biblioteca-web.git
cd biblioteca-web
```

### 2. Environment Configuration
Create a `.env` file in the root directory:
```env
# Security
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=development

# Database
DATABASE_URL=postgresql://postgres:senha_dev@db:5432/biblioteca
POSTGRES_DB=biblioteca
POSTGRES_USER=postgres
POSTGRES_PASSWORD=senha_dev

# Optional: API Keys
OPENLIBRARY_API_TIMEOUT=10
```

### 3. Launch with Docker
```bash
# Development environment
docker-compose -f docker-compose.dev.yml up --build

# Production environment
docker-compose up --build
```

### 4. Access the Application
- **Web Interface**: http://localhost (production) or http://localhost:8080 (development)
- **Database**: localhost:5432 (development only)

## 📁 Project Structure

```
biblioteca-web/
├── app/                          # Main application package
│   ├── __init__.py              # Application factory and configuration
│   ├── controllers/             # Route handlers (MVC pattern)
│   │   ├── auth.py             # Authentication routes
│   │   ├── books.py            # Book management routes
│   │   └── routes.py           # Core application routes
│   ├── models/                  # Data models and forms
│   │   ├── modelsdb.py         # SQLAlchemy database models
│   │   ├── forms.py            # WTForms definitions
│   │   ├── book_search.py      # External API integration
│   │   └── code_book.py        # Book classification system
│   ├── security/               # Security utilities
│   │   ├── middleware.py       # Security headers and middleware
│   │   └── security.py         # Password validation and utilities
│   ├── utils/                  # Helper utilities
│   │   ├── helpers.py          # Form and UI helpers
│   │   ├── sanitize.py         # Input sanitization
│   │   └── notifications.py    # User notification formatting
│   ├── templates/              # Jinja2 templates
│   └── static/                 # CSS, JavaScript, images
├── tests/                      # Test suite
│   ├── conftest.py            # Test configuration
│   └── test_books.py          # Book functionality tests
├── data/                       # Sample data and imports
├── nginx/                      # Nginx configuration
├── scripts/                    # Utility scripts
├── docker-compose.yml          # Production Docker setup
├── docker-compose.dev.yml      # Development Docker setup
├── Dockerfile.dev             # Development container
├── requirements.txt           # Python dependencies
└── config.py                 # Application configuration
```

## 🛠️ Development Setup

### Local Development (without Docker)
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database (PostgreSQL required)
createdb biblioteca
export DATABASE_URL="postgresql://user:password@localhost:5432/biblioteca"

# Run application
python run.py
```

### Database Management
```bash
# Reset database (development)
./scripts/reset.sh

# Manual database access
docker exec -it biblioteca-web_db_1 psql -U postgres -d biblioteca
```

## 🧪 Testing

Run the test suite to ensure everything works correctly:

```bash
# Using Docker
docker-compose exec app python -m pytest tests/ -v

# Local environment
python -m pytest tests/ -v --cov=app
```

### Test Coverage
The project includes tests for:
- User authentication and registration
- Book creation and validation
- Database models and relationships
- API integrations
- Form validation

## 📊 Architecture Overview

### Database Schema
The application uses a relational database with the following key entities:

- **Users**: Authentication and profile management
- **Books**: Core book information with ISBN integration
- **UserBooks**: Many-to-many relationship for personal collections
- **UserReadings**: Reading progress tracking
- **Loans**: Book lending between users

### API Integration
- **Open Library API**: Automatic book metadata retrieval
- **Cover Image API**: Intelligent book cover detection
- **Fallback Mechanisms**: Amazon scraping as backup for cover images

### Security Features
- **Password Hashing**: Scrypt-based secure password storage
- **CSRF Protection**: Form-based attack prevention
- **Session Security**: Secure cookie configuration
- **Input Validation**: Comprehensive data sanitization

## 🔧 Configuration

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key for sessions | `dev-secret-key-fallback` |
| `DATABASE_URL` | PostgreSQL connection string | Development database |
| `FLASK_ENV` | Environment mode | `development` |
| `SESSION_COOKIE_SECURE` | Enable secure cookies | `False` (dev) |

### Application Settings
Key configuration options in `config.py`:
- Session timeout and security settings
- Database connection pooling
- Logging configuration
- CSRF and security headers

## 📈 Performance Optimization

### Caching Strategy
- **Flask-Caching**: Route-level caching for book collections
- **Database Indexing**: Optimized queries for search operations
- **Static File Serving**: Nginx for efficient asset delivery

### Database Optimization
- **Connection Pooling**: SQLAlchemy connection management
- **Query Optimization**: Eager loading for related entities
- **Pagination**: Efficient large dataset handling

## 🚀 Deployment

### Production Deployment
```bash
# Build production images
docker-compose build

# Deploy with environment variables
export SECRET_KEY="your-production-secret"
export DATABASE_URL="your-production-db-url"
docker-compose up -d
```

### Health Monitoring
- **Health Check Endpoint**: `/health` for load balancer monitoring
- **Logging**: Structured logging with rotation
- **Error Tracking**: Comprehensive error handling and logging

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for detailed information.

**Quick Start for Contributors:**

1. **Fork the repository** and create a feature branch
2. **Read our [Code of Conduct](CODE_OF_CONDUCT.md)**
3. **Follow code style** guidelines (PEP 8 for Python)
4. **Write tests** for new functionality
5. **Update documentation** for significant changes
6. **Submit a pull request** using our [PR template](.github/pull_request_template.md)

### 📋 Issue Templates
- [🐛 Bug Report](.github/ISSUE_TEMPLATE/bug_report.md)
- [✨ Feature Request](.github/ISSUE_TEMPLATE/feature_request.md)
- [❓ Question](.github/ISSUE_TEMPLATE/question.md)

### Code Style
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Follow Flask best practices and patterns
- Maintain test coverage above 80%

## 📝 API Documentation

### Book Management Endpoints
```http
GET    /your_collection          # List user's books
POST   /register_new_book        # Add new book
GET    /search                   # Search books
POST   /delete_book/<id>         # Remove book
```

### Authentication Endpoints
```http
POST   /register                 # User registration
POST   /login                    # User login
GET    /logout                   # User logout
```

## 🐛 Troubleshooting

### Common Issues

**Database Connection Issues**
```bash
# Check database status
docker-compose ps db
docker-compose logs db

# Reset database
./scripts/reset.sh
```

**Nginx 502 Errors**
```bash
# Check application logs
docker-compose logs app

# Restart services
docker-compose restart
```

**Book Metadata Not Loading**
- Verify internet connection for Open Library API
- Check API rate limits
- Review application logs for API errors

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🔒 Security

Please see our [Security Policy](SECURITY.md) for reporting security vulnerabilities.

## 📋 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed list of changes and version history.

## 👩‍💻 Author

**Larissa Ember**
- GitHub: [@lari-ember](https://github.com/lari-ember)
- Project Link: [biblioteca-web](https://github.com/lari-ember/biblioteca-web)

## 🙏 Acknowledgments

- [Open Library](https://openlibrary.org/) for book metadata API
- [Flask](https://flask.palletsprojects.com/) community for excellent documentation
- All contributors who have helped improve this project

## 📚 Additional Resources

- [Contributing Guidelines](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security Policy](SECURITY.md)
- [Changelog](CHANGELOG.md)
- [Project Structure Guide](docs/PROJECT_STRUCTURE.md)
- [Milestone Planning](docs/MILESTONES.md)
- [Full Release Milestone Template](docs/FULL_RELEASE_MILESTONE_TEMPLATE.md)

---

⭐ If you find this project useful, please consider giving it a star on GitHub!