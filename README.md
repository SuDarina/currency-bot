# currency_bot

## Развертывание

- В файле ```database_work.py``` внести параметры подключения к базе данных PostgreSQL <br>

Например:
```
con = psycopg2.connect(
    database="currency_bot",
    user="user",
    password="1234567890",
    host="localhost",
    port="5432"
)
```

- Загрузить табличку в базу данных из DDL-файла ```database.sql```
- Запустить файл ```main.py```