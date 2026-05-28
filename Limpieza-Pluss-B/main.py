from fastapi import FastAPI #SE IMPORTA FASTAPI
from .routes.user_routes import router as user_router

app = FastAPI()

app.include_router(user_router)