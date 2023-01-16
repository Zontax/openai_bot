from aiogram import types

ADMIN = 1059897340
RESTART_TIME = 5
TEMPERATURE = 0.1
SIZE_PHOTO = '1024x1024'

# Адмін кнопки
kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(types.InlineKeyboardButton(text='Що ти вмієш?'))


def check_first_sumvol(text):
    if text[0] == '\n' or text[0] == '?' or text[0] == ',' or text[
            0] == '.' or text[0] == '/' or text[0] == ' ':
        text = text[1:]
    return text


def write_log(text):
    file = open('logs.txt', 'a', encoding='windows-1251', errors='replace')
    file.write(text)


def pprint(text):
    print(f'[ChatGPT]>> {text}')
