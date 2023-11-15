import threading
import time

import requests
from bs4 import BeautifulSoup as BS

from data import banks, currencies

rates = {bank: {currency: None for currency in currencies} for bank in banks}


def get_banks_currency(bank, currency, rusBank, rusCurrency):
    if rates is None or rates[bank] is None or rates[bank][currency] is None:
        return f"Курс для банка {bank} с валютой {currency} не удалось получить"
    else:
        return f"{rusBank} {rusCurrency} ({currency}) : {rates[bank][currency]}"


def start_requesting_rates_one_a_day():
    notification_thread = threading.Thread(target=request_banks_rates)
    notification_thread.start()


def request_banks_rates():
    while True:
        for bank in banks:
            for currency in currencies:
                url = 'https://mainfin.ru/bank/' + banks.get(bank).get('url') + '/currency/' + currencies.get(
                    currency).get(
                    'url')
                soup = BS(requests.get(url).text, 'html.parser')
                course = soup.find("span", {"id": "sell_" + currencies.get(currency).get('url')})
                print(
                    f"{banks.get(bank).get('rus_spell')} {currencies.get(currency).get('rus_spell')}: {str(course.text)}")
                rates[bank][currency] = str(course.text)
        print(rates)
        print("INFO - Finished requesting")
        time.sleep(60 * 60 * 24)
