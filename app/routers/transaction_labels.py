from models import Transaction, Label
from sqlmodel import select
from db import SessionDep
from fastapi import status, APIRouter, HTTPException

router = APIRouter(prefix="/api/transactions", tags=["transaction_labels"])

@router.post("/{transaction_id}/labels/{label_id}", status_code=status.HTTP_204_NO_CONTENT)
async def add_label_to_transaction(transaction_id: int, label_id: int, session: SessionDep):
    transaction_db = session.get(Transaction, transaction_id)
    if not transaction_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    label_db = session.get(Label, label_id)
    if not label_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Label not found")
    transaction_db.labels.append(label_db)
    session.add(transaction_db)
    session.commit()
    return {"detail": "Label added to transaction"}

@router.delete("/{transaction_id}/labels/{label_id}", status_code=status.HTTP_200_OK)
async def remove_label_from_transaction(transaction_id: int, label_id: int, session: SessionDep):
    transaction_db = session.get(Transaction, transaction_id)
    if not transaction_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    label_db = session.get(Label, label_id)
    if not label_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Label not found")
    transaction_db.labels.remove(label_db)
    session.add(transaction_db)
    session.commit()
    return {"detail": "Label removed from transaction"}