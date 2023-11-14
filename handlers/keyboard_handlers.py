from telebot import types

from data import banks_order, banks
from keyboards import kb_currencies, kb_banks


def banks_handler(bot):
    l = []

    @bot.callback_query_handler(func=lambda call: call.data and call.data.startswith('bank'))
    def process_callback_bank(callback_query: types.CallbackQuery):
        code = callback_query.data[-1]
        if code != str(6):
            if l.__contains__(banks.get(banks_order[int(code) - 1]).get('rus_spell')) == 0:
                l.append(banks.get(banks_order[int(code) - 1]).get('rus_spell'))
            print(banks.get(banks_order[int(code) - 1]).get('rus_spell'))
            bot.answer_callback_query(callback_query.id, text="Выбрано: " +
                                                              str(banks.get(banks_order[int(code) - 1]).get(
                                                                  'rus_spell')))
        else:
            bot.send_message(callback_query.from_user.id, text=f"Выбранные банки: {print_banks(l)}")
            bot.send_message(callback_query.from_user.id, text="Выбор валюты", reply_markup=inline_kb_currencies)


def print_banks(l):
    s = ''
    for i in l:
        s += f"{i}, "
    return s[:-2]
