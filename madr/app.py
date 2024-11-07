from fastapi import FastAPI

from madr.routers import auth, contas, livros, romancistas

app = FastAPI()
app.include_router(romancistas.router)
app.include_router(contas.router)
app.include_router(auth.router)
app.include_router(livros.router)
