# Meakathon_cat_monitor
> Animal monitoring web-app for counting cat population

> DB INIT
```
import sqlite3

connection = sqlite3.connect('db/animal_monitor.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS telegram_updates (
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
    entities_type VARCHAR,
    is_answered BOOL DEFAULT FALSE NOT NULL);''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    telegram_id VARCHAR UNIQUE NOT NULL, 
    username VARCHAR NOT NULL, 
    first_name VARCHAR NOT NULL, 
    date TEXT NOT NULL,
    live_period INTEGER NOT NULL,
    is_active BOOL NOT NULL DEFAULT FALSE);''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER REFERENCES user(id) ON UPDATE CASCADE,
    message_id INTEGER NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    date TEXT NOT NULL,
    live_period INTEGER NOT NULL,
    heading FLOAT, 
    horizontal_accuracy FLOAT);''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS pet_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER REFERENCES user(id) ON UPDATE CASCADE,
    tracking_id INTEGER REFERENCES user_tracking(id) ON UPDATE CASCADE,
    pet_type VARCHAR NOT NULL,
    sex VARCHAR NOT NULL,
    color VARCHAR NOT NULL,
    age INTEGER NOT NULL,
    photo_path VARCHAR NOT NULL,
    is_wild BOOL NOT NULL,
    is_ill BOOL NOT NULL,
    in_danger BOOL NOT NULL);'''
               )
connection.commit()
connection.close()
```