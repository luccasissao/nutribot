import telebot
from telebot import types
from dotenv import load_dotenv
import os
from llm import llm_answer
from tg_audio2text import telegram_audio_to_text



load_dotenv()
token = os.getenv('BOT_TOKEN')
if not token:
    raise ValueError("BOT_TOKEN not found in environment variables")
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: types.Message):
    bot.reply_to(message, "Bem vindo ao Nutribot! Envie o que você comeu hoje por áudio e eu te darei as informações nutricionais")

@bot.message_handler(content_types=['voice', 'audio'])
def handle_audio(message):
    try:
        print("🎧 Áudio recebido")
        # 1. áudio → texto
        text = telegram_audio_to_text(bot, message)

        if not isinstance(text, str):
            bot.reply_to(message, "Não consegui entender o áudio 😕")
            return

        # 2. texto → LLM
        answer = llm_answer(text)
        # answer = "Funcionalidade de LLM desativada temporariamente."
        print("📝 Transcrição:", text)

        # 3. resposta
        bot.reply_to(message, answer)

    except Exception as e:
        bot.reply_to(message, "❌ Erro ao processar o áudio.")
        print(e)

def main():
    print("🤖 Nutribot rodando...")
    bot.infinity_polling(
        timeout=10,
        long_polling_timeout=5
    )

if __name__ == "__main__":
    main()