#!/bin/bash

# 🎯 Biblioteca Web - Milestone Creation Script
# This script creates the recommended GitHub milestones for the project

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    print_error "GitHub CLI (gh) is not installed. Please install it first:"
    echo "  - macOS: brew install gh"
    echo "  - Ubuntu/Debian: sudo apt install gh"
    echo "  - Windows: Download from https://cli.github.com/"
    exit 1
fi

# Check if user is authenticated
if ! gh auth status &> /dev/null; then
    print_error "Not authenticated with GitHub CLI. Please run: gh auth login"
    exit 1
fi

print_status "Creating GitHub milestones for Biblioteca Web..."

# Create Full Release Milestone
print_status "Creating v1.0.0 - Full Release milestone..."

FULL_RELEASE_DESC="🚀 Complete library management system with all core and bonus features, polished UI/UX, and comprehensive documentation

🎯 **Core Features:** Complete user authentication, full book management, API integration, advanced search, reading tracking, lending system, personal collections, user profiles, notifications, data import/export

🌟 **Bonus Features:** Recommendation algorithm, social features, analytics dashboard, PWA capabilities, offline support, wishlists, AI-powered search, third-party integrations, i18n, themes

📚 **Documentation:** API docs, user manual, admin guides, developer docs, contributing guidelines, deployment docs, security practices, troubleshooting, schema docs, testing docs

🎨 **UI/UX Polish:** Modern design, responsive layout, accessibility compliance, performance optimization, error handling, animations, keyboard navigation, loading states, professional branding

🔒 **Security & Performance:** Security audit, performance benchmarking, query optimization, caching, security headers, validation, rate limiting, backup procedures, monitoring, privacy compliance"

if gh api repos/:owner/:repo/milestones \
  --method POST \
  --field title="v1.0.0 - Full Release" \
  --field description="$FULL_RELEASE_DESC" \
  --field due_on="2025-06-30T23:59:59Z" \
  --field state="open" &> /dev/null; then
    print_success "Created v1.0.0 - Full Release milestone"
else
    print_warning "v1.0.0 - Full Release milestone may already exist or creation failed"
fi

# Create Beta Release Milestone
print_status "Creating v0.9.0 - Beta Release milestone..."

BETA_RELEASE_DESC="🔄 Feature-complete beta for testing and feedback

Key features include all core functionality, basic testing coverage, user feedback integration, bug fixes and stability improvements, and deployment documentation."

if gh api repos/:owner/:repo/milestones \
  --method POST \
  --field title="v0.9.0 - Beta Release" \
  --field description="$BETA_RELEASE_DESC" \
  --field due_on="2025-03-31T23:59:59Z" \
  --field state="open" &> /dev/null; then
    print_success "Created v0.9.0 - Beta Release milestone"
else
    print_warning "v0.9.0 - Beta Release milestone may already exist or creation failed"
fi

# Create Infrastructure & DevOps Milestone
print_status "Creating Infrastructure & DevOps milestone..."

INFRA_DESC="🏗️ Development infrastructure and deployment improvements

Ongoing improvements to CI/CD pipeline, Docker environment, automated testing, security scanning, performance monitoring, and backup strategies."

if gh api repos/:owner/:repo/milestones \
  --method POST \
  --field title="Infrastructure & DevOps" \
  --field description="$INFRA_DESC" \
  --field state="open" &> /dev/null; then
    print_success "Created Infrastructure & DevOps milestone"
else
    print_warning "Infrastructure & DevOps milestone may already exist or creation failed"
fi

# Create Documentation & UX Milestone
print_status "Creating Documentation & UX milestone..."

DOCS_UX_DESC="📚 Documentation improvements and user experience enhancements

Ongoing work on API documentation, user guides, developer documentation, UI/UX improvements, accessibility enhancements, and internationalization."

if gh api repos/:owner/:repo/milestones \
  --method POST \
  --field title="Documentation & UX" \
  --field description="$DOCS_UX_DESC" \
  --field state="open" &> /dev/null; then
    print_success "Created Documentation & UX milestone"
else
    print_warning "Documentation & UX milestone may already exist or creation failed"
fi

# Create Technical Debt & Refactoring Milestone
print_status "Creating Technical Debt & Refactoring milestone..."

TECH_DEBT_DESC="🔧 Code quality improvements and technical debt reduction

Ongoing work on code refactoring, performance optimizations, database optimization, security improvements, code coverage improvements, and dependency updates."

if gh api repos/:owner/:repo/milestones \
  --method POST \
  --field title="Technical Debt & Refactoring" \
  --field description="$TECH_DEBT_DESC" \
  --field state="open" &> /dev/null; then
    print_success "Created Technical Debt & Refactoring milestone"
else
    print_warning "Technical Debt & Refactoring milestone may already exist or creation failed"
fi

# Create Advanced Features Milestone
print_status "Creating Advanced Features milestone..."

ADVANCED_DESC="🌟 Advanced features and integrations

Future enhancements including book recommendations system, social features, advanced analytics, mobile app consideration, third-party integrations, and advanced search algorithms."

if gh api repos/:owner/:repo/milestones \
  --method POST \
  --field title="Advanced Features" \
  --field description="$ADVANCED_DESC" \
  --field due_on="2025-09-30T23:59:59Z" \
  --field state="open" &> /dev/null; then
    print_success "Created Advanced Features milestone"
else
    print_warning "Advanced Features milestone may already exist or creation failed"
fi

print_success "Milestone creation process completed!"
print_status "You can view the milestones at: https://github.com/$(gh repo view --json owner,name -q '.owner.login + \"/\" + .name')/milestones"

echo ""
print_status "Next steps:"
echo "  1. Review the created milestones on GitHub"
echo "  2. Assign existing issues to appropriate milestones"
echo "  3. Create new issues for missing features"
echo "  4. Set up milestone progress tracking"
echo "  5. Plan sprint cycles around milestone deadlines"