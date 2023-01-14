from aiogram.utils import executor
from aiogram.types import Message
from aiogram.dispatcher import Dispatcher
import os, openai, aiogram

openai.api_key = os.getenv('OPENAITOKEN')  # paste your openai token here
bot = aiogram.Bot(token=os.getenv('TOKEN'))  # paste your bot token here
dp = Dispatcher(bot)


def pprint(text):
    print(f'[ChatGPT] >> {text}')


def ChatGPT(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{text}",
        temperature=0.5,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
    )
    return response


@dp.message_handler(commands=['start', 'help'])
async def commands(message: Message):
    text = "Вітаю на сторінці бота!\nНадсилайте текстові запити та чекайте на відповідь"
    pprint(text)
    await bot.send_message(message.from_user.id, text)


@dp.message_handler()
async def process_message(message: Message):
    text = message.text  # input text
    print(f'[{message.from_user.full_name}]: {text}')

    response = ChatGPT(text)
    response = response['choices'][0]['text']
    pprint(response)  # output text

    if response[0] == '\n' or response[0] == '?' or response[0] == ',':
        response = response[1:]

    await bot.send_message(message.from_user.id, response)


if __name__ == '__main__':
    pprint('Bot started')
    executor.start_polling(dp, skip_updates=False)
