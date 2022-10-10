import datetime
import sqlite3


def connecting_bd():
    ''' подключене к БД '''

    conn = sqlite3.connect('logging.db')
    return conn


def create_table(conn, cursor):
    ''' Создание таблицы '''

    sql_create_table = "CREATE TABLE IF NOT EXISTS log_request(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL," \
                       " city TEXT, status TEXT, cteatedDT timestamp);"
    cursor.execute(sql_create_table)
    conn.commit()


def create_log(conn, cursor, city, status):
    ''' Создание записи в таблице БД '''

    date_now = datetime.datetime.now()
    sql_request = f'INSERT INTO log_request(city, status, cteatedDT) VALUES("{city}", "{status}", "{date_now}");'
    cursor.execute(sql_request)
    conn.commit()
