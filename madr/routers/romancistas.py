from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Romancista
from madr.schemas import RomancistaPublic, RomancistaSchema

router = APIRouter(prefix="/romancistas", tags=["Romancistas"])
Session = Annotated[Session, Depends(get_session)]


@router.post("/", response_model=RomancistaPublic)
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
