# ===========================================
# Expense Manager - Development Commands
# ===========================================

# === Setup Commands ===

# Initialize the project with all dependencies
init:
	poetry add django uvicorn psycopg2-binary whitenoise pytest pytest-django
	poetry install
	@echo "Dependencies installed. Create a .env file before continuing."

# Quick Start First Time Setup
setup:
	@echo "Setting up Expense Manager..."
	@if [ ! -f .env ]; then \
		echo "Creating example .env file..."; \
		echo "DEBUG=True" > .env; \
		echo "SECRET_KEY=your-secret-key-here" >> .env; \
		echo "POSTGRES_USERNAME=postgres" >> .env; \
		echo "POSTGRES_PASSWORD=qwerty" >> .env; \
		echo "POSTGRES_HOST=database" >> .env; \
		echo "POSTGRES_PORT=5432" >> .env; \
		echo "POSTGRES_DATABASE=dj_db" >> .env; \
		echo "Please edit the .env file with your settings"; \
	fi
	poetry install
	poetry run python manage.py migrate
	docker compose build
	make migrate
	@echo "Setup complete! Run 'make run' to start the application."

# === Database Commands ===
migrations:
	docker compose run --rm web poetry run python manage.py makemigrations

migrate:
	docker compose run --rm web poetry run python manage.py migrate

# Resets Database
resetdb:
	docker compose down
	docker volume rm expense_manager_postgres_data || true
	docker compose up -d db
	sleep 3  # Wait for database to initialize
	make migrate

# Creates a Super User
superuser:
	docker compose run web poetry run python manage.py createsuperuser

# === Running the Application ===

# First time setup with build
first:
	docker compose up --build

# Rebuild containers (use when Dockerfile or requirements change)
build:
	docker compose up --build --force-recreate

# Run the application
run:
	docker compose up

# Run in detached mode (background)
run-detached:
	docker compose up -d

# Stop the application
stop:
	docker compose down

# === Development Tools ===

# Collect static files
static:
	docker compose exec web poetry run python manage.py collectstatic --noinput

# Run tests
devsetup:
	poetry add --dev pytest pytest-django

test:
	poetry run pytest -vvv
