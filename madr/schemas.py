from pydantic import BaseModel


class RomancistaSchema(BaseModel):
    nome: str


class RomancistaPublic(BaseModel):
    id: int
    nome: str
