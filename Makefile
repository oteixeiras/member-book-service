# Member Book Service - Makefile

.PHONY: help build up down logs shell migrate seed test clean

# Default target
help: ## Show this help message
	@echo "Member Book Service - Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Docker commands
build: ## Build the Docker image
	sudo docker compose build

up: ## Start the application
	sudo docker compose up -d

down: ## Stop the application
	sudo docker compose down

logs: ## Show application logs
	sudo docker compose logs -f app

logs-db: ## Show database logs
	sudo docker compose logs -f db

# Development commands
dev: ## Start in development mode with hot reload
	sudo docker compose up

shell: ## Open shell in the app container
	sudo docker compose exec app bash

shell-db: ## Open PostgreSQL shell
	sudo docker compose exec db psql -U postgres -d member_book_db

# Database commands
migrate: ## Run database migrations
	sudo docker compose exec app alembic upgrade head

migrate-create: ## Create a new migration (usage: make migrate-create MESSAGE="migration message")
	sudo docker compose exec app alembic revision --autogenerate -m "$(MESSAGE)"

seed: ## Populate database with seed data
	sudo docker compose exec app python -c "from app.seeds.profiles_seed import seed_profiles; from app.db.database import SessionLocal; db = SessionLocal(); seed_profiles(db); db.close()"

# Testing commands
test: ## Run tests
	sudo docker compose exec app python -m pytest

# Utility commands
clean: ## Clean up containers and volumes
	sudo docker compose down -v
	sudo docker system prune -f

restart: ## Restart the application
	sudo docker compose restart app

status: ## Show container status
	sudo docker compose ps

# API testing
test-api: ## Test the API endpoints
	@echo "Testing health endpoint..."
	curl -f http://localhost:8000/health || echo "Health check failed"
	@echo ""
	@echo "Testing populate data endpoint..."
	curl -X PUT http://localhost:8000/members-book-service/v1/members/populate-data || echo "Populate data failed"

# Full setup
setup: build up migrate seed ## Complete setup: build, start, migrate and seed
	@echo "✅ Setup complete! API available at http://localhost:8000"
	@echo "📚 Documentation: http://localhost:8000/docs"
