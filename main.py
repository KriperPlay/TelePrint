import os
import telebot
from telebot import types

API_TOKEN = ''

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("PRINT")
    markup.add(btn1)
    bot.send_message(message.chat.id,"Hello, I am bot for printing documents",reply_markup=markup)

@bot.message_handler(content_types=['text','document'])
def text_message(message):
    if message.text == 'PRINT':
        bot.send_message(message.chat.id, "Send me document")
        bot.register_next_step_handler(message,handle_docs)

def handle_docs(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = '' + message.document.file_name + '1'
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        for i in range(len(message.document.file_name)):
            if message.document.file_name[i] == '.':
                point = i
        os.rename(message.document.file_name+'1', f"document{message.document.file_name[point:]}")
        os.system("lprm -")
        os.system(f"lpr document{message.document.file_name[point:]}")
        os.system(f"rm document{message.document.file_name[point:]}")

        bot.reply_to(message, "I print this")
    except Exception as e:
        bot.reply_to(message, e)

bot.infinity_polling(timeout=30,long_polling_timeout=10)
