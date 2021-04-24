# Meakathon_cat_monitor
> Animal monitoring web-app for counting cat population

> DB INIT
```
_import sqlite3

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
    in_danger INTEGER NOT NULL);'''
               )
cursor.execute('''
CREATE TABLE IF NOT EXISTS proceeded_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    update_id INTEGER UNIQUE NOT NULL,
    is_resolved INTEGER NOT NULL DEFAULT 1
);'''
               )

connection.commit()
connection.close()_
```


            """
            if not response['ok']:
                return {'Messages': 'No new'}

            for message_response in parsed_response.result:
                if 'message' in message_response.dict().keys():
                    data = {'status': parsed_response.ok,
                            'update_id': message_response.update_id,
                            'message_id': message_response.message.message_id,
                            'message_from_id': message_response.message.from_.id,
                            'message_from_is_bot': message_response.message.from_.is_bot,
                            'message_from_first_name': message_response.message.from_.first_name,
                            'message_from_username': message_response.message.from_.username,
                            'message_from_language_code': message_response.message.from_.language_code,
                            'message_chat_id': message_response.message.chat.id,
                            'message_chat_first_name': message_response.message.chat.first_name,
                            'message_chat_username': message_response.message.chat.username,
                            'message_chat_type': message_response.message.chat.type,
                            'date': message_response.message.date.isoformat()}

                    if message_response.message.entities is not None:
                        data.update({'entities_offset': message_response.message.entities[0].offset,
                                     'entities_length': message_response.message.entities[0].length,
                                     'entities_type': message_response.message.entities[0].type})
                    else:
                        data.update({'entities_offset': None, 'entities_length': None, 'entities_type': None})

                    if message_response.message.location is not None:
                        data.update({'longitude': message_response.message.location.longitude,
                                     'latitude': message_response.message.location.latitude,
                                     'live_period': message_response.message.location.live_period,
                                     })
                    else:
                        data.update({'longitude': None, 'latitude': None})

                    if message_response.message.text is not None:
                        data.update({'text': message_response.message.text})
                    else:
                        data.update({'text': None})

                async with aiosqlite.connect('../db/animal_monitor.db') as db:
                    await db.execute(INSERT_UPDATES % data)
                    await db.commit()

            if response['ok']:
                for result in response['result']:
                    async with aiosqlite.connect('../db/animal_monitor.db') as db:
                        res = await db.execute(CHECK_IS_ANSWERED.format(message_id=result['message']['message_id'],
                                                                        chat_id=result['message']['chat']['id']))
                        row = await res.fetchall()
                        chat_id = row[0][0]
                        message_id = row[0][1]
                        is_answered = row[0][2]
                        if not is_answered:
                            await self.message_handler(result)

                        await db.execute(UPDATE_ANSWERED.format(message_id=message_id, chat_id=chat_id))
                        await db.commit()
            """