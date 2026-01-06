from fastapi import status

transaction_in = {
    "type": "expense",
    "amount": 100,
    "date": "2022-01-01T00:00:00",
    "note": "test transaction"
}

transaction_update = {
    "type": "income",
    "amount": 200,
    "date": "2022-01-02T00:00:00",
    "note": "test transaction update"
}

def test_create_transaction(client):
    response = client.post("/api/transactions", json=transaction_in)
    assert response.status_code == status.HTTP_201_CREATED

def test_read_transaction(client):
    response = client.post("/api/transactions", json=transaction_in)
    assert response.status_code == status.HTTP_201_CREATED
    transaction_id: int = response.json()["id"]
    response_read = client.get(f"/api/transactions/{transaction_id}")
    assert response_read.status_code == status.HTTP_200_OK
    assert response_read.json()["type"] == transaction_in["type"]
    assert response_read.json()["amount"] == transaction_in["amount"]
    assert response_read.json()["date"] == transaction_in["date"]
    assert response_read.json()["note"] == transaction_in["note"]

def test_delete_transaction(client):
    response = client.post("/api/transactions", json=transaction_in)
    assert response.status_code == status.HTTP_201_CREATED
    transaction_id: int = response.json()["id"]
    response_delete = client.delete(f"/api/transactions/{transaction_id}")
    assert response_delete.status_code == status.HTTP_200_OK
    response_read = client.get(f"/api/transactions/{transaction_id}")
    assert response_read.status_code == status.HTTP_404_NOT_FOUND

def test_update_transaction(client):
    response = client.post("/api/transactions", json=transaction_in)
    assert response.status_code == status.HTTP_201_CREATED
    transaction_id: int = response.json()["id"]
    response_update = client.patch(f"/api/transactions/{transaction_id}", json=transaction_update)
    assert response_update.status_code == status.HTTP_200_OK
    response_read = client.get(f"/api/transactions/{transaction_id}")
    assert response_read.status_code == status.HTTP_200_OK
    assert response_read.json()["type"] == transaction_update["type"]
    assert response_read.json()["amount"] == transaction_update["amount"]
    assert response_read.json()["date"] == transaction_update["date"]
    assert response_read.json()["note"] == transaction_update["note"]

def test_list_transactions(client):
    response = client.post("/api/transactions", json=transaction_in)
    assert response.status_code == status.HTTP_201_CREATED
    response_list = client.get("/api/transactions")
    assert response_list.status_code == status.HTTP_200_OK
    assert response_list.json()[0]["type"] == transaction_in["type"]
    assert response_list.json()[0]["amount"] == transaction_in["amount"]
    assert response_list.json()[0]["date"] == transaction_in["date"]
    assert response_list.json()[0]["note"] == transaction_in["note"]
