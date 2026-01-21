import os
import subprocess
import whisper

model = whisper.load_model("base")

def telegram_audio_to_text(bot, message, language="pt"):
    """
    Recebe uma mensagem do Telegram (voice ou audio),
    baixa o áudio, converte para WAV e retorna a transcrição.
    """
    # 1. identificar o tipo de áudio
    if message.voice:
        file_id = message.voice.file_id
        ext = "ogg"
    elif message.audio:
        file_id = message.audio.file_id
        ext = "audio"
    else:
        raise ValueError("Mensagem não contém áudio")

    # 2. baixar arquivo
    file_info = bot.get_file(file_id)
    audio_bytes = bot.download_file(file_info.file_path)

    input_path = f"input_{message.message_id}.{ext}"
    output_path = f"output_{message.message_id}.wav"

    with open(input_path, "wb") as f:
        f.write(audio_bytes)

    # 3. converter para wav (16kHz mono)
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", input_path,
            "-ar", "16000",
            "-ac", "1",
            output_path
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # 4. transcrever
    result = model.transcribe(output_path, language=language)
    text = result["text"]

    # 5. limpeza
    os.remove(input_path)
    os.remove(output_path)

    return text
