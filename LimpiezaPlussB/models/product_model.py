from sqlalchemy import Column,Integer,String, Numeric #IMPORTA FRAGMENTOS DE LA TABLA DE SQL COMO NORMALMENTE SE HACE DE FORMA NATIVA EN UN GESTOR DE BD
from ..config.database import Base #IMPORTAMOS EL DATABASE.PY 


class Producto(Base): #Clase para crear la tabla que sera en base de datos desde python
    __tablename__ = "productos" #NOMBRE DE LA TABLA QUE SE ALOJARA EN LA BD CREADA EN PYTHON
    
    id_Producto = Column(Integer, primary_key=True, index=True) #CREAMOS UN CAMPO COMO SE HARIA EN LA BASE DE DATOS
    nombre_Producto = Column(String(100), unique=True, nullable=False) #COLUMNA DE TIPO STRING PARA EL NOMBRE
    precio = Column(Numeric(10,2), nullable= False) #COLUMNA DEL NUMERIC Float
    descripcion = Column(String(500), nullable= False) #COLUMNA DE TIPO STRING
    categoria = Column(String(100), nullable= False) #COLUMNA DE TIPO STRING
    stock = Column(Integer, nullable= False) 
    
