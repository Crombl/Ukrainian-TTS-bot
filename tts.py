from gtts import gTTS
import io
# from langdetect import detect
from headphones_play import headphones_play
from EMOJI_LIB import replace_emojis

# def detect_alphabet(text):
#     # # Діапазони символів для кирилиці та латиниці
#     # cyrillic_range = (0x0400, 0x04FF)  # Діапазон символів кирилиці
#     # latin_range = (0x0041, 0x007A)    # Діапазон латинських букв (A-Z, a-z)

#     # # Перевірка символів в тексті
#     # for char in text:
#     #     if cyrillic_range[0] <= ord(char) <= cyrillic_range[1]:
#     #         return "uk"
#     #     elif latin_range[0] <= ord(char) <= latin_range[1] or \
#     #          latin_range[0] <= ord(char) <= latin_range[1] + 32:  # Додаємо латинські малі букви
#     #         return "en"
        
#     return "uk"


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