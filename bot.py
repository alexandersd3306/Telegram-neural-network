import telebot
from telebot import types # для указание типов
import requests
import Nero 
import constant
import openai
import random

API_TOKEN = "5831159696:AAH78salcvKAOFTSn5hx40Rfo8dxTQ9bh_w"
bot = telebot.TeleBot(API_TOKEN)

openai.api_key = "" #Подключаемся к api для работы с диалоговым модулем через GPT


buffer1 = {}


@bot.message_handler(commands=['start']) # Приветственная надпись
def hello(message):
    if buffer1.get(message.from_user.id) == message.text: #буфферная переменная для того что бы несколько раз не смогли отправить сообщение 
        return 
    buffer1[message.from_user.id] = message.text
    bot.send_message(message.chat.id, 'Привет, {name}. Рад тебя видеть'.format(name=message.from_user.username))
    return message

@bot.message_handler(content_types=['text']) #стандартные фразы
def send_text(message):
    if buffer1.get(message.from_user.id) == message.text:
        return 
    buffer1[message.from_user.id] = message.text
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, хозяин')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай, хозяин')
    elif message.text.lower() == 'спасибо':
        bot.send_message(message.chat.id, 'Спасибо и вам что пользуетесь данным ботом')
    elif message.text.lower() == 'я тебя люблю':
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEIXdFkJB33xAbvk3TOrzDRIjc4wFSdggACPwADUomRIz5Sax_F0SlrLwQ')
    elif message.text.lower() == "поговорим?":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)
        btn1 = types.KeyboardButton("Как меня зовут?")
        btn2 = types.KeyboardButton("Что ты можешь?")
        markup.add(btn1, btn2)
    elif message.text.lower() == "как меня зовут?":
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEIXc9kJB3QZrGu7JwtoT3ScsHbLrp-iAACDgMAAm2wQgMXWqCVVdoCpi8E')
    elif message.text.lower() == "что ты можешь?" or message.text.lower() == "что ты можешь":
        x = bot.send_message(message.chat.id, 'Напишите мне любой вопрос')
        bot.register_next_step_handler(x, handl_message)
    else:
        bot.send_message(message.chat.id, 'Напиши что то другое')

@bot.message_handler(content_types=['text']) # Обработчик входящих сообщений    chatgpt подкл
def handl_message(message):
    if buffer1.get(message.from_user.id) == message.text:
        return 
    buffer1[message.from_user.id] = message.text
    msg = bot.send_message(message.chat.id, "Генерирую ответ...")
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=message.text,
      temperature=0.7,
      max_tokens=2048,
      top_p=0.7,
      n=1,
      stop=None,
      timeout=15,
      frequency_penalty=0.0)
    bot.delete_message(message.chat.id, msg.message_id) 
    message = bot.send_message(message.chat.id, text=response['choices'][0]['text'])

@bot.message_handler(content_types=['photo']) #Обработка фото через Nero(отпредениение кошка собака)
def processPhotoMessage(message):
    file = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file.file_path)
    path=str(random.randint(1,1000))+'.jpg'
    with open(path, 'wb') as new_file:
        new_file.write(downloaded_file)
    result = Nero.classify(path)
    bot.send_message(message.chat.id,result)

bot.infinity_polling()
