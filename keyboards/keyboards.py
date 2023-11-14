from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

kb_configure = ReplyKeyboardMarkup(row_width=1).add(
    KeyboardButton("Выбрать банки"),
    KeyboardButton("Выбрать валюты"),
    KeyboardButton("Закрыть"))

kb_banks = ReplyKeyboardMarkup(row_width=1).add(
    KeyboardButton('Тинькофф'),
    KeyboardButton('ВТБ'),
    KeyboardButton('СБЕР'),
    KeyboardButton('Газпромбанк'),
    KeyboardButton('Альфа-Банк'),
    KeyboardButton('Закрыть'))

kb_currencies = ReplyKeyboardMarkup(row_width=1).add(
    KeyboardButton('Доллар'),
    KeyboardButton('Евро'),
    KeyboardButton('Закрыть'))
