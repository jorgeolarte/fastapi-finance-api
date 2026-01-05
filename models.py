from pydantic import BaseModel
from sqlmodel import SQLModel, Field
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
    pass

class TransactionUpdate(TransactionBase):
    pass

class Transaction(TransactionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
