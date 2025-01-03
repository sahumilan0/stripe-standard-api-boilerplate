from fastapi import APIRouter, HTTPException, Depends, Query, Body, Path
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from ..database.config import get_db
from ..models.models import TransactionModel, UserModel
from ..schemas.schemas import Transaction
from ..utils.pagination import paginate

router = APIRouter(prefix="/api/v1", tags=["Transactions"])

@router.get("/transactions", response_model=List[Transaction])
def list_transactions(
    limit: int = Query(10, ge=1, le=100, example=10),
    starting_after: Optional[str] = Query(None, example="txn_abc12345"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a paginated list of transactions.
    """
    query = db.query(TransactionModel).order_by(TransactionModel.id)
    transactions = paginate(query, limit, starting_after)
    return [txn.to_schema() for txn in transactions]

@router.post("/users/{user_id}/transactions", response_model=Transaction, status_code=201)
def create_transaction(
    user_id: str = Path(..., example="user_abc12345"),
    transaction: Transaction = Body(..., example={
        "details": {"amount": "100.00", "description": "Payment for services"}
    }),
    db: Session = Depends(get_db)
):
    """
    Create a new transaction for a user.
    """
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    transaction_id = f"txn_{uuid.uuid4().hex[:8]}"
    db_transaction = TransactionModel(
        id=transaction_id,
        amount=transaction.details.amount,
        description=transaction.details.description,
        user_id=user_id
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction.to_schema()

@router.get("/transactions/{transaction_id}", response_model=Transaction)
def get_transaction(
    transaction_id: str = Path(..., example="txn_abc12345"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific transaction by ID.
    """
    transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction.to_schema() 