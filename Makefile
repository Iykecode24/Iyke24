.PHONY: help dev up down build logs migrate test clean

# ============================================================
# IYKE CONTENT STUDIO — Makefile
# ============================================================

help: ## Show available commands
	@echo "IYKE CONTENT STUDIO - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ── Docker Commands ──

up: ## Start all services
	docker compose up -d

down: ## Stop all services
	docker compose down

build: ## Build all Docker images
	docker compose build

logs: ## View all service logs
	docker compose logs -f

logs-backend: ## View backend logs
	docker compose logs -f backend

logs-frontend: ## View frontend logs
	docker compose logs -f frontend

logs-worker: ## View Celery worker logs
	docker compose logs -f celery-worker

restart: ## Restart all services
	docker compose restart

clean: ## Stop and remove all containers, volumes
	docker compose down -v --remove-orphans

# ── Database Commands ──

migrate: ## Run database migrations
	docker compose exec backend alembic upgrade head

migration: ## Create a new migration (usage: make migration msg="description")
	docker compose exec backend alembic revision --autogenerate -m "$(msg)"

migrate-down: ## Rollback last migration
	docker compose exec backend alembic downgrade -1

db-shell: ## Open PostgreSQL shell
	docker compose exec postgres psql -U iyke -d iyke_studio

# ── Backend Commands ──

backend-shell: ## Open backend shell
	docker compose exec backend bash

backend-test: ## Run backend tests
	docker compose exec backend pytest tests/ -v --tb=short

backend-lint: ## Lint backend code
	docker compose exec backend python -m ruff check app/

# ── Frontend Commands ──

frontend-shell: ## Open frontend shell
	docker compose exec frontend sh

frontend-test: ## Run frontend tests
	docker compose exec frontend npm test

frontend-build: ## Build frontend for production
	docker compose exec frontend npm run build

# ── Development ──

dev-backend: ## Run backend locally (without Docker)
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Run frontend locally (without Docker)
	cd frontend && npm run dev

dev-worker: ## Run Celery worker locally
	cd backend && celery -A app.workers.celery_app worker --loglevel=info

# ── Setup ──

setup: ## Initial project setup
	cp -n .env.example .env || true
	docker compose up -d postgres redis
	@echo "Waiting for database..."
	@sleep 5
	docker compose up -d backend
	@sleep 3
	docker compose exec backend alembic upgrade head
	docker compose up -d
	@echo ""
	@echo "✅ Iyke Content Studio is running!"
	@echo "   Frontend: http://localhost:3000"
	@echo "   API:      http://localhost:8000"
	@echo "   API Docs: http://localhost:8000/docs"
