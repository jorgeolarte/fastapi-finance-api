from fastapi import FastAPI
from db import create_db_and_tables
from .routers import transactions, labels, transaction_labels

app = FastAPI(lifespan=create_db_and_tables)
app.include_router(transactions.router)
app.include_router(labels.router)
app.include_router(transaction_labels.router)

@app.get("/")
async def read_root():
    return {"message": "FastAPI Finance API"}

