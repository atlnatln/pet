# ==============================================================================
# 🐾 Evcil Hayvan Platformu - Development Makefile
# ==============================================================================
# Common development tasks automation
# ==============================================================================

.PHONY: help install dev-install test lint format clean docker-build docker-up

# Default target
help:
	@echo "🐾 Evcil Hayvan Platformu - Development Commands"
	@echo "=================================================="
	@echo ""
	@echo "📦 INSTALLATION:"
	@echo "  install      Install production dependencies"
	@echo "  dev-install  Install development dependencies"
	@echo ""
	@echo "🧪 TESTING & QUALITY:"
	@echo "  test         Run all tests"
	@echo "  test-cov     Run tests with coverage"
	@echo "  lint         Run linting checks"
	@echo "  format       Format code with black and isort"
	@echo "  check        Run all quality checks"
	@echo ""
	@echo "🗄️ DATABASE:"
	@echo "  migrate      Run Django migrations"
	@echo "  makemigrations Create new migrations"
	@echo "  superuser    Create Django superuser"
	@echo ""
	@echo "🐳 DOCKER:"
	@echo "  docker-build Build Docker images"
	@echo "  docker-up    Start development environment"
	@echo "  docker-down  Stop development environment"
	@echo ""
	@echo "🧹 MAINTENANCE:"
	@echo "  clean        Clean cache and temporary files"
	@echo "  reset-db     Reset database (DANGER!)"
	@echo ""

# ==============================================================================
# 📦 INSTALLATION
# ==============================================================================
install:
	@echo "📦 Installing production dependencies..."
	pip install -r requirements.txt

dev-install:
	@echo "📦 Installing development dependencies..."
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install
	@echo "✅ Development environment ready!"

# ==============================================================================
# 🧪 TESTING & QUALITY
# ==============================================================================
test:
	@echo "🧪 Running tests..."
	python manage.py test

test-cov:
	@echo "🧪 Running tests with coverage..."
	coverage run --source='.' manage.py test
	coverage report
	coverage html

lint:
	@echo "🔍 Running linting checks..."
	flake8 .
	mypy .
	bandit -r . -x tests,venv

format:
	@echo "🎨 Formatting code..."
	black .
	isort .

check: lint test
	@echo "✅ All quality checks passed!"

# ==============================================================================
# 🗄️ DATABASE
# ==============================================================================
migrate:
	@echo "🗄️ Running migrations..."
	python manage.py migrate

makemigrations:
	@echo "🗄️ Creating migrations..."
	python manage.py makemigrations

superuser:
	@echo "👤 Creating superuser..."
	python manage.py createsuperuser

# ==============================================================================
# 🚀 DEVELOPMENT
# ==============================================================================
runserver:
	@echo "🚀 Starting development server..."
	python manage.py runserver

shell:
	@echo "🐍 Starting Django shell..."
	python manage.py shell

# ==============================================================================
# 🐳 DOCKER
# ==============================================================================
docker-build:
	@echo "🐳 Building Docker images..."
	docker-compose build

docker-up:
	@echo "🐳 Starting development environment..."
	docker-compose up -d
	@echo "🌐 Application: http://localhost:8000"
	@echo "🗄️ Database: localhost:5432"
	@echo "🔴 Redis: localhost:6379"
	@echo "📊 Flower: http://localhost:5555"

docker-down:
	@echo "🐳 Stopping development environment..."
	docker-compose down

docker-logs:
	@echo "📋 Following Docker logs..."
	docker-compose logs -f

# ==============================================================================
# 🧹 MAINTENANCE
# ==============================================================================
clean:
	@echo "🧹 Cleaning cache and temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .tox/
	@echo "✅ Cleanup completed!"

reset-db:
	@echo "⚠️  DANGER: This will delete all data!"
	@read -p "Are you sure? Type 'yes' to continue: " confirm && [ "$$confirm" = "yes" ]
	rm -f db.sqlite3
	python manage.py migrate
	@echo "🗄️ Database reset completed!"

# ==============================================================================
# 📊 MONITORING
# ==============================================================================
coverage-report:
	@echo "📊 Generating coverage report..."
	coverage html
	@echo "📊 Coverage report available at: htmlcov/index.html"

security-check:
	@echo "🛡️ Running security checks..."
	bandit -r . -f json -o security-report.json
	@echo "🛡️ Security report generated: security-report.json"

# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================
welcome:
	@echo ""
	@echo "🐾 ==============================================="
	@echo "   Evcil Hayvan Platformu Development"
	@echo "==============================================="
	@echo ""
	@echo "💝 Platform development environment hazır!"
	@echo "🚀 Development başlatmak için: make docker-up"
	@echo "🧪 Test çalıştırmak için: make test"
	@echo "🎨 Kod formatlamak için: make format"
	@echo ""
	@echo "📚 Daha fazla komut için: make help"
	@echo ""
	@echo "🐾 Her commit, bir hayvan hayatı için! 💝"
	@echo ""
