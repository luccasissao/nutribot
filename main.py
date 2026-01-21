import telebot
from telebot import types
from dotenv import load_dotenv
import os
from tg_audio2text import telegram_audio_to_text

load_dotenv()
token = os.getenv('BOT_TOKEN')
if not token:
    raise ValueError("BOT_TOKEN not found in environment variables")
bot = telebot.TeleBot(token)

# def speech_to_text(audio_bytes):
#     """
#     Transcribes audio bytes using Whisper large model optimized for Portuguese.

#     Args:
#         audio_bytes (bytes): The audio file content as bytes.

#     Returns:
#         str: The transcribed text in Portuguese.
#     """
#     # Load Whisper large model for better accuracy
#     pipe = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3")

#     # Load audio from bytes using librosa
#     audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)

#     # Transcribe with Portuguese language specification
#     result = pipe(audio, generate_kwargs={"language": "portuguese"})

#     return result["text"]

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: types.Message):
    # bot.reply_to(message, "Bem vindo ao Nutribot! Envie o que você comeu hoje por áudio e eu te darei as informações nutricionais.")
    bot.reply_to(message, "Welcome to Nutribot! Send me a voice message describing what you ate today, and I'll provide you with the nutritional information.")

# @bot.message_handler(content_types=['voice'])
# def handle_voice(message: types.Message):
#     try:
#         # Get file info
#         file_info = bot.get_file(message.voice.file_id)
#         # Download audio as bytes
#         audio_bytes = bot.download_file(file_info.file_path)
#         # Transcribe
#         transcription = speech_to_text(audio_bytes)
#         # Reply with transcription
#         bot.reply_to(message, f"Transcrição: {transcription}")
#     except Exception as e:
#         bot.reply_to(message, f"Erro ao processar áudio: {str(e)}")

@bot.message_handler(content_types=['voice', 'audio'])
def handle_audio(message):
    try:
        text = telegram_audio_to_text(bot, message)
        bot.reply_to(message, f"📝 Transcrição:\n{text}")
    except Exception as e:
        bot.reply_to(message, "❌ Erro ao processar o áudio.")
        print(e)


bot.infinity_polling()
