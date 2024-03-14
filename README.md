# spreadsheet_uploader
Uploader tool

## Requirements

Main objectives
* authentication for user to enter web frontend
* function to upload file with button
* tests for file format?
* pydantic data model
* fast api communication with database
* upload to s3 bucket - push to lamda function which writes to database


* [EXTENSION] Form type upload

Initial format for KH upload:

| name | email | id | 01/01/2024 | 02/01/2024 | 03/01/2024 |
| tony |       |    | 5          | 6          | 0          |
|      |       |    |            |            |            |

* Open file
* Preview screen? Showing data to be uploaded
* Check for changes, insert changes to database
* Give the user some sort of feedback:
  * Upload successful, added: .......
  * Upload unsuccessful, columns/ and or blah not in right format?

* Endpoint: Upload depends on security


Schedule:

for 21/03/2024:
- [Rudolf] Authentication and FastAPI end point setup
- [Ben] Front end outline with login page and upload buttons

21/03/2024:
- Review and tie the two together (aws review/ lambda function etc. S3?)




