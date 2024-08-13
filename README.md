# Spreadsheet Uploader Tool


To run: 

# Backend: 
## .env
FASTAPI_SECRET_KEY=
FASTAPI_HASH_ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
USER_DB_URL="sqlite:///:memory:"
FILE_DB_URL="sqlite:///:memory:"

```
cd backend-app
poetry install
poetry run uvicorn app.main:app --reload
```
to run pytest
```
poetry run pytest
```
docs available with SwaggerUI at `http://localhost:8000/docs`

# Frontend

```
cd frontend-app
npm install
npm run dev
```

