# 📋 Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Repository organization with contributing guidelines
- Issue templates for bugs, features, and questions
- Pull request template
- Code of Conduct (bilingual - Portuguese/English)
- Security policy and reporting guidelines
- Comprehensive CONTRIBUTING.md guide

### Changed
- Improved repository structure and documentation

### Security
- Added security policy for responsible disclosure
- Enhanced security practices documentation

## [0.1.0] - 2024-12-XX

### Added
- Initial Flask application structure
- User authentication system
- Book management functionality
- Open Library API integration
- Docker containerization
- PostgreSQL database setup
- Basic CI/CD pipeline with GitHub Actions
- Book search and filtering capabilities
- User reading progress tracking
- Book lending system between users

### Features
- **User Management**
  - User registration and login
  - Password hashing with Scrypt
  - Session management
  - User profiles

- **Book Management**
  - Add books manually or via ISBN lookup
  - Automatic metadata retrieval from Open Library
  - Book cover image fetching
  - Dewey-inspired classification system
  - Reading progress tracking

- **Search & Discovery**
  - Advanced search with multiple filters
  - Search by title, author, genre, year
  - Book recommendations

- **Library Features**
  - Personal book collections
  - Book lending between users
  - Reading statistics and analytics
  - Book status tracking (read, reading, to-read)

### Technical
- Flask web framework
- SQLAlchemy ORM with PostgreSQL
- Flask-Login for authentication
- Responsive web design
- Docker support with docker-compose
- Automated testing with pytest
- Code quality tools (Black, isort, flake8, Bandit)
- CI/CD pipeline with GitHub Actions

### Security
- CSRF protection
- Secure session handling
- Password hashing
- Input validation and sanitization
- Security headers configuration

---

## Legend / Legenda

- 🚀 **Added / Adicionado**: New features
- 🔄 **Changed / Alterado**: Changes in existing functionality
- 🗑️ **Deprecated / Descontinuado**: Soon-to-be removed features
- ❌ **Removed / Removido**: Removed features
- 🐛 **Fixed / Corrigido**: Bug fixes
- 🔒 **Security / Segurança**: Security improvements