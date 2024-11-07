from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Livro, Romancista, User
from madr.schemas import LivroList, LivroPublic, LivroSchema, Mensagem
from madr.security import get_current_user

router = APIRouter(prefix="/livros", tags=["Livros"])
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/", status_code=HTTPStatus.CREATED, response_model=LivroPublic)
def create_livro(livro: LivroSchema, user: CurrentUser, session: Session):
    livro_db = session.scalar(
        select(Livro).where(Livro.titulo == livro.titulo)
    )
    romancista = session.scalar(
        select(Romancista).where(Romancista.id == livro.romancista_id)
    )

    if not romancista:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Romancista não encontrado",
        )

    if livro_db:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="O Livro informado já existe",
        )
    else:
        livro_db = Livro(
            titulo=livro.titulo,
            romancista_id=livro.romancista_id,
            ano=livro.ano,
        )
        session.add(livro_db)
        session.commit()

        session.refresh(livro_db)
        return livro_db


@router.get("/", response_model=LivroList)
def read_livro(session: Session, user: CurrentUser):
    livros = session.scalars(select(Livro)).all()
    return {"livros": livros}


@router.delete("/{livro_id}", response_model=Mensagem)
def delete_livro(livro_id: int, session: Session, user: CurrentUser):
    livro = session.scalar(select(Livro).where(Livro.id == livro_id))
    if not livro:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Livro não encontrado",
        )
    session.delete(livro)
    session.commit()
    return {"mensagem": "Livro deletado com sucesso"}


@router.put("/{livro_id}", response_model=LivroPublic)
def update_livro(
    livro_id: int, livro: LivroSchema, session: Session, user: CurrentUser
):
    livro_db = session.scalar(select(Livro).where(Livro.id == livro_id))
    if not livro_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Livro não encontrado",
        )

    livro_db.titulo = livro.titulo
    livro_db.romancista_id = livro.romancista_id
    livro_db.ano = livro.ano

    session.commit()
    session.refresh(livro_db)
    return livro_db
