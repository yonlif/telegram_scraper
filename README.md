Python Client to scrape messages, save to MySQL DB and serve to get requests.

### Setup:
1. Python (3.10)
   1. Pip install `telethon==1.28.5`, `mysql-connector-python==8.0.33` and `Flask==1.0.2` (All written in the `requirement.txt` file)
2. You'll need MySQL Server
   1. Get the username, password, hostname and port to the `database_settings.json` file
3. Activated Telegram account
   1. After activation go to https://my.telegram.org/ and menage apps
   2. Put your phone number, api id and api hash in the `credentials.json` file

> Example for `credentials.json` file:
```
{
  "clients": [
      {
        "phone_number": "+972 123 456 789",
        "api_id": 12345678,
        "api_hash": "1234567890abcdef1234567890abcdef"
      }
    ]
}
```

### Run:
1. You'll need to run the telegram scraper every once in a while
2. Run the server
   1. Example request: ```http://localhost:5000/data?from_date=2023-06-20&to_date=2023-06-30&chat_name=cool chat```
