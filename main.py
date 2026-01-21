import telebot
from telebot import types
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('BOT_TOKEN')
if not token:
    raise ValueError("BOT_TOKEN not found in environment variables")
bot = telebot.TeleBot(token)



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: types.Message):
    # bot.reply_to(message, "Bem vindo ao Nutribot! Envie o que você comeu hoje por áudio e eu te darei as informações nutricionais.")
    bot.reply_to(message, "Welcome to Nutribot! Send me a voice message describing what you ate today, and I'll provide you with the nutritional information.")

@bot.message_handler(content_types=['voice'])
def handle_voice(message: types.Message):

    bot.reply_to(message, "Áudio recebido! Processando... (Funcionalidade em desenvolvimento)")

bot.infinity_polling()
