def test_create_upload_file_unauthenticated(unauth_client):
    files = {"file": ("test.csv", "1,2,3\n4,5,6\n7,8,9\n")}
    response = unauth_client.post("/fileupload/", files=files)
    assert response.status_code == 401


def test_create_upload_file_wrong_file(client, files_bad_type):
    response = client.post("/fileupload/", files=files_bad_type)
    assert response.status_code == 422
    assert response.json()["detail"] == "File needs to have .csv format."


def test_create_upload_file_new(client, files_good):
    response = client.post("/fileupload/", files=files_good)

    assert response.status_code == 200
    assert response.json() == "Table with name file_table created"


def test_create_upload_file_update(client, file_db, files_good_updated):
    response = client.post("/fileupload/", files=files_good_updated)

    assert response.status_code == 200
    assert response.json() == "Table with name file_table updated"
