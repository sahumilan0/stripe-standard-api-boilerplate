# Stripe-Style-API-Boilerplate

This repository provides a boilerplate for building APIs using FastAPI, following standards similar to those adopted by Stripe and other companies known for their excellent API designs. The structure and implementation in this boilerplate emphasize modularity, scalability, and adherence to best practices.
I am creating this boilerplate to share how to think about API design and how to implement it in a way that is easy to understand and maintain and set a new standard of boilerplate for API design.


I will keep on adding more features to this boilerplate and will keep on updating the README.md file to reflect the changes. Stay tuned for more updates.
- [ ] Making this boilerplate more modular and compliant with other databases and ORMs.
- [ ] Adding more features to the API like authentication, authorization, rate limiting, etc.
- [ ] Adding more features to the database models like indexes, constraints, etc.
- [ ] Adding more features to the API documentation like Swagger, ReDoc, etc.
- [ ] Adding more features to the API testing like pytest, etc.

## Why Build Good APIs?
A well-designed API:

- **Enhances Developer Experience**: Clear and consistent APIs are easier to use and integrate.
- **Facilitates Scalability**: Thoughtful design ensures the API can grow with the application's needs.
- **Improves Maintainability**: Standardized practices reduce the complexity of maintaining and updating APIs.
- **Encourages Adoption**: Developers are more likely to adopt APIs that are intuitive and reliable.

Stripe is a prime example of how excellent API design can accelerate developer adoption and enable seamless integration across different platforms.

## Features of This Boilerplate

- [x] **Health Check Endpoint**: Quickly verify the API's availability.
- [x] **User Management**: Create, retrieve, and paginate users.
- [x] **Transaction Management**: Manage transactions associated with users.
- [x] **Pagination**: Cursor-based pagination for efficient data handling.
- [x] **Data Models**: Cleanly separated SQLAlchemy models for database interactions and Pydantic models for validation and response schemas.
- [ ] **Clear Documentation**: Swagger UI (`/docs`) and ReDoc (`/redoc`) auto-generated documentation with examples for testing.

## How to Use This Boilerplate

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/stripe-standard-api-boilerplate.git
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

### 4. Test the Endpoints
Use the Swagger UI at `http://127.0.0.1:8000/docs` or ReDoc at `http://127.0.0.1:8000/redoc` to explore and test the API endpoints.

## API Endpoints

### Health
- **`GET /api/v1/health`**: Returns the health status of the API.

### Users
- **`GET /api/v1/users`**: Retrieve a paginated list of users.
  - Query Parameters:
    - `limit`: Maximum number of users to return (default: 10).
    - `starting_after`: Cursor for pagination (ID of the last user from the previous page).
- **`POST /api/v1/users`**: Create a new user.
  - Request Body:
    ```json
    {
      "name": "Jane Doe",
      "email": "jane.doe@example.com"
    }
    ```
- **`GET /api/v1/users/{user_id}`**: Retrieve details of a specific user.

### Transactions
- **`GET /api/v1/transactions`**: Retrieve a paginated list of transactions.
  - Query Parameters:
    - `limit`: Maximum number of transactions to return (default: 10).
    - `starting_after`: Cursor for pagination (ID of the last transaction from the previous page).
- **`POST /api/v1/users/{user_id}/transactions`**: Create a transaction for a specific user.
  - Request Body:
    ```json
    {
      "amount": "100.00",
      "description": "Payment for services"
    }
    ```
- **`GET /api/v1/transactions/{transaction_id}`**: Retrieve details of a specific transaction.

## How Stripe Achieves This
Stripe’s API is widely regarded as a gold standard because:

- **Consistency**: Uniform endpoint naming, parameter structures, and response formats.
- **Clear Documentation**: Detailed examples and use cases for every endpoint.
- **Error Handling**: Clear and actionable error messages.
- **Versioning**: Ensures backward compatibility while enabling incremental improvements.
- **Developer Support**: Comprehensive SDKs, libraries, and tools to facilitate integration.

By following similar principles, this boilerplate aims to provide a foundation for building high-quality APIs.

## Contributing
Feel free to contribute by submitting issues or pull requests to improve this boilerplate.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

