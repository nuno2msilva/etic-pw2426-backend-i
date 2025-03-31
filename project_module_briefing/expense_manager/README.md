# Expense Manager

## A simple yet powerful personal finance tracking application built with Django. Track expenses and income, categorize transactions, and gain insights into your spending habits.

### Features

- Track your expenses and income with detailed information
- Categorize transactions for better organization
- View spending summaries by category
- Sort and filter transaction history
- Multi-user support

## Setup Options

### Option 1: VS Code + Docker (Recommended)

This is the recommended approach as it provides a consistent development environment.

#### Requirements:
- Visual Studio Code
- Docker and Docker Compose
- VS Code Extensions:
  - Docker
  - Remote - Containers

#### Setup Steps:

1. Clone the repository:
```
git clone https://github.com/nuno2msilva/etic-pw2426-backend-i/
cd etic-pw2426-backend-i/project_module_briefing/expense_manager/
```

2. Open the project in VS Code:
```
code .
```

3. Reopen the project in a container:
   - Click on the green button in the bottom-left corner of VS Code
   - Select "Reopen in Container"

4. Run the engine command:
```
make plugandplay
```

5. If it doesn't open a page automatically, visit localhost:8000 in your browser.


### Option 2: Manual Setup (without Docker)

#### Requirements:
- Python 3.8+
- Poetry (dependency management)

#### Setup Steps:

1. Clone the repository:
```
git clone https://github.com/nuno2msilva/etic-pw2426-backend-i/
cd etic-pw2426-backend-i/project_module_briefing/expense_manager/
```

2. Run the automated engine:
```
make plugandplay
```

3. If it doesn't open a page automatically, visit localhost:8000 in your browser.

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
