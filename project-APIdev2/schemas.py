from pydantic import BaseModel


class ploegBase(BaseModel):
    titels: int
    regio: str
    huidige_positie: int


class ploegCreate(ploegBase):
    titels: int
    regio: str
    huidige_positie: int


class ploeg(ploegBase):
    id: int
    ploeg_id: int

    class Config:
        orm_mode = True


class SpelerBase(BaseModel):
    naam: str
    achternaam: str
    email: str
    hashed_password: str
    leeftijd: int
    nationaliteit: str


class SpelerCreate(SpelerBase):
    naam: str
    achternaam: str
    email: str
    hashed_password: str
    leeftijd: int
    nationaliteit: str


class Speler(SpelerBase):
    id: int
    is_active: bool
    ploegen: list[ploeg] = []

    class Config:
        orm_mode = True