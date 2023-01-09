from sqlalchemy.orm import Session

import models
import schemas
import auth


def get_voetballer(db: Session, speler_id: int):
    return db.query(models.Speler).filter(models.Speler.id == speler_id).first()


def get_voetballer_by_email(db: Session, email: str):
    return db.query(models.Speler).filter(models.Speler.email == email).first()


def get_voetballers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Speler).offset(skip).limit(limit).all()


def maak_voetballer(db: Session, speler: schemas.SpelerCreate):
    hashed_password = auth.get_password_hash(speler.hashed_password)
    db_speler = models.Speler(naam=speler.naam, achternaam=speler.achternaam, email=speler.email, hashed_password=hashed_password,leeftijd=speler.leeftijd, nationaliteit=speler.nationaliteit)
    db.add(db_speler)
    db.commit()
    db.refresh(db_speler)
    return db_speler

def update_voetballer(db: Session, speler: schemas.SpelerCreate, speler_id: int):
    db_speler = get_voetballer(db=db, speler_id=speler_id)
    db_speler.naam = speler.naam
    db_speler.achternaam = speler.achternaam
    db_speler.email= speler.email
    db_speler.hashed_password= speler.hashed_password
    db_speler.leeftijd = speler.leeftijd
    db_speler.nationaliteit = speler.nationaliteit
    db.commit()
    db.refresh(db_speler)
    return db_speler


def verwijder_voetballer(db: Session,speler_id: int):
    db.query(models.Speler).filter(models.Speler.id== speler_id).delete()
    db.commit()

def get_ploeg(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ploeg).offset(skip).limit(limit).all()


def maak_ploeg(db: Session, ploeg: schemas.ploegCreate, speler_id: int):
    db_ploeg = models.ploeg(**ploeg.dict(), ploeg_id=speler_id)
    db.add(db_ploeg)
    db.commit()
    db.refresh(db_ploeg)
    return db_ploeg

def maak_voetballer_ploeg(db: Session, ploeg: schemas.ploegCreate, speler_id: int):
    db_ploeg = models.ploeg(**ploeg.dict(), ploeg_id=speler_id)
    db.add(db_ploeg)
    db.commit()
    db.refresh(db_ploeg)
    return db_ploeg

def verwijder_ploeg(db: Session,ploeg_id: int):
    db.query(models.ploeg).filter(models.ploeg.id== ploeg_id).delete()
    db.commit()


def create_user(db: Session, speler: schemas.SpelerCreate):
    hashed_password = auth.get_password_hash(speler.password)
    db_user = models.Speler(email=speler.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user