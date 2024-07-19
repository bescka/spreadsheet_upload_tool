# spreadsheet_uploader
Uploader tool


## Backend
`pip install -r requirements.txt`
`cd backend-app`
`uvicorn app.main:app --reload`

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
- ~~__[Rudolf] Authentication and FastAPI end point setup__~~

for 28/03/2024:
- ~~[Ben] Provide sample csv file~~
- ~~[Ben] Front end outline with login page and buttons~~
- ~~[Rudi] CRUD for user DB~~ 
- ~~[Rudi] Split into multiple files~~

04/04/2024:
- Review and tie the two together (aws review/ lambda function etc. S3?)

  - ~~[Rudi] Tests (using sample data)~~
  - ~~[Ben] implement middleware stuff/ connection~~
  
11/04/2024: 
- Focus: Front and backend processes for file upload
  - [Rudi] Do all the tests. ALL the tests.
  - ~~[Rudi] Permissions, cleanup (auth)~~
  - ~~[Rudi] Admin user~~
  
  - [Ben] Uploader page
  - [Rudolf] To give lecture on Airflow and CI/ github actions
  
  

Other
  - [Ben] frontend testing framework? 
  - [Ben] https? 


- Session: 
  - review git actions
    - when you push they run tests? 

## Steps TODO 
- Staging/ Prod env?
  - proddb
- Hosting (AWS) - lambda or separate host? 
- CSS/ Frontend
- Containerization? Docker? Kubernetes? 
- Continuous integration? 
- Resolve **DeprecationWarning**: crypt 
- Resolve **DeprecationWarning**: app to --> explicit style 
- Check 404 Exceptions 

## Discussion 
- 

## Process Qu
- Best practice for commits/ git management
- How does rebasing work? 
- Where do you put tokens securely? local storage might be accessible from javascripts. 
- **How to handel unregistered users?**

## Questions
JWT uses only username why?
