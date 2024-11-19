from sqlalchemy import Column, Integer, String, Float
from database import Base

class Transaction(Base):
    """
    Represents a financial transaction, either income or expense.
    """
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)  # Transaction date (ISO 8601 format)
    category = Column(String, index=True)  # Category of the transaction
    amount = Column(Float, nullable=False)  # Amount of money involved
    type = Column(String, nullable=False)  # Either 'income' or 'expense'
    description = Column(String, nullable=True)  # Optional description
