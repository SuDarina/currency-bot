import threading
from datetime import datetime
import time
from telebot import types

from rf_bank_api import get_banks_currency
from keyboards import kb_banks, kb_currencies, kb_configure
from database_work import add_banks, add_currencies, get_currencies, get_banks, form_gist, update_notify, get_notify
from data import banks, currencies, rus_to_en_banks, rus_to_en_currencies

import telebot
import requests


def send_daily_notifications(user_id, bot):
    while True:
        if get_notify(user_id)[0]:
            banks_list = get_banks(user_id)[0]
            currencies_list = get_currencies(user_id)[0]

            for bank in banks_list:
                for currency in currencies_list:
                    message_text = get_banks_currency(rus_to_en_banks.get(bank), rus_to_en_currencies.get(currency), bank, currency)
                    bot.send_message(user_id, text=message_text)

            time.sleep(24 * 60 * 60)
        else:
            time.sleep(60)


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, "Чтобы узнать о возможностях бота, введите команду /help")

    @bot.message_handler(commands=["help"])
    def start_message(message):
        bot.send_message(message.chat.id,
                         "/help - помощь \n/configure - выбор валют и банков \n/notifyOn - включить ежедневные уведомления\n"
                         "/notifyOff - выключить ежедневные уведомления\n"
                         "/get - получить сводку по выбранным валютам и банкам \n/location - получить ближайшие банки")

    @bot.message_handler(commands=["get"])
    def start_message(message):
        send_notify(message)

    @bot.message_handler(commands=['location'])
    def send_location(message):
        request = bot.send_message(message.chat.id, "Пожалуйста, отправьте свою текущую геолокацию")
        bot.register_next_step_handler(request, process_location)

    def process_location(message):
        if message.location:
            user_id = message.chat.id
            latitude = message.location.latitude
            longitude = message.location.longitude
            bank_names = sum(list(get_banks(user_id)), [])

            geocoder_url = "https://search-maps.yandex.ru/v1/"

            if bank_names is None:
                params = {
                    "apikey": "cd3ab8da-15f6-4feb-83ac-c13e22eb2c24",
                    "format": "json",
                    "text": "обмен валют",
                    "lang": "ru_RU",
                    "ll": f"{longitude},{latitude}",
                    "spn": "0.02, 0.02",
                    "results": 5
                }
                response = requests.get(geocoder_url, params=params).json()
                resultBanks = response['features']

                bank_adresses = []
                bank_longitude = []
                bank_latitude = []
                for address in resultBanks:
                    bank_adresses.append(address['properties']['CompanyMetaData']['address'])
                    bank_longitude.append(address['geometry']['coordinates'][0])
                    bank_latitude.append(address['geometry']['coordinates'][1])

                formatted_message = "Ближайшие отделения банков находятся: \n\n" + "\n".join(bank_adresses)
                bot.send_message(message.chat.id, formatted_message, parse_mode='HTML')

                for item in range(len(bank_longitude)):
                    bot.send_location(message.chat.id, latitude=bank_latitude[item], longitude=bank_longitude[item])
            else:
                for bank_name in bank_names:
                    params = {
                        "apikey": "cd3ab8da-15f6-4feb-83ac-c13e22eb2c24",
                        "format": "json",
                        "text": f"обмен валют, {bank_name}",
                        "lang": "ru_RU",
                        "ll": f"{longitude},{latitude}",
                        "spn": "0.02, 0.02",
                        "results": 1
                    }
                    response = requests.get(geocoder_url, params=params).json()
                    if response is not None:
                        resultBanks = response['features'][0]

                        bank_adresses = resultBanks['properties']['CompanyMetaData']['address']
                        bank_longitude = resultBanks['geometry']['coordinates'][0]
                        bank_latitude = resultBanks['geometry']['coordinates'][1]

                        formatted_message = f"Ближайшее отделение банка {bank_name} находится: \n\n" + f"\n{bank_adresses}"
                        bot.send_message(message.chat.id, formatted_message, parse_mode='HTML')
                        bot.send_location(message.chat.id, latitude=bank_latitude, longitude=bank_longitude)
        else:
            bot.send_message(message.chat.id, "К сожалению, не удалось получить вашу геолокацию")

    @bot.message_handler(commands=['configure'])
    def start_message(message: types.Message):
        response = bot.send_message(message.chat.id, text="Выберите из списка:", reply_markup=kb_configure)
        d = {'c': [], 'l': []}
        bot.register_next_step_handler(response, choose_option, d)

    @bot.message_handler(commands=["notifyOn"])
    def enable_notifications(message):
        user_id = message.chat.id
        if get_notify(user_id) is None:
            bot.send_message(user_id, "Банки или валюты не выбраны!")
            return
        if not get_notify(user_id)[0]:
            update_notify(user_id, True)
            bot.send_message(user_id, "Ежедневные уведомления включены!")

            notification_thread = threading.Thread(target=send_daily_notifications, args=(user_id, bot))
            notification_thread.start()
        else:
            bot.send_message(user_id, "Ежедневные уведомления уже включены!")

    @bot.message_handler(commands=["notifyOff"])
    def disable_notifications(message):
        user_id = message.chat.id
        update_notify(user_id, False)
        bot.send_message(user_id, "Ежедневные уведомления выключены!")

    def choose_option(message, d):
        if message.text == 'Выбрать банки':
            response = bot.send_message(message.chat.id, text="Выберите банки:", reply_markup=kb_banks)
            bot.register_next_step_handler(response, choose_banks, d)
        if message.text == 'Выбрать валюты':
            response = bot.send_message(message.chat.id, text="Выберите валюты:", reply_markup=kb_currencies)
            bot.register_next_step_handler(response, choose_currency, d)
        if message.text == 'Закрыть':
            bot.send_message(message.chat.id, text=f"Изменения сохранены.\nТекущие настройки:\nБанки:{d.get('l')}\n"
                                                   f"Валюты: {d.get('c')}", reply_markup=types.ReplyKeyboardRemove())

    def choose_banks(message, d):
        if message.text != "Закрыть":
            for bank in banks:
                if message.text == banks.get(bank).get("rus_spell"):
                    append_banks(d.get('l'), message)
                    break
            message = bot.send_message(message.chat.id, text="Выберите банки:", reply_markup=kb_banks)
            bot.register_next_step_handler(message, choose_banks, d)
        else:
            if d.get('l') is not None:
                add_banks(message.chat.id, d.get('l'))
            message = bot.send_message(message.chat.id, text=f"Выбранные банки: {d.get('l')}. Сохранено!",
                                       reply_markup=kb_configure)
            bot.register_next_step_handler(message, choose_option, d)

    def append_banks(l, message):
        if not l.__contains__(message.text):
            l.append(message.text)
        return bot.send_message(message.chat.id, text=f"Выбранные банки: {l}. Выберите банки:",
                                reply_markup=kb_banks)

    def append_currencies(c, message):
        if not c.__contains__(message.text):
            c.append(message.text)
        return bot.send_message(message.chat.id, text=f"Выбранные валюты: {c}. Выберите валюты:",
                                reply_markup=kb_currencies)

    def choose_currency(message, d):
        if message.text != "Закрыть":
            for cur in currencies:
                print()
                if (message.text + " (EUR)" == currencies.get(cur).get("rus_spell")) or \
                        (message.text + " (USD)" == currencies.get(cur).get("rus_spell")):
                    append_currencies(d.get('c'), message)
                    break
            message = bot.send_message(message.chat.id, text="Выберите валюты:", reply_markup=kb_currencies)
            bot.register_next_step_handler(message, choose_currency, d)
        else:
            if d.get('c') is not None:
                add_currencies(message.chat.id, d.get('c'))
            bot.send_message(message.chat.id, text=f"Выбранные валюты: {d.get('c')}. Сохранено!",
                             reply_markup=kb_configure)
            bot.register_next_step_handler(message, choose_option, d)

    @bot.message_handler(commands=['show'])
    def start_message(message: types.Message):
        user_id = message.chat.id
        bot.send_message(message.chat.id, text=f"Текущие настройки:\n Банки:{get_banks(user_id)}\n"
                                               f"Валюты: {get_currencies(user_id)}")

    def send_notify(message):
        bot.send_message(message.chat.id, text=str(datetime.now()))
        user_id = message.chat.id
        for bank in get_banks(user_id)[0]:
            for curr in get_currencies(user_id)[0]:
                bot.send_message(message.chat.id,
                                 text=get_banks_currency(rus_to_en_banks.get(bank), rus_to_en_currencies.get(curr), bank, curr))

    bot.polling()
