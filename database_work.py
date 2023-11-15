import psycopg2
import numpy as np
import matplotlib.pyplot as plt
from obj_store_work import upload_to_os

con = psycopg2.connect(
    database="currency_bot",
    user="user",
    password="1234567890",
    host="localhost",
    port="5432"
)
file = 'statistics.png'

# con = psycopg2.connect("""
#         host=rc1b-aoqqjr9x14brcm55.mdb.yandexcloud.net
#         port=6432
#         sslmode=verify-full
#         dbname=db1
#         user=sudarina
#         password=9218683095
#         target_session_attrs=read-write
#     """)

cur = con.cursor()


def add_banks(id, banks):
    cur.execute(f"SELECT id FROM currency_bot_data WHERE id={id}")
    if cur.fetchone() is None:
        cur.execute(
            f"INSERT INTO currency_bot_data (id,banks) VALUES ({id},ARRAY{banks})"
        )
    else:
        cur.execute(
            f"UPDATE currency_bot_data SET banks = ARRAY{banks} WHERE id = {id};"
        )

    # form_gist(file, get_statistics_banks(), get_statistics_currencies())
    # upload_to_os(file)
    con.commit()


def add_currencies(id, currencies):
    cur.execute(f"SELECT id FROM currency_bot_data WHERE id={id}")
    if cur.fetchone() is None:
        cur.execute(
            f"INSERT INTO currency_bot_data (id,currencies) VALUES ({id},ARRAY{currencies})"
        )

    else:
        cur.execute(
            f"UPDATE currency_bot_data SET currencies = ARRAY{currencies} WHERE id = {id};"
        )
    con.commit()
    # form_gist(file, get_statistics_banks(), get_statistics_currencies())
    # upload_to_os(file)


def update_notify(id, notify):
    cur.execute(f"SELECT id FROM currency_bot_data WHERE id={id}")
    if cur.fetchone() is None:
        cur.execute(
            f"INSERT INTO currency_bot_data (id, notify) VALUES ({id}, false)"
        )

    else:
        cur.execute(
            f"UPDATE currency_bot_data SET notify = {notify} WHERE id = {id};"
        )
    con.commit()


def get_notify(id):
    cur.execute(f"SELECT notify "
                f"FROM currency_bot_data "
                f"WHERE id={id} and banks is not null and currencies is not null")
    return cur.fetchone()


def get_banks(id):
    cur.execute(f"SELECT banks FROM currency_bot_data WHERE id={id}")
    return cur.fetchone()


def get_currencies(id):
    cur.execute(f"SELECT currencies FROM currency_bot_data WHERE id={id}")
    return cur.fetchone()


def get_statistics_banks():
    popular_banks = {'Тинькофф': 0, 'ВТБ': 0, 'СБЕР': 0, 'Газпромбанк': 0, 'Альфа-Банк': 0}
    cur.execute(f"SELECT banks FROM currency_bot_data")
    l = cur.fetchall()
    for elem in l:
        for bank in elem[0]:
            print(bank)
            popular_banks[bank] = popular_banks.get(bank) + 1
    print(popular_banks)
    return popular_banks


def get_statistics_currencies():
    popular_currencies = {'Доллар': 0, 'Евро': 0}
    cur.execute(f"SELECT currencies FROM currency_bot_data")
    l = cur.fetchall()
    for elem in l:
        for curr in elem[0]:
            popular_currencies[curr] = popular_currencies.get(curr) + 1
    print(popular_currencies)
    return popular_currencies


def form_gist(filename, popular_banks, popular_currencies):
    x1 = np.array(['Тинькофф', 'ВТБ', 'СБЕР', 'Газпромбанк', 'Альфа-Банк'])
    y1 = np.array([popular_banks.get('Тинькофф'), popular_banks.get('ВТБ'),
                   popular_banks.get('СБЕР'), popular_banks.get('Газпромбанк'), popular_banks.get('Альфа-Банк')])

    x2 = np.array(['Доллар', 'Евро'])
    y2 = np.array([popular_currencies.get('Доллар'), popular_currencies.get('Евро')])

    fig, ax = plt.subplots(2, 1)
    ax[0].bar(x1, y1)
    ax[1].bar(x2, y2)

    ax[0].set_facecolor('seashell')
    fig.set_facecolor('floralwhite')
    fig.set_figwidth(12)
    fig.set_figheight(12)

    plt.savefig(filename)
