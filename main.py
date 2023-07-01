from datetime import datetime, timezone, timedelta
from time import sleep

from database_connection import connect_to_db, add_multiple_messages_to_db
from telegram_scraper import get_messages_from_session, create_session


def main():
    conn = connect_to_db()
    while True:
        # Specify the date range for filtering messages
        end_date = datetime.now(tz=timezone.utc)
        start_date = end_date - timedelta(minutes=1)  # Read the messages from the last minute

        messages = get_messages_from_session(create_session(), start_date, end_date)
        add_multiple_messages_to_db(conn, messages)
        sleep(60)


if __name__ == '__main__':
    main()
