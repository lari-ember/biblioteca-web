# 📁 Project Structure - Biblioteca Web

This document explains the organization and structure of the Biblioteca Web project.

## 🏗️ Directory Structure

```
biblioteca-web/
├── .github/                    # GitHub-specific files
│   ├── ISSUE_TEMPLATE/        # Issue templates
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── question.md
│   ├── workflows/             # GitHub Actions workflows
│   │   └── main.yml
│   └── pull_request_template.md
├── app/                       # Flask application code
│   ├── __init__.py           # App factory and configuration
│   ├── models/               # Database models
│   ├── routes/               # Route handlers
│   ├── templates/            # Jinja2 templates
│   ├── static/               # Static files (CSS, JS, images)
│   └── utils/                # Utility functions
├── config/                   # Configuration files
├── data/                     # Data files and samples
├── docs/                     # Documentation
│   └── MILESTONES.md
├── nginx/                    # Nginx configuration
├── scripts/                  # Utility scripts
├── tests/                    # Test files
├── .dockerignore            # Docker ignore file
├── .gitignore               # Git ignore file
├── .pre-commit-config.yaml  # Pre-commit hooks
├── CHANGELOG.md             # Project changelog
├── CODE_OF_CONDUCT.md       # Community guidelines
├── CONTRIBUTING.md          # Contribution guidelines
├── Dockerfile.dev           # Development Docker configuration
├── LICENSE                  # MIT license
├── README.md                # Project documentation
├── SECURITY.md              # Security policy
├── config.py                # Flask configuration
├── docker-compose.dev.yml   # Docker Compose for development
├── pyproject.toml           # Python project configuration
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
└── run.py                   # Application entry point
```

## 📂 Core Directories

### `/app` - Flask Application
- **`__init__.py`**: Application factory and initialization
- **`models/`**: SQLAlchemy database models
- **`routes/`**: Flask route handlers and views
- **`templates/`**: HTML templates using Jinja2
- **`static/`**: CSS, JavaScript, images, and other static assets
- **`utils/`**: Helper functions and utilities

### `/tests` - Testing
- Test files following pytest conventions
- Includes unit tests, integration tests, and fixtures
- Configuration in `pyproject.toml`

### `/config` - Configuration
- Environment-specific configuration files
- Database configuration
- Application settings

### `/docs` - Documentation
- Project documentation
- API documentation
- Guides and tutorials

### `/.github` - GitHub Integration
- Issue and pull request templates
- GitHub Actions workflows
- Community files

## 📋 Key Files

### Root Level Files
- **`README.md`**: Main project documentation
- **`CONTRIBUTING.md`**: Guidelines for contributors
- **`CODE_OF_CONDUCT.md`**: Community standards
- **`SECURITY.md`**: Security reporting and policies
- **`CHANGELOG.md`**: Version history and changes
- **`LICENSE`**: MIT license terms

### Configuration Files
- **`config.py`**: Flask application configuration
- **`pyproject.toml`**: Python project metadata and tool configuration
- **`requirements.txt`**: Production Python dependencies
- **`requirements-dev.txt`**: Development Python dependencies
- **`.pre-commit-config.yaml`**: Pre-commit hooks configuration

### Docker Files
- **`Dockerfile.dev`**: Development Docker image
- **`docker-compose.dev.yml`**: Development environment setup
- **`.dockerignore`**: Files to ignore in Docker builds

## 🔧 Development Workflow

### 1. Setup
```bash
git clone https://github.com/lari-ember/biblioteca-web.git
cd biblioteca-web
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Development
```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up

# Run tests
pytest tests/ -v

# Code quality checks
black app/
isort app/
flake8 app/
```

### 3. Contribution
- Follow [CONTRIBUTING.md](../CONTRIBUTING.md) guidelines
- Use issue templates for bugs and features
- Follow pull request template
- Ensure tests pass and code quality checks pass

## 📊 File Organization Principles

### 🎯 Separation of Concerns
- **Models**: Database structure and business logic
- **Routes**: HTTP request handling
- **Templates**: User interface
- **Static**: Client-side assets
- **Utils**: Shared functionality

### 📏 Naming Conventions
- **Files**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions**: `snake_case()`
- **Constants**: `UPPER_SNAKE_CASE`
- **Templates**: `snake_case.html`

### 📦 Import Organization
```python
# Standard library imports
import os
import sys

# Third-party imports
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# Local application imports
from app.models import User, Book
from app.utils import helper_function
```

## 🔒 Security Considerations

### 📁 Sensitive Files
- Environment variables in `.env` (not committed)
- Secret keys and passwords
- API keys and tokens
- Database credentials

### 🛡️ File Permissions
- Configuration files should be readable only by application
- Log files should have appropriate permissions
- Static files can be publicly accessible

## 📈 Scaling Considerations

### 📂 Future Structure
As the project grows, consider:
- Splitting models into separate files
- Organizing routes by feature (blueprints)
- Adding dedicated API module
- Implementing caching layer
- Adding background job processing

### 🔄 Maintainability
- Keep files focused and single-purpose
- Use consistent naming conventions
- Document complex logic
- Maintain test coverage
- Regular dependency updates

---

This structure promotes maintainability, scalability, and collaboration while following Flask and Python best practices.