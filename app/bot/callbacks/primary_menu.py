from app.bot import delete_message
from app.bot.handlers import start
from app.bot.callbacks import return_menu
from app.bot import bot
from telebot import types


week_days = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

def haircuts(call: types.CallbackQuery):
    delete_message(call.message)

    buttons = types.InlineKeyboardMarkup()
    return_menu(buttons, call)

    text = "Cortes de cabelo disponíveis: \n1. Degradê, R$ 20.00\n2. Social, R$ 15.00\n3. Mullet R$ 30.00"

    bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=buttons)

def socialmedia(call: types.CallbackQuery):
    delete_message(call.message)

    chat_id = call.message.chat.id
    message_id = call.message.message_id

    buttons = types.InlineKeyboardMarkup()

    wpp = types.InlineKeyboardButton(text="Whatsapp", callback_data="wpp")
    insta = types.InlineKeyboardButton(text="Instagram", callback_data="insta")

    buttons.row(wpp)
    buttons.row(insta)
    return_menu(buttons, call)
    
    text:str = "Minha mídias sociais são:"

    delete_message(call)
    bot.send_message(chat_id=chat_id, text=text, reply_markup=buttons)

def primary_menu(call: types.CallbackQuery):
    match call.data:
        case "haircuts":
            print("haircuts")
            haircuts(call)
        
        case "socialmedia":
            print("wpp")
            socialmedia(call)
        
        case "primary_menu":
            start(call.message)

bot.register_callback_query_handler(callback=primary_menu, func=lambda call: not call.data.startswith("appoint"))
