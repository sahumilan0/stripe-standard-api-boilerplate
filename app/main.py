from fastapi import FastAPI
from .database.config import engine, Base
from .routes import users, transactions

# Create database tables
Base.metadata.create_all(bind=engine)

# FastAPI App
app = FastAPI(
    title="Stripe-Style API",
    version="1.0.0",
    description="A RESTful API following Stripe-like patterns"
)

# Health Endpoint
@app.get("/api/v1/health", tags=["Health"])
def health_check():
    """
    Check the health status of the API.
    """
    return {"status": "ok"}

# Include routers
app.include_router(users.router)
app.include_router(transactions.router)
