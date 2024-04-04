backend-start: from source: 
```
uvicorn app.main:app --reload
```
frontend-start: from frontend-app: 
```
yarn start
```


BC server
{
  "email": "testing@testing.com",
  "password": "testing"
}


Scopes are used to grant an application different levels of access to data on behalf of the end user. Each API may declare one or more scopes.

API requires the following scopes. Select which ones you want to grant to Swagger UI.

OAuth2PasswordBearer (OAuth2, password)
Authorized
Token URL: token

Flow: password

username: testing@testing.com
password: ******
Client credentials location: basic
client_secret: ******