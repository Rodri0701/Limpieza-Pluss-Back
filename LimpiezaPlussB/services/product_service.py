from sqlalchemy.orm import Session
from ..models.product_model import Producto
from fastapi import HTTPException
from sqlalchemy import func
import re

def crear_producto(db: Session, producto):
    # nuevo_producto = Producto(
    # nombre_Producto=producto.nombre_Producto,
    # precio=producto.precio,
    # Descripcion=producto.Descripcion,
    # Categoria=producto.Categoria,
    # Stock=producto.Stock
    # )
    
#VALIDACIONES PARA NOMBRE
    
    producto.nombre_Producto = producto.nombre_Producto.strip() #Evita espacios extras en el nombre
    
     # VALIDAR QUE NO VAYA CON CARACTERES ESPECIALES
    if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s]+$', producto.nombre_Producto):
        raise HTTPException(
            status_code=400,
            detail="Nombre con caracteres inválidos"
    )
    
    #VALIDA QUE EL NOMBRE NO VAYA VACIO
    if not producto.nombre_producto.strip():
        raise HTTPException(
            status_code=400,
            detail="El nombre no puede ser vacio"
        )
        
       # VALIDAR MINUSCULAS O MAYUSCULAS POR IGUAL
    existe = db.query(Producto).filter(
       func.lower(Producto.nombre_Producto) == producto.nombre_Producto.lower()
).first()
    
#VALIDACIONES PARA EL PRECIO    

    #EL PRECIO NO PUEDE SER NEGATIVO O CERO
    if producto.precio <=0:
        raise HTTPException(
            status_code=400,
            detail="El precio no puede ser menor"
        )
        #EL PRECIO NO PUEDE SER MUY POR ENCIMA DE 100000
    if producto.precio >= 100000:
        raise HTTPException(
            status_code= 400,
            detail = "Precio extremadamente fuera del rango"
        )
        
#VALIDACIONES PARA EL STOCK
        #EL STOCK NO PUEDE SER MENOR A 5
    if producto.stock < 5:
        raise HTTPException(
            status_code=400,
            detail="No puedes tener stock por debajo de 5"
        )
        # EL STOCK NO PUEDE SER MAYOR A 10MIL
    if producto.stock >=10000:
        raise HTTPException(
            status_code= 400,
            detail = "No puedes agregar tanto a existencia"
        )

    # QUE NO HAYA DUCPLICADOS
    if existe:
        raise HTTPException(
            status_code=400,
            detail = "EN EXISTENCIA"
        )
     
    
        # CREA EL PRODUCTO SEGUN EL MODELO
    nuevo_producto = Producto(**producto.model_dump()) 
    
        
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    
    return nuevo_producto