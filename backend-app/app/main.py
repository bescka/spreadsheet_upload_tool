import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import auth, fileupload, users
from .api.users import init_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

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


@app.on_event("startup")
def on_startup():
    init_db()


# @app.get('/')
# async def root():
#     return {'message': 'live'}
