import requests, urllib.parse, json, re
from random import *
from telegram import *
from telegram.ext import *
from googletrans import Translator


BOT_TOKEN = 'API_TELEGRAM_TOKEN'

alp = ['а', 'б', 'в', 'г',
       'д', 'е', 'ё', 'ж',
       'з', 'и', 'й', 'к',
       'л', 'м', 'н', 'о',
       'п', 'р', 'с', 'т',
       'у', 'ф', 'х', 'ц',
       'ч', 'ш', 'щ', 'ъ',
       'ы', 'ь', 'э', 'ю', 'я', ' ', ' ']

sizes = [8, 12]


def generate_text(isq=False, nmin=120, nmax=150):
    num = randint(nmin, nmax)
    if isq:
        if '?' not in alp:
            alp.append('?')
            alp.append('?')
    else:
        if '?' in alp:
            alp.remove('?')
            alp.remove('?')
    text = ''
    for i in range(num):
        text += choice(alp)
    return text


def start(bot, update):
    update.message.reply_text('Мы смотрим на глупость с вами, и давайте поговорим о том, как ее получить'
                                + ' чтобы получить утвердительное сообщение отправьте /say'
                                + ' чтобы получить вопросительное – ask')

def ask(bot, update):
    is_correct = False
    result = ''
    while not is_correct:
        is_correct = True
        result = translator.translate(generate_text(True), src='lb', dest='ru').text
        if len(re.findall('[a-zA-Z]', result)) == 0 and '?' in result:
            for i in re.findall(r"[\w']+", result):
                if len(i) > 20:
                    is_correct = False
                    print('denied:\n' + result)
        else:
            print('denied:\n' + result)
            is_correct = False
    update.message.reply_text('*Моя думать:*\n%s' % result.capitalize(), parse_mode='Markdown')


def say(bot, update):
    is_correct = False
    result = ''
    while not is_correct:
        is_correct = True
        result = translator.translate(generate_text(), src='lb', dest='ru').text
        if len(re.findall('[a-zA-Z]', result)) == 0:
            for i in re.findall(r"[\w']+", result):
                if len(i) > 20:
                    is_correct = False
                    print('denied:\n' + result)
        else:
            print('denied:\n' + result)
            is_correct = False
    update.message.reply_text('*Моя думать:*\n%s' % result.capitalize(), parse_mode='Markdown')


def message(bot, update):
    reg_en = re.compile('say', re.IGNORECASE)
    if len(reg_en.findall(update.message.text)):
        update.message.reply_text('Moya spasibo tvoya. Moya i vpravdu say.')


def error(bot, update, error):
    print('Update "%s" caused an error "%s"' % (update, error))


translator = Translator()
updater = Updater(BOT_TOKEN)
dp = updater.dispatcher

dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('say', say))
dp.add_handler(CommandHandler('ask', ask))

dp.add_handler(MessageHandler(Filters.text, message))

dp.add_error_handler(error)

updater.start_polling()
updater.idle()
