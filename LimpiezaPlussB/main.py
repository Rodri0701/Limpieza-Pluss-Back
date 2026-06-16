from fastapi import FastAPI #SE IMPORTA FASTAPI
from .config.database import engine, Base
from .routes.product_route import router as producto_router
from .routes.user_routes import router as User_Router


app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(producto_router)
app.include_router(User_Router)


@app.get("/")
def inicio():
    return {"mensaje": "Api en funcionamiento_ si "}


@app.get("/hola")
def hola():
    return {"mensaje:" "Holaaa soy el hola"}

