from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    direccion = Column(String)
    telefono = Column(String)
    correo = Column(String)
    lecturas = relationship("Lectura", back_populates="cliente")

class Lectura(Base):
    __tablename__ = "lecturas"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    fecha = Column(DateTime, default=datetime.utcnow)
    consumo = Column(Float)
    cliente = relationship("Cliente", back_populates="lecturas")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
