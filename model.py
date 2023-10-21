import enum

from sqlalchemy import Column, Enum, Integer, String, Date

from db import Base


class Materia(str, enum.Enum):
    Gimansia = "g"
    Musculacion = "m"
    Aerobico = "a"


class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(30), nullable=False)
    apellido = Column(String(30), nullable=False)
    fecha_de_nacimiento = Column(Date)


class Teacher(Base):
    __tablename__ = "teacher"

    id = Column(Integer, primary_key=True)
    fecha_de_ingreso = Column(Date)
    nombre = Column(String(30), nullable=False)
    apellido = Column(String(30), nullable=False)
    materia_a_dar = Column(Enum(Materia))