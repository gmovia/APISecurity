from fastapi import FastAPI
from routes.access import access

app = FastAPI()

app.include_router(access)