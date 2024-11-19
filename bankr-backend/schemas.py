from pydantic import BaseModel
from typing import Optional

class TransactionBase(BaseModel):
    """
    Base schema for transactions, used for both input and output.
    """
    date: str  # ISO 8601 date format
    category: str  # Transaction category (e.g., groceries, rent)
    amount: float  # Transaction amount
    type: str  # Either 'income' or 'expense'
    description: Optional[str] = None  # Optional description of the transaction

class TransactionCreate(TransactionBase):
    """
    Schema for creating a new transaction.
    """
    pass

class TransactionResponse(TransactionBase):
    """
    Schema for transaction responses, including the ID.
    """
    id: int  # Transaction ID

    class Config:
        orm_mode = True  # Enables ORM compatibility for SQLAlchemy models
