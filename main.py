from fastapi import FastAPI, status
from models import TransactionCreate, TransactionUpdate, Transaction
from db import SessionDep, create_db_and_tables
from sqlmodel import select
from fastapi.exceptions import HTTPException

app = FastAPI(lifespan=create_db_and_tables)

@app.get("/")
async def read_root():
    return {"message": "FastAPI Finance API"}

@app.post("/transactions", response_model=Transaction)
async def create_transaction(transaction: TransactionCreate, session: SessionDep):
    transaction_db = Transaction.model_validate(transaction)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_db

@app.get("/transactions/{transaction_id}", response_model=Transaction)
async def read_transaction(transaction_id: int, session: SessionDep):
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction

@app.delete("/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(transaction_id: int, session: SessionDep):
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    session.delete(transaction)
    session.commit()
    return {"detail": "Transaction deleted"}

@app.patch("/transactions/{transaction_id}", response_model=Transaction, status_code=status.HTTP_201_CREATED)
async def update_transaction(transaction_id: int, transaction_data: TransactionUpdate, session: SessionDep):
    transaction_db = session.get(Transaction, transaction_id)
    if not transaction_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    transaction_data_dict = transaction_data.model_dump(exclude_unset=True)
    transaction_db.sqlmodel_update(transaction_data_dict)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_db

@app.get("/transactions", response_model=list[Transaction])
async def list_transactions(session: SessionDep):
    return session.exec(select(Transaction)).all()
