from telebot import types
from app.bot import bot


def return_menu(buttons: types.InlineKeyboardMarkup, previous_menu: str = None):
    "Adiciona o botôes de 'menu inicial'"
    # "Adiciona os botôes de 'menu inicial' e 'menu anterior'"

    buttons.row(types.InlineKeyboardButton("Menu inicial", callback_data="primary_menu"))
    if previous_menu:
        buttons.row(types.InlineKeyboardButton("Menu anterior", callback_data=previous_menu))




import app.bot.callbacks.primary_menu as primary_menu

