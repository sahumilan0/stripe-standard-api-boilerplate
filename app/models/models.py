from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.config import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    # User Info
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    # User Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    transactions = relationship("TransactionModel", back_populates="user")

    def to_schema(self):
        from ..schemas.schemas import User, UserInfo, UserMetadata
        return User(
            info=UserInfo(name=self.name, email=self.email),
            metadata=UserMetadata(id=self.id, created_at=self.created_at)
        )

class TransactionModel(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, index=True)
    # Transaction Details
    amount = Column(String)
    description = Column(String)
    # Transaction Metadata
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String, ForeignKey("users.id"))

    user = relationship("UserModel", back_populates="transactions")

    def to_schema(self):
        from ..schemas.schemas import Transaction, TransactionDetails, TransactionMetadata
        return Transaction(
            details=TransactionDetails(amount=self.amount, description=self.description),
            metadata=TransactionMetadata(id=self.id, timestamp=self.timestamp),
            user_id=self.user_id
        ) 