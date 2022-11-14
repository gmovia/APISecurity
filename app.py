from fastapi import FastAPI
from routes.accessSQLi import SQLi
from routes.access import access

app = FastAPI()

app.include_router(access)
app.include_router(SQLi)
