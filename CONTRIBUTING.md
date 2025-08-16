# 🤝 Contributing to Biblioteca Web

Thank you for your interest in contributing to Biblioteca Web! This document provides guidelines and information about contributing to this project.

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Process](#contributing-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)

## 📜 Code of Conduct
This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- Git
- PostgreSQL (for local development)

### Fork and Clone
1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/biblioteca-web.git
   cd biblioteca-web
   ```

## 💻 Development Setup

### 1. Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Database Setup
```bash
# Using Docker
docker-compose -f docker-compose.dev.yml up -d

# Or manually with PostgreSQL
createdb biblioteca_dev
```

### 3. Environment Variables
Create a `.env` file:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://username:password@localhost:5432/biblioteca_dev
FLASK_ENV=development
```

### 4. Run Tests
```bash
pytest tests/ -v --cov=app
```

## 🔄 Contributing Process

### 1. Choose an Issue
- Look for issues labeled `good first issue` for beginners
- Check if the issue is already assigned
- Comment on the issue to express interest

### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 3. Make Changes
- Follow our coding standards
- Write tests for new functionality
- Update documentation as needed

### 4. Test Your Changes
```bash
# Run tests
pytest tests/ -v

# Run linting
flake8 app/ --max-line-length=88
black --check app/
isort --check-only app/

# Run security check
bandit -r app/ -ll
```

## 🎨 Coding Standards

### Python Code Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use [Black](https://black.readthedocs.io/) for code formatting
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Maximum line length: 88 characters

### Code Quality
- Write meaningful variable and function names
- Add docstrings for functions and classes
- Follow Flask best practices
- Maintain test coverage above 80%

### Commit Messages
Use conventional commit format:
```
type(scope): description

Types: feat, fix, docs, style, refactor, test, chore
```

Examples:
- `feat(auth): add password reset functionality`
- `fix(books): resolve ISBN validation issue`
- `docs(readme): update installation instructions`

## 🧪 Testing

### Writing Tests
- Write tests for all new functionality
- Follow existing test patterns
- Use descriptive test names
- Test both positive and negative cases

### Test Structure
```python
def test_feature_description():
    """Test description explaining what is being tested."""
    # Arrange
    # Act
    # Assert
```

### Running Tests
```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_books.py -v

# With coverage
pytest tests/ --cov=app --cov-report=html
```

## 📚 Documentation

### Code Documentation
- Add docstrings to all functions and classes
- Use Google-style docstrings
- Update inline comments for complex logic

### API Documentation
- Document new API endpoints
- Include request/response examples
- Update OpenAPI specifications if applicable

### README Updates
- Update feature lists for new functionality
- Update installation/setup instructions
- Add new environment variables

## 📤 Submitting Changes

### 1. Push Changes
```bash
git add .
git commit -m "feat(feature): add new functionality"
git push origin feature/your-feature-name
```

### 2. Create Pull Request
- Use the provided PR template
- Include clear description of changes
- Link related issues
- Add screenshots for UI changes
- Ensure all checks pass

### 3. Code Review
- Address feedback promptly
- Make requested changes
- Update tests as needed
- Maintain discussion in PR comments

## 🏷️ Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements or additions to documentation
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed
- `question` - Further information is requested

## 📞 Getting Help

- Create a [Question issue](https://github.com/lari-ember/biblioteca-web/issues/new?template=question.md)
- Join discussions in existing issues
- Check the [README](README.md) for basic information

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- GitHub contributor list

Thank you for contributing to Biblioteca Web! 🙏

---

**Happy coding!** 🚀