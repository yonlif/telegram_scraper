import json
import logging

from telethon.sync import TelegramClient
from datetime import datetime, timezone, timedelta
from telethon import utils

from ner_api import ner_from_message
from translate_message import translate_message

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def read_credentials(cred_file: str = "credentials.json"):
    with open(cred_file, 'r') as json_file:
        return json.load(json_file)["clients"][0]


def create_session(session_name: str = "session_name"):
    creds = read_credentials()
    client = TelegramClient(session_name, creds["api_id"], creds["api_hash"])
    client.start(creds["phone_number"])
    return client




def get_messages_from_session(client, start_date, end_date):
    return_messages = []
    with client:
        # Get dialogs (chats and channels)
        dialogs = client.iter_dialogs()

        # Iterate over dialogs and process messages within the specified date range
        # From newest to oldest
        for dialog in dialogs:
            if dialog.date < start_date:
                break
            logging.info(f"Processing messages in: {dialog.name}, from date: {dialog.date}")
            messages = client.iter_messages(dialog)

            for message in messages:
                # Filter messages based on the date range
                if start_date <= message.date <= end_date:
                    sender = client.get_entity(message.sender_id)

                    # Extract sender's name and phone number
                    sender_name = utils.get_display_name(sender)
                    sender_phone = sender.__dict__.get('phone', '') or ''

                    logging.info(f"\tFull Sender: {sender}")
                    logging.info(f"\tSender: {sender_name}, Phone: {sender_phone}")
                    logging.info(f"\t\tMessage: {message.message}")

                    photo_path = None
                    # Check if the message contains a photo
                    if message.photo:
                        # Download the photo
                        photo_path = client.download_media(message, file="./downloaded_photos/")

                        # Print the downloaded photo path
                        logging.info(f"\tDownloaded photo: {photo_path}")
                    translated_message = "Could not translate message"
                    try:
                        translated_message = translate_message(message.message)
                    except Exception as e:
                        logging.error(e)

                    ner_object = None
                    try:
                        ner_object = str(ner_from_message(message.message))
                    except Exception as e:
                        logging.error(e)
                    return_messages.append([dialog.name,
                                            sender_name,
                                            sender_phone,
                                            message.message,
                                            translated_message,
                                            photo_path,
                                            message.date.strftime('%Y-%m-%d %H:%M:%S'),
                                            ner_object])
            logging.info('-' * 30)
    return return_messages


def main():
    # Specify the date range for filtering messages
    # start_date = datetime(2023, 6, 25, tzinfo=timezone.utc)  # Replace with your desired start date
    end_date = datetime.now(tz=timezone.utc)  # Replace with your desired end date
    start_date = end_date - timedelta(days=5)

    messages = get_messages_from_session(create_session(), start_date, end_date)
    print(messages[-1])
    print(f"read {len(messages)} messages")


if __name__ == '__main__':
    main()
