import os, sys, openai

openai.api_key = os.getenv('OPENAITOKEN')  # paste your openai token here
print('Введіть ваш запит (exit - вийти)')


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


while True:
    text = input('>> ')  # your text

    if text == 'exit':
        sys.exit()

    responce = ChatGPT(text)

    text = responce['choices'][0]['text']  # openai text
    print(text)