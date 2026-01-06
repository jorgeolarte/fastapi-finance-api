
from models import Transaction, TransactionCreate, TransactionUpdate, Label, TransactionReadWithLabels
from sqlmodel import select
from db import SessionDep
from fastapi import status, APIRouter, HTTPException

router = APIRouter(prefix="/api/transactions", tags=["transactions"])

@router.post("/", response_model=TransactionReadWithLabels, status_code=status.HTTP_201_CREATED)
async def create_transaction(transaction_in: TransactionCreate, session: SessionDep):
    transaction_db = Transaction.model_validate(transaction_in)
    if transaction_in.label_ids:
        transaction_db.labels = session.exec(select(Label).where(Label.id.in_(transaction_in.label_ids))).all()
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_db

@router.get("/{transaction_id}", response_model=TransactionReadWithLabels, status_code=status.HTTP_200_OK)
async def read_transaction(transaction_id: int, session: SessionDep):
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction

@router.delete("/{transaction_id}", status_code=status.HTTP_200_OK)
async def delete_transaction(transaction_id: int, session: SessionDep):
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    session.delete(transaction)
    session.commit()
    return {"detail": "Transaction deleted"}

@router.patch("/{transaction_id}", response_model=TransactionReadWithLabels, status_code=status.HTTP_200_OK)
async def update_transaction(transaction_id: int, transaction_in: TransactionUpdate, session: SessionDep):
    transaction_db = session.get(Transaction, transaction_id)
    if not transaction_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    transaction_data_dict = transaction_in.model_dump(exclude_unset=True)
    transaction_db.sqlmodel_update(transaction_data_dict)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_db

@router.get("/", response_model=list[TransactionReadWithLabels], status_code=status.HTTP_200_OK)
async def list_transactions(session: SessionDep):
    return session.exec(select(Transaction)).all()
