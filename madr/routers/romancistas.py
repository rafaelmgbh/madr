from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Romancista, User
from madr.schemas import (
    Mensagem,
    RomancistaList,
    RomancistaPublic,
    RomancistaSchema,
)
from madr.security import get_current_user

router = APIRouter(prefix="/romancistas", tags=["Romancistas"])
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    "/", status_code=HTTPStatus.CREATED, response_model=RomancistaPublic
)
def create_romancista(
    romancista: RomancistaSchema, user: CurrentUser, session: Session
):
    romacista_db = session.scalar(
        select(Romancista).where(Romancista.nome == romancista.nome)
    )
    if romacista_db:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Romancista already exists",
        )
    else:
        romacista_db = Romancista(
            nome=romancista.nome,
        )
        session.add(romacista_db)
        session.commit()
        session.refresh(romacista_db)

    return romacista_db


@router.get("/", response_model=RomancistaList)
def read_romancista(session: Session, user: CurrentUser):
    romancistas = session.scalars(select(Romancista)).all()
    return {"romancistas": romancistas}


@router.delete("/{romancista_id}", response_model=Mensagem)
def delete_romancista(romancista_id: int, session: Session, user: CurrentUser):
    romancista = session.scalar(
        select(Romancista).where(Romancista.id == romancista_id)
    )
    if not romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Romancista não encontrado",
        )
    session.delete(romancista)
    session.commit()
    return {"mensagem": "Romancista excluído com sucesso."}


@router.patch("/{romancista_id}", response_model=RomancistaPublic)
def patch_romancista(
    romancista_id: int,
    session: Session,
    user: CurrentUser,
    romancista: RomancistaSchema,
):
    romancista_db = session.scalar(
        select(Romancista).where(Romancista.id == romancista_id)
    )
    if not romancista_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Romancista não encontrado.",
        )
    romancista_db.nome = romancista.nome
    session.commit()
    session.refresh(romancista_db)
    return romancista_db
