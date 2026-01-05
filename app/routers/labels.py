from models import Label, LabelCreate, LabelUpdate
from sqlmodel import select
from fastapi import status, APIRouter, HTTPException
from db import SessionDep

router = APIRouter(prefix="/api/labels", tags=["labels"])

@router.post("/", response_model=Label)
async def create_label(label: LabelCreate, session: SessionDep):
    label_db = Label.model_validate(label)
    session.add(label_db)
    session.commit()
    session.refresh(label_db)
    return label_db

@router.get("/{label_id}", response_model=Label)
async def read_label(label_id: int, session: SessionDep):
    label = session.get(Label, label_id)
    if not label:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Label not found")
    return label

@router.delete("/{label_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_label(label_id: int, session: SessionDep):
    label = session.get(Label, label_id)
    if not label:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Label not found")
    session.delete(label)
    session.commit()
    return {"detail": "Label deleted"}

@router.patch("/{label_id}", response_model=Label, status_code=status.HTTP_201_CREATED)
async def update_label(label_id: int, label_data: LabelUpdate, session: SessionDep):
    label_db = session.get(Label, label_id)
    if not label_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Label not found")
    label_db = Label.model_validate(label_data)
    session.add(label_db)
    session.commit()
    session.refresh(label_db)
    return label_db

@router.get("/", response_model=list[Label])
async def list_labels(session: SessionDep):
    return session.exec(select(Label)).all()
