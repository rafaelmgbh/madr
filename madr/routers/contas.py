from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import User
from madr.schemas import ContaList, ContaPublic, ContaSchema
from madr.security import get_current_user, get_password_hash

router = APIRouter(prefix="/contas ", tags=["contas"])
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/", status_code=HTTPStatus.CREATED, response_model=ContaPublic)
def create_conta(conta: ContaSchema, session: Session):
    db_conta = session.scalar(
        select(User).where(
            (User.email == conta.email) | (User.username == conta.username)
        )
    )
    if db_conta:
        if db_conta.email == conta.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="E-mail em uso",
            )
        elif db_conta.username == conta.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Username em uso",
            )

    hashed_password = get_password_hash(conta.password)
    db_conta = User(
        email=conta.email,
        username=conta.username,
        password=hashed_password,
    )

    session.add(db_conta)
    session.commit()
    session.refresh(db_conta)

    return db_conta


@router.get("/", response_model=ContaList)
def read_users(session: Session):
    contas = session.scalars(select(User)).all()
    return {"contas": contas}
