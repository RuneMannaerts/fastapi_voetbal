from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import auth as _auth, crud as _crud, models as _models, schemas as _schemas
from database import SessionLocal, engine
import os

if not os.path.exists('.\sqlitedb'):
    os.makedirs('.\sqlitedb')

#"sqlite:///./sqlitedb/sqlitedata.db"
_models.Base.metadata.create_all(bind=engine)

app = FastAPI()



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://frontend-api-rune-voetbal.netlify.app"
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = _auth.authenticate_speler(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Add the JWT case sub with the subject(user)
    access_token = _auth.create_access_token(
        data={"sub": user.email}
    )
    #Return the JWT as a bearer token to be placed in the headers
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/voetballers/me", response_model=_schemas.Speler)
def read_voetballer_me(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_speler = _auth.get_current_active_speler(db, token)
    return current_speler

@app.post("/voetballers/", response_model=_schemas.Speler)
def maak_voetballer(speler: _schemas.SpelerCreate, db: Session = Depends(get_db)):
    db_speler = _crud.get_voetballer_by_email(db, email=speler.email)
    if db_speler:
        raise HTTPException(status_code=400, detail="Email already registered")
    return _crud.maak_voetballer(db=db, speler=speler)


@app.get("/voetballers/", response_model=list[_schemas.Speler])
def lees_voetballers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    spelers = _crud.get_voetballers(db, skip=skip, limit=limit)
    return spelers


@app.get("/voetballers/{speler_id}", response_model=_schemas.Speler)
def lees_voetballer(speler_id: int, db: Session = Depends(get_db)):
    db_speler = _crud.get_voetballer(db, speler_id=speler_id)
    if db_speler is None:
        raise HTTPException(status_code=404, detail="Speler niet gevonden")
    return db_speler

@app.put("/voetballers/{speler_id}", response_model=_schemas.Speler)
def update_voetballer(speler_id: int, speler: _schemas.SpelerCreate, db: Session = Depends(get_db)):
    return _crud.update_voetballer(db=db, speler=speler, speler_id=speler_id)

@app.delete("/voetballers/{speler_id}")
def verwijder_voetballer(speler_id: int, db: Session = Depends(get_db)):
    _crud.verwijder_voetballer(db=db, speler_id=speler_id)
    return {"message": f"succesvol verwijderd speler met id: {speler_id}"}

@app.post("/voetballers/{speler_id}/ploeg/", response_model=_schemas.ploeg)
def maak_ploeg_voor_speler(
    speler_id: int, ploeg: _schemas.ploegCreate, db: Session = Depends(get_db)
):
    return _crud.maak_ploeg(db=db, ploeg=ploeg, speler_id=speler_id)


@app.get("/ploeg/", response_model=list[_schemas.ploeg])
def lees_ploeg(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ploeg = _crud.get_ploeg(db, skip=skip, limit=limit)
    return ploeg


@app.delete("/ploeg/{ploeg_id}")
def verwijder_ploeg(ploeg_id: int, db: Session = Depends(get_db)):
    _crud.verwijder_ploeg(db=db, ploeg_id=ploeg_id)
    return {"message": f"succesvol verwijderd ploeg met id: {ploeg_id}"}


