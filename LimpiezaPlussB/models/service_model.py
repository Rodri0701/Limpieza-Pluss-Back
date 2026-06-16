from sqlalchemy import Column,Integer,String, Numeric, DateTime, Boolean  #IMPORTA FRAGMENTOS DE LA TABLA DE SQL COMO NORMALMENTE SE HACE DE FORMA NATIVA EN UN GESTOR DE BD
from ..config.database import Base #IMPORTAMOS EL DATABASE.PY

#TABLAS PARA CREAR  LA TABLA EN LA BASE DE DATOS DESDE PYTHON
class Servicio(Base):
    __tablename__ = "servicios" #NOMBRE DE LA TABLA QUE SE ALOJARA EN LA BD CREADA EN PYTHON
    
    id_Servicio = Column(Integer, primary_key=True, index=True) #CREAMOS UN CAMPO COMO SE HARIA EN LA BASE DE DATOS
    nombre_Servicio = Column(String(100), unique=True, nullable=False) #COLUMNA DE TIPO STRING PARA EL NOMBRE
    precio = Column(Numeric(10,2), nullable= False) #COLUMNA DEL NUMERIC Float
    Descripcion = Column(String(500), nullable= False) #COLUMNA DE TIPO STRING
    #Categoria = Column(String(100), nullable= False) #COLUMNA DE TIPO STRING
    Status_servicio = Column(Boolean, default=True) #COLUMNA DE TIPO BOOLEAN PARA CONTROLAR EL ESTATUS DEL SERVICIO
    fecha_reserva = Column(DateTime, nullable=True) #COLUMNA PARA SABER QUE DIA SE RESERVO
    user_reserva = Column(String(50)) #Debería ser FK?
    fecha_creacion = Column(DateTime, default=DateTime)
    user_alta = Column(String(50), nullable= True) 
    
    user_id =Column(Integer, models.ForeignKey("user_model", verbose_name=_("user_id"), on_delete=models.CASCADE))
    
    
    #COLUMNAS PARA COTROLAR LA EDICION DE LA INFORMACIÓN
    
    user_update = Column(String(50), nullable= True)
    fecha_update = Column(DateTime, nullable= True)
    
    
    
    
    