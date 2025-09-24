from . import Base
from app.model import sess
from telebot import types
from sqlalchemy import Column, Integer, String, BigInteger


class Client(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=True)
    chat_id = Column(BigInteger, nullable=False, unique=True)


def register_client(message: types.Message):
    with sess() as conn:
        client = conn.query(Client).filter_by(chat_id=message.chat.id).first() 
        if client == None:
            client = Client()
            client.name = None
            client.chat_id = message.chat.id
            conn.add(client)
            conn.commit()
            return
        
def get_client(chat_id: int) -> Client:
    with sess() as conn:
        client = conn.query(Client).filter(Client.chat_id == chat_id).first()

    return client
