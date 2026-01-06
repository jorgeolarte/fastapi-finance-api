from fastapi import status

label_in = {
    "name": "test_label"
}

label_update = {
    "name": "test_label_update"
}

def test_create_label(client):
    response = client.post("/api/labels", json=label_in)
    assert response.status_code == status.HTTP_201_CREATED

def test_read_label(client):
    response = client.post("/api/labels", json=label_in)
    assert response.status_code == status.HTTP_201_CREATED
    label_id: int = response.json()["id"]
    response_read = client.get(f"/api/labels/{label_id}")
    assert response_read.status_code == status.HTTP_200_OK
    assert response_read.json()["name"] == label_in["name"] 

def test_delete_label(client):
    response = client.post("/api/labels", json=label_in)
    assert response.status_code == status.HTTP_201_CREATED
    label_id: int = response.json()["id"]
    response_delete = client.delete(f"/api/labels/{label_id}")
    assert response_delete.status_code == status.HTTP_204_NO_CONTENT    
    response_read = client.get(f"/api/labels/{label_id}")
    assert response_read.status_code == status.HTTP_404_NOT_FOUND

def test_update_label(client):
    response = client.post("/api/labels", json=label_in)
    assert response.status_code == status.HTTP_201_CREATED
    label_id: int = response.json()["id"]
    response_update = client.patch(f"/api/labels/{label_id}", json=label_update)
    assert response_update.status_code == status.HTTP_200_OK
    response_read = client.get(f"/api/labels/{label_id}")
    assert response_read.status_code == status.HTTP_200_OK
    assert response_read.json()["name"] == label_update["name"]

def test_list_labels(client):
    response = client.post("/api/labels", json=label_in)
    assert response.status_code == status.HTTP_201_CREATED
    response_list = client.get("/api/labels")
    assert response_list.status_code == status.HTTP_200_OK
    assert response_list.json()[0]["name"] == label_in["name"]
