from fastapi import FastAPI

from madr.routers import romancistas

app = FastAPI()
app.include_router(romancistas.router)
