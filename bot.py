# для видалення повідомлення
import asyncio
from contextlib import suppress
from aiogram import types
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound  #

from config import *
from aiogram.utils import executor
from aiogram.types import Message
from aiogram.dispatcher import Dispatcher
import openai, aiogram, time, os

openai.api_key = os.getenv('OPENAITOKEN')  # paste your openai token here
bot = aiogram.Bot(token=os.getenv('TOKEN'))  # paste your bot token here
dp = Dispatcher(bot)


async def delete_message(message: types.Message):
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


async def ChatGPT(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{text}",
        temperature=0.1,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
    )['choices'][0]['text']
    check_first_sumvol(response)
    write_log(response)
    pprint(response)

    return response


@dp.message_handler(commands=['start'])
async def start(message: Message):
    if message.from_user.id == ADMIN:
        start = f'{message.chat.full_name} Вітаю в Адмін Панелі! Виберіть дію на клавіатурі'

        await message.answer(start, reply_markup=kb)

    else:
        text = f"Вітаю на сторінці бота!\n{message.chat.full_name}Надсилайте текстові запити та чекайте на відповідь"

        await message.answer(text)


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    text = (
        'Список команд:', '/start - Почати діалог', '/help - Список команд',
        '/img [prompts] - Фото по ключовим словам\nПриклад: /img cute white cat, rtx, hd, 4k'
    )
    await message.answer('\n'.join(text))


@dp.message_handler(commands=['off_pc'])
async def off_pc(message: Message):
    await message.answer('Вимкнення ПК')
    print('>> Вимкнення ПК')
    os.system('shutdown /p')


@dp.message_handler(commands=['img', 'img:', 'image'])
async def image_prompts(message: types.Message):
    prompts = message.get_args()

    write_log(f'\n[{message.from_user.full_name}]: \n{prompts}')
    print(f'\n[{message.from_user.full_name}]: \n{prompts}')

    temp = await message.answer(f'Генерую фото [{SIZE_PHOTO}] [{prompts}]...')
    response = openai.Image.create(prompt=prompts, n=1, size=SIZE_PHOTO)
    image_url = response['data'][0]['url']

    await asyncio.create_task(delete_message(temp))  # delete temp
    write_log(f'\n[{message.from_user.full_name}]: {image_url}')
    pprint(f'\n{image_url}')
    await message.answer(image_url)


@dp.message_handler()
async def message_to_openai(message: Message):
    write_log(f'\n\n[{message.from_user.full_name}]: {message.text}')
    print(f'[{message.from_user.full_name}]<< {message.text}')

    temp = await message.answer('Генерую відповідь...')
    response = await ChatGPT(message.text)  # output text
    await asyncio.create_task(delete_message(temp))  # delete temp

    await message.answer(response)


if __name__ == '__main__':
    while True:
        print('>> Bot started')
        try:
            executor.start_polling(dp, skip_updates=False)
        except aiogram.utils.exceptions.NetworkError:
            print(
                f'>> NetworkError - Перепідключення через {RESTART_TIME} секунд '
            )
            time.sleep(RESTART_TIME)
        except openai.error.InvalidRequestError:
            print('>> AI Error ' + str(openai.error.InvalidRequestError))
        except asyncio.exceptions.TimeoutError:
            print('>> TimeoutError ' + str(asyncio.exceptions.TimeoutError))
            time.sleep(2)
