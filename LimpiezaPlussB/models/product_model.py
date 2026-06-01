from sqlalchemy import Column,Integer,String,Float, Double #IMPORTA FRAGMENTOS DE LA TABLA DE SQL COMO NORMALMENTE SE HACE DE FORMA NATIVA EN UN GESTOR DE BD
from ..config.database import Base #IMPORTAMOS EL DATABASE.PY 


class Producto(Base): #Clase para crear la tabla que sera en base de datos desde python
    __tablename__ = "productos" #NOMBRE DE LA TABLA QUE SE ALOJARA EN LA BD CREADA EN PYTHON
    
    id_Producto = Column(Integer, primary_key=True, index=True) #CREAMOS UN CAMPO COMO SE HARIA EN LA BASE DE DATOS
    nombre_Producto = Column(String) #COLUMNA DE TIPO STRING PARA EL NOMBRE
    precio = Column(Float) #COLUMNA DEL TIPO Float
    Descripcion = Column(String) #COLUMNA DE TIPO STRING
    Categoria = Column(String) #COLUMNA DE TIPO STRING
    Stock = Column(Integer) 
    
