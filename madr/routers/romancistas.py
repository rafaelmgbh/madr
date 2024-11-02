from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Romancista
from madr.schemas import (
    Mensagem,
    RomancistaList,
    RomancistaPublic,
    RomancistaSchema,
)

router = APIRouter(prefix="/romancistas", tags=["Romancistas"])
Session = Annotated[Session, Depends(get_session)]


@router.post(
    "/", status_code=HTTPStatus.CREATED, response_model=RomancistaPublic
)
def create_romancista(romancista: RomancistaSchema, session: Session):
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
def read_romancista(session: Session):
    romancistas = session.scalars(select(Romancista)).all()
    return {"romancistas": romancistas}


@router.delete("/{romancista_id}", response_model=Mensagem)
def delete_romancista(romancista_id: int, session: Session):
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
