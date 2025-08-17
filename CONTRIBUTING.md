# 🤝 Contributing to Biblioteca Web / Contribuindo para a Biblioteca Web

*[English](#english) | [Português](#português)*

---

## English

Thank you for your interest in contributing to Biblioteca Web! This document provides guidelines and instructions for contributing to our personal library management system.

### 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Code Quality](#code-quality)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
- [Community Guidelines](#community-guidelines)

### 📜 Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

### 🚀 Getting Started

1. **Fork the Repository**
   ```bash
   # Click the "Fork" button on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/biblioteca-web.git
   cd biblioteca-web
   ```

2. **Set Up Remote**
   ```bash
   git remote add upstream https://github.com/lari-ember/biblioteca-web.git
   git remote -v
   ```

### 🔧 Development Setup

#### Prerequisites
- Python 3.10+
- Docker and Docker Compose
- Git

#### Local Development
```bash
# Clone the repository
git clone https://github.com/lari-ember/biblioteca-web.git
cd biblioteca-web

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

#### Docker Development
```bash
# Build and start services
docker-compose -f docker-compose.dev.yml up --build

# The application will be available at http://localhost:5000
```

#### Database Setup
```bash
# Using Docker (recommended)
docker-compose -f docker-compose.dev.yml up postgres

# Local PostgreSQL
createdb biblioteca_dev
export DATABASE_URL="postgresql://username:password@localhost:5432/biblioteca_dev"
```

### 🔄 Making Changes

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Make Your Changes**
   - Follow the project structure in [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)
   - Write clean, readable code
   - Add tests for new functionality
   - Update documentation as needed

3. **Keep Your Branch Updated**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

### 🧪 Testing

#### Running Tests
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app --cov-report=html

# Run specific test file
pytest tests/test_books.py -v

# Run tests in Docker
docker-compose exec app pytest tests/ -v
```

#### Writing Tests
- Place tests in the `tests/` directory
- Use pytest for new tests
- Follow existing test patterns
- Aim for 80%+ code coverage
- Test both positive and negative cases

#### Test Structure
```python
# tests/test_example.py
import pytest
from app import create_app

def test_example_functionality():
    """Test description of what is being tested."""
    # Arrange
    # Act
    # Assert
    assert True
```

### 🎯 Code Quality

#### Code Style
- **Python**: Follow PEP 8 guidelines
- **Line Length**: Maximum 88 characters (Black default)
- **Imports**: Use isort for import sorting
- **Documentation**: Write clear docstrings

#### Tools
```bash
# Format code with Black
black app/

# Sort imports with isort
isort app/

# Lint with flake8
flake8 app/ --max-line-length=88 --extend-ignore=E203,W503

# Security check with bandit
bandit -r app/ -ll

# Type checking with mypy
mypy app/
```

#### Pre-commit Hooks
```bash
# Install pre-commit hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

### 📝 Commit Message Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/) specification:

#### Format
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### Types
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect code meaning
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools

#### Examples
```bash
feat(books): add book lending functionality
fix(auth): resolve session timeout issue
docs: update API documentation
test(books): add unit tests for book validation
```

### 🔄 Pull Request Process

1. **Before Submitting**
   - [ ] Tests pass locally
   - [ ] Code is properly formatted
   - [ ] Documentation is updated
   - [ ] Commit messages follow conventions

2. **Creating the PR**
   - Use our [PR template](.github/pull_request_template.md)
   - Link to related issues
   - Provide clear description of changes
   - Add screenshots for UI changes

3. **Review Process**
   - Maintain professional and respectful communication
   - Address reviewer feedback promptly
   - Keep the PR up to date with the main branch

4. **After Approval**
   - Squash commits if requested
   - Ensure CI/CD passes
   - Wait for maintainer to merge

### 🌟 Community Guidelines

#### Communication
- Be respectful and inclusive
- Use clear, concise language
- Provide constructive feedback
- Ask questions when in doubt

#### Reporting Issues
- Use our [issue templates](.github/ISSUE_TEMPLATE/)
- Provide reproduction steps
- Include environment details
- Search existing issues first

#### Getting Help
- Check existing documentation
- Search closed issues and PRs
- Ask questions in discussions
- Tag maintainers if necessary

---

## Português

Obrigado pelo seu interesse em contribuir para a Biblioteca Web! Este documento fornece diretrizes e instruções para contribuir com nosso sistema de gerenciamento de biblioteca pessoal.

### 📋 Índice

- [Código de Conduta](#código-de-conduta)
- [Primeiros Passos](#primeiros-passos)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Fazendo Mudanças](#fazendo-mudanças)
- [Testes](#testes)
- [Qualidade do Código](#qualidade-do-código)
- [Diretrizes de Mensagem de Commit](#diretrizes-de-mensagem-de-commit)
- [Processo de Pull Request](#processo-de-pull-request)
- [Diretrizes da Comunidade](#diretrizes-da-comunidade)

### 📜 Código de Conduta

Este projeto e todos os participantes são regidos pelo nosso [Código de Conduta](CODE_OF_CONDUCT.md). Ao participar, espera-se que você mantenha este código.

### 🚀 Primeiros Passos

1. **Faça um Fork do Repositório**
   ```bash
   # Clique no botão "Fork" no GitHub, então clone seu fork
   git clone https://github.com/SEU_USUARIO/biblioteca-web.git
   cd biblioteca-web
   ```

2. **Configure o Remote**
   ```bash
   git remote add upstream https://github.com/lari-ember/biblioteca-web.git
   git remote -v
   ```

### 🔧 Configuração do Ambiente

#### Pré-requisitos
- Python 3.10+
- Docker e Docker Compose
- Git

#### Desenvolvimento Local
```bash
# Clone o repositório
git clone https://github.com/lari-ember/biblioteca-web.git
cd biblioteca-web

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com sua configuração
```

#### Desenvolvimento com Docker
```bash
# Construa e inicie os serviços
docker-compose -f docker-compose.dev.yml up --build

# A aplicação estará disponível em http://localhost:5000
```

### 🔄 Fazendo Mudanças

1. **Crie uma Branch de Feature**
   ```bash
   git checkout -b feature/nome-da-sua-feature
   # ou
   git checkout -b fix/seu-bug-fix
   ```

2. **Faça Suas Mudanças**
   - Siga a estrutura do projeto em [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)
   - Escreva código limpo e legível
   - Adicione testes para nova funcionalidade
   - Atualize a documentação conforme necessário

### 🧪 Testes

#### Executando Testes
```bash
# Execute todos os testes
pytest tests/ -v

# Execute com cobertura
pytest tests/ -v --cov=app --cov-report=html

# Execute arquivo de teste específico
pytest tests/test_books.py -v

# Execute testes no Docker
docker-compose exec app pytest tests/ -v
```

### 📝 Diretrizes de Mensagem de Commit

Seguimos a especificação [Conventional Commits](https://www.conventionalcommits.org/):

#### Formato
```
<tipo>[escopo opcional]: <descrição>

[corpo opcional]

[rodapé(s) opcional(is)]
```

#### Tipos
- `feat`: Uma nova funcionalidade
- `fix`: Correção de bug
- `docs`: Apenas mudanças na documentação
- `style`: Mudanças que não afetam o significado do código
- `refactor`: Mudança de código que não corrige bug nem adiciona feature
- `perf`: Mudança de código que melhora performance
- `test`: Adição de testes faltantes ou correção de testes existentes
- `chore`: Mudanças no processo de build ou ferramentas auxiliares

### 🔄 Processo de Pull Request

1. **Antes de Submeter**
   - [ ] Testes passam localmente
   - [ ] Código está adequadamente formatado
   - [ ] Documentação está atualizada
   - [ ] Mensagens de commit seguem convenções

2. **Criando o PR**
   - Use nosso [template de PR](.github/pull_request_template.md)
   - Linke para issues relacionadas
   - Forneça descrição clara das mudanças
   - Adicione screenshots para mudanças de UI

---

**Obrigado por contribuir com a Biblioteca Web! 🙏**

For questions or support, please open an issue or contact the maintainers.
Para perguntas ou suporte, abra uma issue ou entre em contato com os mantenedores.