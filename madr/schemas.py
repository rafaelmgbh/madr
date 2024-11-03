from pydantic import BaseModel, EmailStr, ConfigDict


class RomancistaSchema(BaseModel):
    nome: str


class RomancistaPublic(BaseModel):
    id: int
    nome: str


class RomancistaList(BaseModel):
    romancistas: list[RomancistaPublic]


class Mensagem(BaseModel):
    mensagem: str


class ContaSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class ContaPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class ContaList(BaseModel):
    contas: list[ContaPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
