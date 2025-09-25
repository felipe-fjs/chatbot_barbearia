from CONFIG import TOKEN

import telebot


bot = telebot.TeleBot(token=TOKEN, )

def delete_message(message: telebot.types.Message):
    if message.message_id:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

import app.bot.handlers as handlers
bot.add_message_handler(handlers)


import app.bot.callbacks.appointments as appointment
import app.bot.callbacks.primary_menu as primary_menu

bot.add_callback_query_handler(appointment)
bot.add_callback_query_handler(primary_menu)
