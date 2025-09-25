from app.bot import bot, delete_message
from app.model.Client import register_client
from telebot import types

from datetime import datetime
from zoneinfo import ZoneInfo
import locale

# datetime.now(ZoneInfo("America/Sao_Paulo"))

locale.setlocale(locale.LC_TIME, "pt_BR.utf-8")

@bot.message_handler(commands=["start"])
def start(message: types.Message):
    print("mensagem nova:", message.chat.id)
    delete_message(message)
    buttons = types.InlineKeyboardMarkup()

    haircut_prices = types.InlineKeyboardButton(text='Cortes de cabelo', callback_data='haircuts')
    appointment = types.InlineKeyboardButton(text='Agendar horário', callback_data='appointments_week')
    my_appointment = types.InlineKeyboardButton(text="Meu agendamento", callback_data="appointments_my")
    socialmedia = types.InlineKeyboardButton(text="Redes Sociais", callback_data="socialmedia")

    buttons.row(haircut_prices)
    buttons.row(my_appointment)
    buttons.row(appointment)
    buttons.row(socialmedia)

    register_client(message)

    time = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%H:%M - %d de %B de %Y")

    text = """💈👊 E aí, irmão! Bem-vindo à Navalha de Prata! ✂️
Aqui você pode:

💇‍♂️Dar uma olhada nos cortes

📅Conferir seu agendamento

⏰Marcar seu horário sem enrolação

📲Colar nas nossas redes sociais pra ficar por dentro

👉 É só escolher escolher uma opção abaixo e garantir o corte na régua!"""
    
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=buttons)
