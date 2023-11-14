import schedule

from controller import telegram_bot
from data import token
import psycopg2
from obj_store_work import upload_to_os
from database_work import get_statistics_banks, get_statistics_currencies, form_gist

if __name__ == '__main__':
    telegram_bot(token)
