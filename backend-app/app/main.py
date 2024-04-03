from fastapi import FastAPI

from .api import auth, users, fileupload

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(fileupload.router)

@app.get('/')
async def root():
    return {'message': 'live'}
