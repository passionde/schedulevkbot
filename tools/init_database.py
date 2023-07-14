import json

import psycopg2

db_set = {
    'database': 'sferabot',
    'user': 'yarik_de',
    'password': '3d7469e3e2ea2fd7616a86a5492d9b8da628c9248b462900d720d44956571344',
    'host': 'localhost',
}


def create_tables():
    conn = psycopg2.connect(**db_set)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE group_users  
         (id INT PRIMARY KEY NOT NULL,
         number_group CHAR(20) NOT NULL);''')

    cursor.execute('''CREATE TABLE states (user_id INT PRIMARY KEY NOT NULL);''')

    conn.commit()
    cursor.close()


def load_backup():
    conn = psycopg2.connect(**db_set)
    cursor = conn.cursor()

    data = json.load(open("backup/load.json", "r", encoding="utf-8"))
    cursor.executemany("INSERT INTO group_users (id, number_group) VALUES (%s, %s)", data)

    conn.commit()
    cursor.close()


# create_tables()
load_backup()
