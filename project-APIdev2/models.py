from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Speler(Base):
    __tablename__ = "spelers"

    id = Column(Integer, primary_key=True, index=True)
    naam = Column(String, index=True)
    achternaam = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    leeftijd = Column(Integer, index=True)
    nationaliteit = Column(String, index=True)
    is_active = Column(Boolean, default=True)

    ploeg = relationship("ploeg", back_populates="ploegen")


class ploeg(Base):
    __tablename__ = "ploeg"

    id = Column(Integer, primary_key=True, index=True)
    titels = Column(Integer, index=True)
    regio = Column(Integer, index=True)
    huidige_positie = Column(Integer, index=True)
    ploeg_id = Column(Integer, ForeignKey("spelers.id"))

    ploegen = relationship("Speler", back_populates="ploeg")
