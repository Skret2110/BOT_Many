import telebot
from extensions import APIException, ManyConverter
from config import TOKEN, keys

bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Команда /start - инструкция по конвертации. Команда /values - список доступных для обмена валют'
    bot.reply_to(message, text)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = ""'Для получения информации о валюте, введите запрос в следующем формате:\n1. название валюты.' \
           ' 2. Название Валюты в которую надо произвести конвертацию. ' \
           '3. Сумму конвертации'""
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Дступны валюты:"
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message,):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException("Введите только 3 параметра: 2 валюты и кол-во")

        quote, base, amount = values
        save = ManyConverter.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя!\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду!\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {save}'
        bot.send_message(message.chat.id, text)


bot.polling()
