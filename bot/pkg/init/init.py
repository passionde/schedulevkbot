import json
import logging
import psycopg2
from psycopg2 import pool

logger = logging.getLogger("init")


# Функция инициализации расписания
def init_schedule(path: str):
    try:
        with open(path, "r", encoding="utf-8") as read_file:
            schedules = json.load(read_file)
            logger.info("Successfully Initialized Class Schedule")
            return schedules
    except FileNotFoundError:
        logger.critical(f'File "{path}" not found')
        exit(2)


# Функция создания пула соединений
def init_connections_pool(**kwargs):
    try:
        connections = psycopg2.pool.ThreadedConnectionPool(1, 1, **kwargs)
        logger.info("Successful database connection pooling")
        return connections
    except (Exception, psycopg2.DatabaseError) as error:
        logger.critical(f"Error connecting to PostgreSQL {error}")
        exit(2)


# Функция инициализации данных о номерах групп пользователей
def init_users_group(pool_connections: psycopg2.pool):
    try:
        # запрос к БД
        connection = pool_connections.getconn()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM group_users")
        records = cursor.fetchall()

        # закрытие соединения и возврат его в пул
        cursor.close()
        pool_connections.putconn(connection)

        # формирование словаря {user_id: number_group}
        users_group = {row[0]: str(row[1]).strip() for row in records}

        logger.info(f"Successful initialization of user group number information. "
                    f"Received data on {len(users_group)} users")

        return users_group

    except (Exception, psycopg2.DatabaseError) as error:
        logger.critical(f"Error connecting to PostgreSQL {error}")
        exit(2)


def init_user_states(pool_connections: psycopg2.pool):
    try:
        # запрос к БД
        connection = pool_connections.getconn()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM states")
        user_ids = cursor.fetchall()

        # закрытие соединения и возврат его в пул
        cursor.close()
        pool_connections.putconn(connection)

        logger.info("Successfully getting current user states")

        # формирование словаря
        return {i[0]: None for i in user_ids}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.critical(f"Error connecting to PostgreSQL {error}")
        exit(2)
