# Meakathon_cat_monitor
> Animal monitoring web-app for counting cat population

> DB INIT
```
import sqlite3
connection = sqlite3.connect('db/animal_monitor.db')
cursor = connection.cursor()
cursor.execute('''DROP TABLE telegram_updates;''')
cursor.execute('''CREATE TABLE IF NOT EXISTS telegram_updates (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    status VARCHAR NOT NULL,
    update_id INTEGER NOT NULL,
    message_id INTEGER NOT NULL UNIQUE,
    message_from_id INTEGER NOT NULL, 
    message_from_is_bot BOOL NOT NULL, 
    message_from_first_name VARCHAR NOT NULL, 
    message_from_username VARCHAR NOT NULL, 
    message_from_language_code VARCHAR,
    message_chat_id INTEGER NOT NULL, 
    message_chat_first_name VARCHAR NOT NULL,
    message_chat_username VARCHAR NOT NULL,
    message_chat_type VARCHAR NOT NULL,
    date TEXT NOT NULL,
    latitude FLOAT,
    longitude FLOAT,
    text TEXT NOT NULL,
    entities_offset INTEGER, 
    entities_length INTEGER, 
    entities_type VARCHAR);'''
)
connection.commit()
connection.close()
```
