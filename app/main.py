from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from .api import auth, users, fileupload

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(fileupload.router)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return {'message': 'live'}


