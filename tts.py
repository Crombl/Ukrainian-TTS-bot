from gtts import gTTS
import io
from EMOJI_LIB import replace_emojis


def get_speech(text):

    text = replace_emojis(text)
    tts = gTTS(text=text, lang="uk")
    
    # Створення байтового потоку для зберігання аудіо
    audio_fp = io.BytesIO()
    
    # Запис аудіо в байтовий потік
    tts.write_to_fp(audio_fp)
    
    # Повернення до початку потоку
    audio_fp.seek(0)
    
    return audio_fp


if __name__ == "__main__":
    headphones_play(get_speech("Привіт, Мявчику. Я, нарешті, закінчив роботу над цією програмою."), 0.1)
