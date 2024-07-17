# # Mock user authentication function
# def mock_get_current_active_user():
#     # Simulate an authenticated user
#     return User(id=1, email="test@example.com", is_active=True)
import pytest


# TODO: Change files to fixtures
def test_create_upload_file_authenticated(client):
    files = {"file": ("test.csv", "1,2,3\n4,5,6\n7,8,9\n")}
    response = client.post("/fileupload/", files=files)
    assert response.status_code == 200
    assert '{"1":{"0":4,"1":7},"2":{"0":5,"1":8},"3":{"0":6,"1":9}}' in response.json()


def test_create_upload_file_unauthenticated(unauth_client):
    files = {"file": ("test.csv", "1,2,3\n4,5,6\n7,8,9\n")}
    response = unauth_client.post("/fileupload/", files=files)
    assert response.status_code == 401


def test_create_upload_file_wrong_file(client):
    files = {"file": ("test.txt", "1,2,3\n4,5,6\n7,8,9\n")}
    response = client.post("/fileupload/", files=files)
    assert response.status_code == 422
    assert response.json()["detail"] == "File needs to have .csv format."


### TODO: May Change later
def test_create_upload_file_test(client, files_good):
    response = client.post("/fileupload/", files=files_good)
    assert response.status_code == 200


def test_create_upload_file_test_bad_dtype(client, files_bad_dtype):
    with pytest.raises(
        AssertionError,
        match="object of column id doesn't match <class 'pandas.core.arrays.integer.Int64Dtype'>",
    ):
        response = client.post("/fileupload/", files=files_bad_dtype)


# def test_create_upload_file_test_bad_column(client, files_bad_column):
#     with pytest.raises(
#         AssertionError,
#         match="Unknown colum included",
#     ):
#         response = client.post("/fileupload/", files=files_bad_column)
