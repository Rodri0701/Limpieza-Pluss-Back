from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..schemas.product_schema import ProductoCreate
from ..services.product_service import crear_producto
from ..config.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
        
    finally:
        db.close()
        
@router.post("/productos")
def crear(producto: ProductoCreate, db: Session = Depends(get_db)):
    return crear_producto(db, producto)