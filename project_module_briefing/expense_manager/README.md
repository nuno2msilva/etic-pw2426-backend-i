# Expense Manager

## A simple yet powerful personal finance tracking application built with Django. Track expenses and income, categorize transactions, and gain insights into your spending habits.

### Features

- Track your expenses and income with detailed information;
- Categorize transactions for better organization;
- View spending summaries by category;
- Sort and filter transaction history;
- Multi-user support.

### Requirements

- Python 3.8+
- Poetry (dependency management)

### Dev Requirements

- Python 3.8+
- Poetry (dependency management)
- Docker and Docker Compose (optional)


## Quick Start with Makefile Commands

The project includes a Makefile with convenient commands that simplify common development tasks.

### Setting Up:

1. Clone the repository:
      ```
   git clone https://github.com/nuno2msilva/etic-pw2426-backend-i/
   cd etic-pw2426-backend-i/project_module_briefing/expense_manager/
    ```

2. Run the setup command:
   ```
   make setup
   ```
   
   This will:
   - Create a sample .env file (you should edit this with your settings)
   - Install dependencies with Poetry
   - Build Docker containers
   - Run initial migrations

3. Start the application:
   ```
   make run
   ```

4. Create a superuser (optional):
   ```
   make superuser
   ```

5. Visit http://localhost:8000 in your browser

## Running Tests (For Devs):

- Install Dev Dependencies:
    ```
    made devsetup
    ```


- Run all tests:
  ```
  make test
  ```

## Common Makefile Commands:

- **make run**            : Start the application
- **make stop**           : Stop the application 
- **make run-detached**   : Run in background mode
- **make migrations**     : Create new migrations
- **make migrate**        : Apply database migrations
- **make resetdb**        : Reset the database (dev only)
- **make superuser**      : Create a superuser account
- **make shell**          : Open a Django shell
- **make help**           : Show all available commands

## Manual Setup (without Docker):

1. Clone the repository:
      ```
   git clone https://github.com/nuno2msilva/etic-pw2426-backend-i/
   cd etic-pw2426-backend-i/project_module_briefing/expense_manager/
    ```

2. Install dependencies:
   ```
   pip install poetry
   poetry install
   ```

3. Create a .env file in the project root (Reccomended to edit to your preference):
   ```
   POSTGRES_USERNAME="postgres"
   POSTGRES_PASSWORD="qwerty"
   POSTGRES_HOST="database"
   POSTGRES_PORT="5432"
   POSTGRES_DATABASE="dj_db"
    ```

4. Apply migrations:
   ```
   poetry run python manage.py migrate
   ```

5. Run the development server:
   ```
   poetry run python manage.py runserver
   ```

6. Visit http://localhost:8000 in your browser

## Using the Application

1. Register a new account from the homepage
2. Log in with your credentials
3. Add new expenses or income entries using the form
4. View your transaction history in the table below
5. Use the sorting options to organize transactions by:
   - Date (newest/oldest)
   - Item name (A-Z/Z-A)
   - Category (A-Z/Z-A)
   - Cost (highest/lowest)
6. See spending summaries by category in the dashboard
7. Delete individual transactions as needed
8. Use the "purge" feature (red X icon) to delete all transactions at once (use with caution!)

## Project Structure
```
expense_manager/
├── app/                # Main application code
├── config/             # Django configuration
├── templates/          # HTML templates
├── static/             # Static files (CSS, JS)
├── tests/              # Test suite
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose setup
├── Makefile            # Development commands
├── pyproject.toml      # Poetry dependencies
└── README.md           # This file
```
