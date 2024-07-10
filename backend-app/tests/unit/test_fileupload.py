# # Mock user authentication function
# def mock_get_current_active_user():
#     # Simulate an authenticated user
#     return User(id=1, email="test@example.com", is_active=True)


def test_create_upload_file_authenticated(client):
    files = {"file": ("test.csv", "1,2,3\n4,5,6\n7,8,9\n")}
    response = client.post("/fileupload/", files=files)
    assert response.status_code == 200
    assert '{"1":{"0":4,"1":7},"2":{"0":5,"1":8},"3":{"0":6,"1":9}}' in response.json()


def test_create_upload_file_unauthenticated(unauth_client):
    # Test without patching, so the request is unauthenticated
    files = {"file": ("test.csv", "1,2,3\n4,5,6\n7,8,9\n")}
    response = unauth_client.post("/fileupload/", files=files)
    assert response.status_code == 401  # Assuming 401 Unauthorized for unauthenticated requests


def test_create_upload_file_wrong_file(client):
    files = {"file": ("test.txt", "1,2,3\n4,5,6\n7,8,9\n")}
    response = client.post("/fileupload/", files=files)
    assert response.status_code == 422
    assert response.json()["detail"] == "File needs to have .csv format."
