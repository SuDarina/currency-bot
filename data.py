from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

token = '5898807077:AAEbDieaAl57Toyi5XnQkp3KlHDKdXvmmDg'

banks_order = ["tinkoff", "vtb", 'sber', 'gazprom', 'alfa']
rus_to_en_banks = {'Тинькофф': 'tinkoff', 'ВТБ': 'vtb', 'СБЕР': 'sber', 'Газпромбанк': 'gazprom', 'Альфа-Банк': 'alfa'}
rus_to_en_currencies = {'Доллар': 'USD', 'Евро': 'EUR'}
banks = {banks_order[0]: {'url': 'tcs', 'rus_spell': 'Тинькофф'},
         banks_order[1]: {'url': 'vtb', 'rus_spell': 'ВТБ'},
         banks_order[2]: {'url': 'sberbank', 'rus_spell': 'СБЕР'},
         banks_order[3]: {'url': 'gazprombank', 'rus_spell': 'Газпромбанк'},
         banks_order[4]: {'url': 'alfabank', 'rus_spell': 'Альфа-Банк'}}
currencies = {'USD': {'url': 'usd', 'rus_spell': 'Доллар (USD)'}, 'EUR': {'url': 'eur', 'rus_spell': 'Евро (EUR)'}}

# inline_kb_banks = InlineKeyboardMarkup(row_width=1).add(
#     InlineKeyboardButton('Тинькофф', callback_data='bank1'),
#     InlineKeyboardButton('ВТБ', callback_data='bank2'),
#     InlineKeyboardButton('СБЕР', callback_data='bank3'),
#     InlineKeyboardButton('Газпромбанк', callback_data='bank4'),
#     InlineKeyboardButton('Альфа-Банк', callback_data='bank5'),
#     InlineKeyboardButton('Остановить выбор', callback_data='bank6'))
#
# inline_kb_currencies = InlineKeyboardMarkup(row_width=1).add(
#     InlineKeyboardButton('Доллар', callback_data='cur1'),
#     InlineKeyboardButton('Евро', callback_data='cur2'),
#     InlineKeyboardButton('Остановить выбор', callback_data='cur3'))
