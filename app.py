from fastapi import FastAPI
from routes.accessSQLi import SQLi
from routes.access import access
from routes.passwordRecovery import passwordRecovery

app = FastAPI()

app.include_router(access)
app.include_router(SQLi)
app.include_router(passwordRecovery)
