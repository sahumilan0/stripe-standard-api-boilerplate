from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserInfo:
    def __init__(self, name: str, email: EmailStr):
        self.name = name
        self.email = email

class UserMetadata:
    def __init__(self, created_at: datetime, id: Optional[str] = None):
        self.id = id
        self.created_at = created_at

class User(BaseModel):
    info: UserInfo
    metadata: UserMetadata
    
    @classmethod
    def create(cls, name: str, email: EmailStr):
        return cls(
            info=UserInfo(name=name, email=email),
            metadata=UserMetadata(created_at=datetime.utcnow())
        )

class TransactionDetails:
    def __init__(self, amount: str, description: str):
        self.amount = amount
        self.description = description

class TransactionMetadata:
    def __init__(self, timestamp: datetime, id: Optional[str] = None):
        self.id = id
        self.timestamp = timestamp

class Transaction(BaseModel):
    details: TransactionDetails
    metadata: TransactionMetadata
    user_id: str
    
    @classmethod
    def create(cls, amount: str, description: str, user_id: str):
        return cls(
            details=TransactionDetails(amount=amount, description=description),
            metadata=TransactionMetadata(timestamp=datetime.utcnow()),
            user_id=user_id
        ) 