from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import datetime
import zoneinfo

engine = create_engine("mysql+pymysql://root@localhost:3306/teste_bot")

Base = declarative_base()

_Sessao = sessionmaker(engine)
sess = _Sessao

def datetime_sqlalchemy_to_iso(date: str) -> datetime.datetime:
    """Converte uma data de um registro SQLAlchemy para um datetime python"""
    
    return datetime.datetime.fromisoformat(date)

def now():
    return datetime.datetime.now(datetime.timezone.utc)


def now_br():
    return datetime.datetime.now(zoneinfo.ZoneInfo("America/Sao_Paulo"))



from .Client import Client
from .Appointment import Appointment
from .Admin import Admin
