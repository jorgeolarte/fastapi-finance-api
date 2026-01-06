from fastapi import status

transaction_in = {
    "type": "expense",
    "amount": 100,
    "date": "2022-01-01T00:00:00",
    "note": "test transaction"
}

label_in = {
    "name": "test_label"
}

def test_add_label_to_transaction(client):
    response = client.post("/api/transactions", json=transaction_in)
    assert response.status_code == status.HTTP_201_CREATED
    transaction_id: int = response.json()["id"]
    response = client.post("/api/labels", json=label_in)
    assert response.status_code == status.HTTP_201_CREATED
    label_id: int = response.json()["id"]
    response = client.post(f"/api/transactions/{transaction_id}/labels/{label_id}")
    assert response.status_code == status.HTTP_201_CREATED

def test_remove_label_from_transaction(client):
    response = client.post("/api/transactions", json=transaction_in)
    assert response.status_code == status.HTTP_201_CREATED
    transaction_id: int = response.json()["id"]
    response = client.post("/api/labels", json=label_in)
    assert response.status_code == status.HTTP_201_CREATED
    label_id: int = response.json()["id"]
    response = client.post(f"/api/transactions/{transaction_id}/labels/{label_id}")
    assert response.status_code == status.HTTP_201_CREATED
    response = client.delete(f"/api/transactions/{transaction_id}/labels/{label_id}")
    assert response.status_code == status.HTTP_200_OK