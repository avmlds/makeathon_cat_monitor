# Makeathon pet monitor
> Animal monitoring web-app for counting cat population
> Init DB in /db/ folder, specify TELEGRAM_TOKEN' in lib/secret.py 


```
User states

#        {"0": user in db, geo is set,
#         "1": user in db, photo is sent,
#         "2": user in db, pet_type checked,
#         "3": user in db, pet_color checked,
#         "4": user in db, pet_sex checked,
#         "5": user in db, pet_age checked,
#         "6": user in db, is_wild checked,
#         "7": user in db, is_ill checked,
#         "8": user in db, in_danger checked,
#         "9": user in db, session ended

```

>DB INIT

![image info](docs/makeathon.svg) 

```

import sqlite3

connection = sqlite3.connect('db/animal_monitor.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS telegram_updates (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    status VARCHAR NOT NULL,
    update_id INTEGER NOT NULL,
    message_id INTEGER NOT NULL,
    message_from_id INTEGER NOT NULL, 
    message_from_is_bot INTEGER NOT NULL, 
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
    entities_type VARCHAR,
    is_answered INTEGER DEFAULT 0 NOT NULL);''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    telegram_id VARCHAR UNIQUE NOT NULL, 
    username VARCHAR NOT NULL, 
    first_name VARCHAR NOT NULL, 
    system_timestamp TEXT NOT NULL,
    date TEXT NOT NULL,
    live_period INTEGER NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 0);''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER REFERENCES user(id) ON UPDATE CASCADE,
    message_id INTEGER NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    system_timestamp TEXT NOT NULL,
    date TEXT NOT NULL,
    live_period INTEGER NOT NULL,
    heading FLOAT, 
    horizontal_accuracy FLOAT);''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS pet_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER REFERENCES user(id) ON UPDATE CASCADE,
    tracking_id INTEGER REFERENCES user_tracking(id) ON UPDATE CASCADE,
    message_id INTEGER REFERENCES user_tracking(message_id) ON UPDATE CASCADE,
    system_timestamp TEXT NOT NULL,
    pet_type VARCHAR NOT NULL,
    sex VARCHAR NOT NULL,
    color VARCHAR NOT NULL,
    age INTEGER NOT NULL,
    photo_path VARCHAR NOT NULL,
    is_wild INTEGER NOT NULL,
    is_ill INTEGER NOT NULL,
    in_danger INTEGER NOT NULL);''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS proceeded_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    update_id INTEGER UNIQUE NOT NULL,
    is_resolved INTEGER NOT NULL DEFAULT 1);''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_state (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER UNIQUE REFERENCES user(id) ON UPDATE CASCADE,
    state INTEGER NOT NULL DEFAULT 0);''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS trusted_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    telegram_id INTEGER UNIQUE REFERENCES user(telegram_id) ON UPDATE CASCADE NOT NULL,
    telegram_username VARCHAR REFERENCES user(telegram_username) ON UPDATE CASCADE NOT NULL,
    telegram_first_name VARCHAR REFERENCES user(first_name) ON UPDATE CASCADE NOT NULL);''')

connection.commit()
connection.close()
```
