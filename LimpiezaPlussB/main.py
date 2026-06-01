from fastapi import FastAPI #SE IMPORTA FASTAPI
from .config.database import engine, Base
from .routes.product_route import router as producto_router


app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(producto_router)


@app.get("/")
def inicio():
    return {"mensaje": "Api en funcionamiento_ si "}


@app.get("/hola")
def hola():
    return {"mensaje:" "Holaaa soy el hola"}

