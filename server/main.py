# Main file
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import database
from app.api import routers
from app.exceptions.exception_handlers import validation_exception_handler

app = FastAPI()

for router in routers:
    app.include_router(router, prefix="/api")

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9000"],  # Origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
