from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models import Transaction
from schemas import TransactionCreate, TransactionResponse
from typing import List

app = FastAPI()

# Initialize the database
init_db()

# Configure CORS for frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust based on frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/transactions/", response_model=TransactionResponse)
def add_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    """
    Adds a new transaction to the database.
    """
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.get("/transactions/", response_model=List[TransactionResponse])
def get_transactions(db: Session = Depends(get_db)):
    """
    Retrieves all transactions from the database.
    """
    return db.query(Transaction).all()

@app.put("/transactions/{transaction_id}", response_model=TransactionResponse)
def update_transaction(transaction_id: int, transaction: TransactionCreate, db: Session = Depends(get_db)):
    """
    Updates an existing transaction by its ID.
    """
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    for key, value in transaction.dict().items():
        setattr(db_transaction, key, value)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """
    Deletes a transaction by its ID.
    """
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(db_transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}

@app.get("/summary/")
def get_summary(db: Session = Depends(get_db)):
    """
    Provides a summary of total income, total expenses, and savings.
    """
    income = db.query(Transaction).filter(Transaction.type == "income").all()
    expenses = db.query(Transaction).filter(Transaction.type == "expense").all()
    income_total = sum(item.amount for item in income)
    expenses_total = sum(item.amount for item in expenses)
    savings = income_total - expenses_total
    return {"income": income_total, "expenses": expenses_total, "savings": savings}
