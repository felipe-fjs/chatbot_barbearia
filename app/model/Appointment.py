from . import Base, now_br
from app.model import sess
from app.model.Client import get_client
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from datetime import timedelta
from typing import List

import datetime
import zoneinfo
import enum


class AppointmentStatus(enum.Enum):
    FREE = "FREE"
    RESERVED = "RESERVED"
    REQUESTED = "REQUESTED"
    CONFIRMED = "CONFIRMED"


class Appointment(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hour: datetime.datetime = Column(DateTime(), nullable=False, unique=True)
    status = Column(Enum(AppointmentStatus), nullable=False, default=AppointmentStatus.FREE)
    

    client_id = Column(ForeignKey("clientes.id", ondelete="SET NULL"), nullable=True, default=None)

    def __init__(self, hour: DateTime):
        self.hour = hour


def get_appointment(appoint_id: int) -> Appointment | None:
    with sess() as conn:
        app = conn.query(Appointment).filter_by(id=appoint_id).first()
        
    return app

def get_client_last_appointment(chat_id: int):
    with sess() as conn:
        appoint = conn.query(Appointment).filter(Appointment.client_id == get_client(chat_id).id).all()
        last_appoint = appoint.pop()
    
    return last_appoint

def update_appointment(appointment: Appointment):
    with sess() as conn:
        conn.merge(appointment)
        conn.commit()

def create_weekly_availability(): 
    """
    Este método será utilizado para a criação da agenda semanal da barbearia.\n
    este método estará registrando datas da semana seguinte no dia de sexta-feira
    """
    hour_teste = (now_br().replace(hour=8, minute=0, second=0, microsecond=0) + timedelta(days=3))
    with sess() as conn:
        if not conn.query(Appointment).filter(Appointment.hour == hour_teste).first():
            hours = list()
            
            now = datetime.datetime.now(zoneinfo.ZoneInfo("America/Sao_Paulo"))
            now = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=2)
            
            for i in range(1, 7):
                now += timedelta(days=1)
                for j in range(8, 19):
                    if j != 12:
                        hour = now + timedelta(hours=j)
                        hours.append(Appointment(hour))


            for hour in hours:
                conn.add(hour)
            conn.commit()
            return
        
        print("Registro da semana já realizado!")

def get_next_week_appointments() -> List[List[Appointment]]:
    appoints: List[List[Appointment]] = [[], [], [], [], [], [], []]
    with sess() as conn:
        week_appointments = conn.query(Appointment).filter(Appointment.hour >= now_br()).all()

    if week_appointments == []:
        return None
    
    for appoint in week_appointments:
        appoints[appoint.hour.weekday()].append(appoint)

    return appoints

def get_free_appointments() ->  List[List[Appointment]] | None:

    appoints = get_next_week_appointments()
    if appoints:
        for appoints_day in appoints:
            for appoint in appoints_day:
                if appoint.status != AppointmentStatus.FREE:
                    appoints[appoint.hour.weekday()].remove(appoint)
        
        return appoints
    
    return None