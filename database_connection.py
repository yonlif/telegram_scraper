import json
import mysql.connector


def read_database_settings(settings_file: str = "database_settings.json"):
    with open(settings_file, 'r') as json_file:
        return json.load(json_file)


def connect_to_db():
    # Connect to the MySQL database
    database_settings = read_database_settings()
    print(database_settings)
    db_connection = mysql.connector.connect(
        **database_settings,
    )

    create_db_query = "CREATE DATABASE IF NOT EXISTS telegram_messages_db"
    with db_connection.cursor() as cursor:
        cursor.execute(create_db_query)

    create_table_query = '''
        CREATE TABLE IF NOT EXISTS telegram_messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            chat_name VARCHAR(255),
            sender_name VARCHAR(255),
            sender_phone VARCHAR(255),
            message TEXT,
            photo_url VARCHAR(255),
            timestamp TIMESTAMP
        ) CHARACTER SET utf8mb4
    '''
    with db_connection.cursor() as cursor:
        cursor.execute(create_table_query)
    return db_connection


def add_message_to_db(db_connection, message):
    insert_query = '''
        INSERT INTO telegram_messages (chat_name, sender_name, sender_phone, message, photo_url, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    with db_connection.cursor() as cursor:
        cursor.execute(insert_query, message)
    db_connection.commit()


def add_multiple_messages_to_db(db_connection, messages):
    for msg in messages:
        add_message_to_db(db_connection, msg)


def main():
    # Testing db connection and printing content
    db_connection = connect_to_db()
    print_query = '''
        SELECT * FROM telegram_messages
    '''
    with db_connection.cursor() as cursor:
        cursor.execute(print_query)
        res = cursor.fetchall()

    for _ in res[:10]:
        print(_)


if __name__ == '__main__':
    main()
