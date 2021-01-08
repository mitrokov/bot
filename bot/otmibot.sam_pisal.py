
#Бот для телеграмм делаю первый раз
# уроки брал отсюда https://youtu.be/M8fhrtvedHA
# и отсюда https://habr.com/ru/post/442800/
# интересно https://habr.com/ru/post/462333/


import telebot
import config
import random

from telebot import types

bot = telebot.TeleBot (config.TOKEN) # config.py

@bot.message_handler (commands = ['start'])
def welcome (message):
    sti = open ("img/welcome.tgs", "rb")
    bot.send_sticker(message.chat.id, sti)
    
    #keyboard
    markup = types.ReplyKeyboardMarkup (resize_keyboard = True)
    item1 = types.KeyboardButton("Рандомное число")
    item2 = types.KeyboardButton("Как дела")

    markup.add (item1, item2)

    bot.send_message (message.chat.id,"Welcome, {0.first_name}! \n Я - <b>{1.first_name}</b> бот создан чтобы быть подопытным кроликом \n Я еще практически ничего не умею, но мой создатель работает надо мной и надеюсь в скором времени я обрету много полезных навыков!".format(message.from_user, bot.get_me()), parse_mode = 'html', reply_markup = markup)

@bot.message_handler (content_types = ['text'])
def lalala (message):
    if message.chat.type == 'private':
        if message.text == 'Рандомное число':
            bot.send_message (message.chat.id, str (random.randint(0, 100)))
        elif message.text == 'Как дела ?':

            markup = types.InlineKeyboardMarkup (row_width = 3)
            item1 = types.InlineKeyboardButton ("Хорошо", callback_data = 'good')
            item2 = types.InlineKeyboardButton ("Не очень", callback_data = 'bad')

            markup.add (item1, item2)
            
            bot.send_message (message.chat.id, 'Отлично, а у тебя как?', reply_markup = markup)
        else:
            bot.send_message (message.chat.id, 'Извините я не знаю что ответить')

@bot.callback_query_handler (func = lambda call: True)
def callback_inline (call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message (call.message.chat.id, 'Вот и отличненько')
            elif call.data == 'bad':
                bot.send_message (call.message.chat.id, 'Ничего бывает')

            # remove inline buttons
            bot.edit_message_text (chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Как дела?", 
                    reply_markup = None) 

            #show alert
            bot.answer_callback_query (callback_query_id = call.id, show_alert = False, 
                    text = "Это тестовое уведомление!")

    except Exception as e:
       print (repr (e))

bot.polling (none_stop = True, interval=0)
