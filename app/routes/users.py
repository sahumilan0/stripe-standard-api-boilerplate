from fastapi import APIRouter, HTTPException, Depends, Query, Body, Path
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from ..database.config import get_db
from ..models.models import UserModel
from ..schemas.schemas import User
from ..utils.pagination import paginate

router = APIRouter(prefix="/api/v1/users", tags=["Users"])

@router.get("/", response_model=List[User])
def list_users(
    limit: int = Query(10, ge=1, le=100, example=10),
    starting_after: Optional[str] = Query(None, example="user_abc12345"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a paginated list of users.
    """
    query = db.query(UserModel).order_by(UserModel.id)
    users = paginate(query, limit, starting_after)
    return [user.to_schema() for user in users]

@router.post("/", response_model=User, status_code=201)
def create_user(
    user: User = Body(..., example={
        "info": {"name": "Jane Doe", "email": "jane.doe@example.com"}
    }),
    db: Session = Depends(get_db)
):
    """
    Create a new user.
    """
    user_id = f"user_{uuid.uuid4().hex[:8]}"
    db_user = UserModel(
        id=user_id,
        name=user.info.name,
        email=user.info.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user.to_schema()

@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: str = Path(..., example="user_abc12345"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific user by ID.
    """
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.to_schema() 