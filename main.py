import argparse
from datetime import datetime, timezone, timedelta
from time import sleep

from database_connection import connect_to_db, add_multiple_messages_to_db
from telegram_scraper import get_messages_from_session, create_session


def main(sampling_time):
    conn = connect_to_db()
    while True:
        # Specify the date range for filtering messages
        end_date = datetime.now(tz=timezone.utc)
        start_date = end_date - timedelta(seconds=sampling_time)  # Read the messages from the last minute

        messages = get_messages_from_session(create_session(), start_date, end_date)
        add_multiple_messages_to_db(conn, messages)
        sleep(sampling_time)


def single(start_date, end_date):
    conn = connect_to_db()
    messages = get_messages_from_session(create_session(), start_date, end_date)
    add_multiple_messages_to_db(conn, messages)


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    main_parser = subparsers.add_parser('main')
    main_parser.add_argument('--sample-time', '-t', type=int,
                             help='Sampling time in seconds')

    single_parser = subparsers.add_parser('single')
    group = single_parser.add_mutually_exclusive_group(required=True)
    single_parser.add_argument('--end-date', '-e', type=str, default=datetime.now(tz=timezone.utc),
                               help='End date (format: YYYY-MM-DD HH:MM:SS)')
    group.add_argument('--start-date', '-s', type=str, default=None,
                       help='Start date (format: YYYY-MM-DD HH:MM:SS)')
    group.add_argument('--sample-time', '-t', type=int,
                       help='Sample time backwards (use instead of start_date)')

    args = parser.parse_args()

    if args.command == 'main':
        main(args.sample_time)
    elif args.command == 'single':
        start_date = args.start_date if args.start_date else args.end_date - timedelta(seconds=args.sample_time)
        single(start_date, args.end_date)
    else:
        parser.print_help()


if __name__ == '__main__':
    # python script.py main --sampling_time 60
    # python script.py single --start_date "2023-07-01 09:00:00" --end_date "2023-07-03 12:00:00"
    # python script.py single --sampling_time 100 --end_date "2023-07-03 12:00:00"
    # python script.py single --sampling_time 100
    parse_args()
