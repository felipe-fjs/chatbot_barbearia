from . import Base, sess
from sqlalchemy import Column, Integer, BigInteger


class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger, unique=True)

def get_admin() -> Admin:
    with sess() as conn:
        admin = conn.query(Admin).all()
    
    return admin[0]

