# Main file
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.core.database import database
from app.exceptions.exception_handlers import validation_exception_handler

app = FastAPI()


app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
