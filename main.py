from controller import telegram_bot
from data import token
from database_work import drop_notifications
from rf_bank_api import start_requesting_rates_one_a_day

if __name__ == '__main__':
    # drop_notifications before start
    drop_notifications()
    # request rates one time per day
    start_requesting_rates_one_a_day()

    telegram_bot(token)
