from fastapi import FastAPI, HTTPException, Depends, Query, Body, Path
from pydantic import BaseModel, EmailStr, validator
from sqlalchemy import create_engine, Column, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
from typing import List, Optional
from datetime import datetime
import uuid

# Database Setup
DATABASE_URL = "sqlite:///./app.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Models
class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    transactions = relationship("TransactionModel", back_populates="user")

class TransactionModel(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, index=True)
    amount = Column(String)
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String, ForeignKey("users.id"))

    user = relationship("UserModel", back_populates="transactions")

Base.metadata.create_all(bind=engine)

# Pydantic Models
class User(BaseModel):
    id: Optional[str] = None
    name: str
    email: EmailStr
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Transaction(BaseModel):
    id: Optional[str] = None
    amount: str
    description: str
    timestamp: Optional[datetime] = None
    user: Optional[User] = None

    class Config:
        from_attributes = True


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI App
app = FastAPI(title="Stripe-Style API", version="1.0.0")

# Health Endpoint
@app.get("/api/v1/health", tags=["Health"])
def health_check():
    """
    Check the health status of the API.

    Returns:
    - **status**: "ok" if the API is running.
    """
    return {"status": "ok"}

# Utility for Pagination
def paginate(query, limit: int, starting_after: Optional[str]):
    if starting_after:
        query = query.filter(UserModel.id > starting_after)
    return query.limit(limit).all()

# User Endpoints
@app.get("/api/v1/users", response_model=List[User], tags=["Users"])
def list_users(limit: int = Query(10, ge=1, le=100, example=10), starting_after: Optional[str] = Query(None, example="user_abc12345"), db: Session = Depends(get_db)):
    """
    Retrieve a paginated list of users.

    Parameters:
    - **limit**: Maximum number of users to return.
    - **starting_after**: Cursor for pagination.

    Returns:
    - List of users.
    """
    query = db.query(UserModel).order_by(UserModel.id)
    return paginate(query, limit, starting_after)

@app.post("/api/v1/users", response_model=User, status_code=201, tags=["Users"])
def create_user(user: User = Body(..., example={"name": "Jane Doe", "email": "jane.doe@example.com"}), db: Session = Depends(get_db)):
    """
    Create a new user.

    Parameters:
    - **name**: Full name of the user.
    - **email**: Valid email address.

    Returns:
    - The created user object.
    """
    user_id = f"user_{uuid.uuid4().hex[:8]}"
    db_user = UserModel(id=user_id, **user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/api/v1/users/{user_id}", response_model=User, tags=["Users"], responses={
    200: {
        "description": "User retrieved successfully",
        "content": {
            "application/json": {
                "example": {
                    "id": "user_abc12345",
                    "name": "Jane Doe",
                    "email": "jane.doe@example.com",
                    "created_at": "2024-01-01T00:00:00"
                }
            }
        }
    },
    404: {
        "description": "User not found",
        "content": {
            "application/json": {
                "example": {"detail": "User not found"}
            }
        }
    }
})
def get_user(user_id: str = Path(..., example="user_abc12345"), db: Session = Depends(get_db)):
    """
    Retrieve a specific user by ID.

    Parameters:
    - **user_id**: The ID of the user to retrieve.

    Returns:
    - The user object.

    Raises:
    - **404**: If the user is not found.
    """
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Transaction Endpoints
@app.get("/api/v1/transactions", response_model=List[Transaction], tags=["Transactions"])
def list_transactions(limit: int = Query(10, ge=1, le=100, example=10), starting_after: Optional[str] = Query(None, example="txn_abc12345"), db: Session = Depends(get_db)):
    """
    Retrieve a paginated list of transactions.

    Parameters:
    - **limit**: Maximum number of transactions to return.
    - **starting_after**: Cursor for pagination.

    Returns:
    - List of transactions.
    """
    query = db.query(TransactionModel).order_by(TransactionModel.id)
    return paginate(query, limit, starting_after)

@app.post("/api/v1/users/{user_id}/transactions", response_model=Transaction, status_code=201, tags=["Transactions"])
def create_transaction(user_id: str = Path(..., example="user_abc12345"), transaction: Transaction = Body(..., example={"amount": "100.00", "description": "Payment for services"}), db: Session = Depends(get_db)):
    """
    Create a new transaction for a user.

    Parameters:
    - **user_id**: The ID of the user.
    - **amount**: The transaction amount.
    - **description**: A description of the transaction.

    Returns:
    - The created transaction object.

    Raises:
    - **404**: If the user is not found.
    """
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    transaction_id = f"txn_{uuid.uuid4().hex[:8]}"
    db_transaction = TransactionModel(id=transaction_id, user_id=user_id, **transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.get("/api/v1/transactions/{transaction_id}", response_model=Transaction, tags=["Transactions"], responses={
    200: {
        "description": "Transaction retrieved successfully",
        "content": {
            "application/json": {
                "example": {
                    "id": "txn_abc12345",
                    "amount": "100.00",
                    "description": "Payment for services",
                    "timestamp": "2024-01-01T12:00:00",
                    "user": {
                        "id": "user_abc12345",
                        "name": "Jane Doe",
                        "email": "jane.doe@example.com"
                    }
                }
            }
        }
    },
    404: {
        "description": "Transaction not found",
        "content": {
            "application/json": {
                "example": {"detail": "Transaction not found"}
            }
        }
    }
})
def get_transaction(transaction_id: str = Path(..., example="txn_abc12345"), db: Session = Depends(get_db)):
    """
    Retrieve a specific transaction by ID.

    Parameters:
    - **transaction_id**: The ID of the transaction to retrieve.

    Returns:
    - The transaction object.

    Raises:
    - **404**: If the transaction is not found.
    """
    transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction
