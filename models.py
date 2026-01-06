from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from enum import Enum

class TransactionType(str, Enum):
    EXPENSE = "expense"
    INCOME = "income"

class TransactionBase(SQLModel):
    type: TransactionType = Field(default=TransactionType.EXPENSE)
    amount: float = Field(default=0)
    date: datetime = Field(default_factory=datetime.now)
    note: str | None = Field(default=None)

class TransactionCreate(TransactionBase):
    label_ids: list[int] = Field(default_factory=list)

class TransactionUpdate(TransactionBase):
    label_ids: list[int] = Field(default_factory=list)

class LabelBase(SQLModel):
    name: str = Field(default="")

class LabelCreate(LabelBase):
    pass

class LabelUpdate(LabelBase):
    pass

class TransactionLabel(SQLModel, table=True):
    transaction_id: int = Field(foreign_key="transaction.id", primary_key=True)
    label_id: int = Field(foreign_key="label.id", primary_key=True)

class Transaction(TransactionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    labels: list["Label"] = Relationship(back_populates="transactions", link_model=TransactionLabel)

class Label(LabelBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    transactions: list["Transaction"] = Relationship(back_populates="labels", link_model=TransactionLabel)

class TransactionReadWithLabels(TransactionBase):
    labels: list[Label] = Field(default_factory=list)