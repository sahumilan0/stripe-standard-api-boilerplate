# Stripe-Style-API-Boilerplate

This repository provides a boilerplate for building APIs using FastAPI, following standards similar to those adopted by Stripe and other companies known for their excellent API designs. The structure and implementation in this boilerplate emphasize modularity, scalability, and adherence to best practices.
I am creating this boilerplate to share how to think about API design and how to implement it in a way that is easy to understand and maintain and set a new standard of boilerplate for API design.

## Project Structure

```
app/
├── __init__.py
├── main.py                 # FastAPI application entry point
├── database/              # Database configuration
│   ├── __init__.py
│   └── config.py
├── models/               # SQLAlchemy models
│   ├── __init__.py
│   └── models.py
├── schemas/             # Pydantic schemas
│   ├── __init__.py
│   └── schemas.py
├── routes/              # API endpoints
│   ├── __init__.py
│   ├── users.py
│   └── transactions.py
└── utils/               # Utility functions
    ├── __init__.py
    └── pagination.py
```

## Features

- Modular project structure
- RESTful API design
- SQLite database with SQLAlchemy ORM
- Pydantic data validation
- Cursor-based pagination
- Nested schema design for better data organization
- Type hints throughout the codebase

## Data Models

### User
```python
{
    "info": {
        "name": "string",
        "email": "string"
    },
    "metadata": {
        "id": "string",
        "created_at": "datetime"
    }
}
```

### Transaction
```python
{
    "details": {
        "amount": "string",
        "description": "string"
    },
    "metadata": {
        "id": "string",
        "timestamp": "datetime"
    },
    "user_id": "string"
}
```

## API Endpoints

### Health Check
- `GET /api/v1/health` - Check API health status

### Users
- `GET /api/v1/users` - List users (paginated)
- `POST /api/v1/users` - Create a new user
- `GET /api/v1/users/{user_id}` - Get a specific user

### Transactions
- `GET /api/v1/transactions` - List transactions (paginated)
- `POST /api/v1/users/{user_id}/transactions` - Create a transaction for a user
- `GET /api/v1/transactions/{transaction_id}` - Get a specific transaction

## Setup and Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd stripe-standard-api-boilerplate
```

### 2. Set Up the Environment

Install [Poetry](https://python-poetry.org/) if not already installed:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Install dependencies:
```bash
poetry install
```

### 3. Run the API

Activate the virtual environment and start the FastAPI development server:
```bash
poetry shell
poetry run uvicorn app.main:app --reload
```

The server will be accessible at `http://127.0.0.1:8000`.

## API Documentation

Once the server is running, you can access:
- Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc`

## Pagination

All list endpoints support cursor-based pagination with the following parameters:
- `limit`: Maximum number of items to return (default: 10, max: 100)
- `starting_after`: Cursor for pagination (optional)

Example:
```bash
GET /api/v1/users?limit=5&starting_after=user_abc123
```

## Error Handling

The API uses standard HTTP status codes:
- `200`: Success
- `201`: Resource created
- `400`: Bad request
- `404`: Resource not found
- `500`: Server error

Error responses follow this format:
```json
{
    "detail": "Error message"
}
```

## Development

The project follows a modular structure:
- `database/`: Database configuration and connection management
- `models/`: SQLAlchemy models representing database tables
- `schemas/`: Pydantic models for request/response validation
- `routes/`: API endpoints grouped by resource
- `utils/`: Utility functions and helpers

## Contributing
Feel free to contribute by submitting issues or pull requests to improve this boilerplate.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

