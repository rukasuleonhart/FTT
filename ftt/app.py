from http import HTTPStatus

from fastapi import FastAPI

from ftt.routers import auth, users, blocks, rooms, reservations
from ftt.schemas import Message

app = FastAPI(title="Sistema de Reserva de Sala UniEvangelica")

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(blocks.router)
app.include_router(rooms.router)
app.include_router(reservations.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}