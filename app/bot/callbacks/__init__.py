from telebot import types
from app.bot import bot


def return_menu(buttons: types.InlineKeyboardMarkup, call: types.CallbackQuery):
    "Adiciona o botôes de 'menu inicial'"
    # "Adiciona os botôes de 'menu inicial' e 'menu anterior'"

    buttons.row(types.InlineKeyboardButton("Menu inicial", callback_data="primary_menu"))
    # buttons.row(types.InlineKeyboardButton("Menu anterior", callback_data=call.data))

def delete_message(call: types.CallbackQuery):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


import app.bot.callbacks.primary_menu as primary_menu

