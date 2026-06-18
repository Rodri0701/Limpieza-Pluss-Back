from sqlalchemy import Column, Integer, String
from ..config.database import Base

class Usuarios(Base):
    __tablename__ = "usuarios" #NOMBRE DE LA TABLA
    
    id_user = Column(Integer, primary_key= True, index= True) #CREAR LA PRIMARY KEY
    email = Column(String(100), unique=True, index=True, nullable=False) 
    nombre = Column(String(50), nullable=False) 
    apellido = Column(String(50), nullable=False)
    edad = Column(Integer, nullable=False) 
    calle = Column(String(100), nullable=True)
    colonia = Column(String(100), nullable=True)
    num_exterior = Column(String(20), nullable=True) 
    hashed_password = Column(String(255), nullable=False)
    roll = Column(String(20), nullable = False, default= "user")
    
    
    