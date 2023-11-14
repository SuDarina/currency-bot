import requests
from bs4 import BeautifulSoup as BS
from data import banks, currencies


def get_banks_currency(bank, currency):
    url = 'https://mainfin.ru/bank/' + banks.get(bank).get('url') + '/currency/' + currencies.get(currency).get('url')
    soup = BS(requests.get(url).text, 'html.parser')
    course = soup.find("span", {"id": "sell_" + currencies.get(currency).get('url')})
    return f"{banks.get(bank).get('rus_spell')} {currencies.get(currency).get('rus_spell')}: {str(course.text)}"
