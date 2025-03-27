This is a planning script for an upcoming project about making a python expense manager with, if possible, budgeting options.

Note: This is a draft and requires formatting, and consistency.

Common Data, sequentially: Type: String Dictionary (FILL, STANDALONE, BULK) ID: Sequential Float Unique TIMESTAMP: User input, Integral, YYYYMMDD LOCAL: String CATEGORY: String auto-dict ITEM: String VOLUME: Float (units or weight) COST: Float (€)

CLI Examples:

For fill: pretype: make; type: fill; id: (auto); timestamp: 20250320; local: Null; category: Null; Item: Wage; Volume: (always) 1; Cost: 300,01

make fill 2025 wage 300,01 (fill,1,20250302,,,wage,1,300.01)

For Standalone: pretype: make; type: standalone; id: (auto); timestamp: 20250321; local: coffeeshop; category: food; item: coffee; volume: 1; cost: 0,90

Make standalone 20250321 coffeeshop food coffee 1 0,90 (standalone,2,20250321,coffeeshop,food,coffee,1;0.90)

For Bulk:

pretype: make; type: bulk; id: (auto) + (ID p/ standalone, ex: 3.1, 3.2, 3.3…); timestamp: 20250322; local: walmart; category: custom standalone; item: custom standalone; volume: total standalone items; cost: total standalone cost

make bulk 20250322 wallmart make bulkalone bakery bread 3 0,60 make bulkalone food spaghetti 1 1,20 make bulkalone candy ‘sweet raspberries’ 1 0,99 make bulkalone end (bulk,3,20250322,wallmart,,,,) (bulkalone,3.1,,,bakery,bread,3,0.60) (bulkalone,3.2,,,food,spaghetti,1,1.20) (bulkalone,3.3,,,candy, sweet raspberries,1,0.99)

Example csv: TYPE,ID,TIMESTAMP,LOCAL,CATEGORY,ITEM,VOLUME,COST fill,1,20250302,,,wage,1,300.01 standalone,2,20250321,coffeeshop,food,coffee,1,0.90 bulk,3,20250322,wallmart,,,, bulkalone,3.1,,,bakery,bread,3,0.60 bulkalone,3.2,,,food,spaghetti,1,1.20 bulkalone,3.3,,,candy, sweet raspberries,1,0.99

Planning:

    Iniciate project
    Detect file, if doesnt exist, create CSV automatically on root
    Add fill and standalone
    Add bulk and bulkalone
    List transactions page by page
    Edit fill and standalone
    Edit bulk and bulkalone
    Delete fill and standalones
    Delete bulk and bulkalones
    Read Wallet (how much you have)
    (extension) List categories
    (extension) Filter categories and how much
    (extension) Define category limits (budgets)
    (extension) Monthly Analysis
    (optional) apply fuzzy text to avoid duplicate categories
    Makefiles and Dockerfiles

Tips: Maybe make a pretty client asking exactly what you want with a handholding approach for each part and filling the other ones automatically use “;” instead of “,” to separate values

Template Project Module Briefing

This final project spans four sessions and challenges you to develop a real-world application using one or more of the following Python solutions: a Command Line Interface (CLI) with Typer, an API with FastAPI, or a SaaS web application with Django. You may even combine frameworks (for instance, using FastAPI for REST endpoints and Typer for background job commands) to solve the problem more effectively. Below are the detailed requirements and evaluation criteria.

Project Objectives and Requirements

Real-World Problem Solving:
Your project must address a practical problem. For example:
    Personal Finance Manager: Manage income and expenses via a CLI or web interface.
    Task Manager: Organise, update, and track tasks using REST APIs and a web dashboard.
    Inventory System: Manage products and categories in a business context with full administrative features.

Choose an idea that is relevant and adds real value to users. Framework Implementation Requirements:

CLI using Typer:
    Commands: Implement at least 5 different commands (e.g. add, list, update, delete, summary).
        Options & Arguments: Each command must use options and arguments to handle user input effectively.

Example: A command to add an expense might require an amount, category, and optional notes.

API using FastAPI:
    Endpoints: Create one endpoint per major HTTP verb—GET, POST, PUT, PATCH, DELETE.
    OpenAPI Documentation: Each endpoint must be automatically documented on the OpenAPI (Swagger) page provided by FastAPI.

Example: A GET endpoint to retrieve tasks, a POST endpoint to create a new task, etc.

SaaS using Django:
    Models: Create at least 2 models (e.g. Product and Category, or Task and User).
    Form: Implement at least 1 form for user input (e.g. a contact or registration form).
    Views: Develop at least 4 views (function-based or class-based) to cover listing, detail, creation, and update operations.
    Admin: Set up the corresponding admin views to manage your models.

Example: A Django app for inventory could have ListView for products, DetailView for product details, CreateView for adding a new product, and UpdateView for editing existing products. Testing:

Implement tests using either pytest or unittest. Ensure that critical functionality (e.g. API endpoints, CLI commands, form validations) is covered.

Logging:

Integrate logging into your project to track operations and errors. Ensure that logs capture key actions and any exceptions that occur.

Database Integration:

The project must interact with a database (Postgres is recommended). Ensure that CRUD operations or data queries are performed via your chosen framework’s ORM or database connectivity tool.

Documentation:

Create a comprehensive README.md that describes the project, installation steps, and usage instructions.
The documentation should be clear enough so that another developer can set up and run your project without additional guidance.

Poetry:

Use Poetry to manage your dependencies and project configuration consistently.

Bonus – Docker and Docker Compose:

Although not mandatory, using Docker and Docker Compose is a plus. This will allow you to set up your development environment (including Postgres) in a containerised manner without needing to install these tools locally.
Include a Dockerfile and a docker-compose.yml file that orchestrates your application and database services.

Project Evaluation (Maximum 20 Points)

Documentation (3 points):
    The README.md must clearly describe the project, installation process, and usage instructions.

Poetry and Frameworks Requirements (5 points):
    Your project must use Poetry for dependency management and meet the specific framework requirements (e.g., 5 CLI commands with options for Typer, endpoints for FastAPI, or models, form, views, and admin for Django).

Tests (3 points):
    Include a comprehensive test suite covering core functionalities.

Logging (2 points):
    Implement logging that captures key operations and errors.

Database Integration (1 point):
    The project must interact with a database (preferably Postgres).

GIT Release (Tag) and Copy on Google Drive Module Folder (2 points):
    Ensure that you tag a release in your Git repository and provide a copy in the designated Google Drive folder.

Docker and Docker Compose (1 point):
    Using Docker and Docker Compose to containerise your solution is a plus.

Working Solution + Multiple Framework Implementation (3 points):
    A fully functioning project that may integrate more than one framework (e.g., a FastAPI API combined with Typer background jobs) will score higher.

Describing Examples

Typer Example:
    Create a CLI tool where the command expense add --amount 100 --category food --note "Lunch" adds an expense record. Include commands such as list, update, delete, and summary to manage expenses.

FastAPI Example:
    Build a RESTful API with endpoints:
        GET /tasks/ to retrieve all tasks.
        POST /tasks/ to create a task.
        PUT /tasks/{id} to update a task.
        PATCH /tasks/{id} for partial updates.
        DELETE /tasks/{id} to delete a task.
    All endpoints are automatically documented in FastAPI’s interactive docs.

Django Example:
    Develop a SaaS solution, such as an inventory management system, with models for Product and Category, a form for product input, views to list, detail, create, and update products, and an admin interface that allows for managing these models.

