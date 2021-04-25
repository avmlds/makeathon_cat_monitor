from lib.telegram import TelegramBot
import aiosqlite
from datetime import datetime

#         "2": user in db, pet_type checked,
#         "3": user in db, pet_color checked,
#         "4": user in db, pet_sex checked,
#         "5": user in db, pet_age checked,
#         "6": user in db, is_wild checked,
#         "7": user in db, is_ill checked,
#         "8": user in db, in_danger checked,
#         "9": user in db, session ended


async def insert_state(user_id):
    query = f'INSERT OR IGNORE INTO user_state(user_id) VALUES({user_id});'
    async with aiosqlite.connect('../db/animal_monitor.db') as db:
        result = await db.execute(query)
        await db.commit()


async def update_state(user_id, state):
    query = f'UPDATE user_state SET state = {state} WHERE user_id = {user_id};'
    async with aiosqlite.connect('../db/animal_monitor.db') as db:
        result = await db.execute(query)
        await db.commit()


async def get_state(user_id):
    query = f'SELECT state FROM user_state WHERE user_id = {user_id};'
    async with aiosqlite.connect('../db/animal_monitor.db') as db:
        result = await db.execute(query)
        data = await result.fetchall()
        await db.commit()
        if len(data) == 1:
            return data[0][0]
        else:
            print(f'Unknown behaviour, check user state for user_id = {user_id}')
            print('user is not in db')


async def callback_query_resolver(data):
    user_id = data.callback_query.from_.id
    state = await get_state(user_id)
    if state == 1 and 'type' in data.callback_query.data:
        type_ = [i['text'] for i in TelegramBot.pet_types_buttons if i['callback_data'] == data.callback_query.data][0]
        await resolve_pet_type_state(user_id, state, data, type_)

    if state == 2 and 'color' in data.callback_query.data:
        color = [i['text'] for i in TelegramBot.animal_color_buttons if i['callback_data'] == data.callback_query.data][0]
        await resolve_pet_color_state(user_id, state, data, color)

    if state == 3 and 'sex' in data.callback_query.data:
        sex = [i['text'] for i in TelegramBot.animal_sex_buttons if i['callback_data'] == data.callback_query.data][0]
        await resolve_pet_sex_state(user_id, state, data, sex)

    if state == 4 and 'age' in data.callback_query.data:
        age = int(data.callback_query.data.replace('age_', ''))
        await resolve_pet_age_state(user_id, state, data, age)

    if state == 5 and 'wild' in data.callback_query.data:
        wild = int(data.callback_query.data.replace('wild_', ''))
        await resolve_pet_wild_state(user_id, state, data, wild)

    if state == 6 and 'ill' in data.callback_query.data:
        ill = int(data.callback_query.data.replace('ill_', ''))
        await resolve_pet_ill_state(user_id, state, data, ill)

    if state == 7 and 'danger' in data.callback_query.data:
        danger = int(data.callback_query.data.replace('danger_', ''))
        await resolve_pet_danger_state(user_id, state, data, danger)

    if state == 8 and 'height' in data.callback_query.data:
        height = int(data.callback_query.data.replace('height_', ''))
        await resolve_pet_height_state(user_id, state, data, height)


async def resolve_pet_type_state(user_id, state, data, type_):
    pet_data = await TelegramBot.get_user_tracking_id(data.callback_query.from_.id)
    if pet_data is not None:
        tracking_id, user_id, message_id, date, live_period = pet_data[0], pet_data[1], pet_data[2], \
                                                              pet_data[3], pet_data[4]
        await insert_pet_type_data_in_db(user_id, tracking_id, message_id, type_)
        await update_state(user_id, state=state + 1)
    else:
        print('Set geolocation first!')


async def resolve_pet_color_state(user_id, state, data, color):
    pet_data = await TelegramBot.get_user_tracking_id(data.callback_query.from_.id)
    if pet_data is not None:
        tracking_id, user_id, message_id, date, live_period = pet_data[0], pet_data[1], pet_data[2], \
                                                              pet_data[3], pet_data[4]
        await insert_color_data_in_db(user_id, tracking_id, message_id, color)
        await update_state(user_id, state=state + 1)
    else:
        print('Set geolocation first!')


async def resolve_pet_sex_state(user_id, state, data, sex):
    pet_data = await TelegramBot.get_user_tracking_id(data.callback_query.from_.id)
    if pet_data is not None:
        tracking_id, user_id, message_id, date, live_period = pet_data[0], pet_data[1], pet_data[2], \
                                                              pet_data[3], pet_data[4]
        await insert_sex_data_in_db(user_id, tracking_id, message_id, sex)
        await update_state(user_id, state=state + 1)
    else:
        print('Set geolocation first!')
    pass


async def resolve_pet_age_state(user_id, state, data, age):
    pet_data = await TelegramBot.get_user_tracking_id(data.callback_query.from_.id)
    if pet_data is not None:
        tracking_id, user_id, message_id, date, live_period = pet_data[0], pet_data[1], pet_data[2], \
                                                              pet_data[3], pet_data[4]
        await insert_age_data_in_db(user_id, tracking_id, message_id, age)
        await update_state(user_id, state=state + 1)
    else:
        print('Set geolocation first!')


async def resolve_pet_wild_state(user_id, state, data, wild):
    pet_data = await TelegramBot.get_user_tracking_id(data.callback_query.from_.id)
    if pet_data is not None:
        tracking_id, user_id, message_id, date, live_period = pet_data[0], pet_data[1], pet_data[2], \
                                                              pet_data[3], pet_data[4]
        await insert_wild_data_in_db(user_id, tracking_id, message_id, wild)
        await update_state(user_id, state=state + 1)
    else:
        print('Set geolocation first!')



async def resolve_pet_ill_state(user_id, state, data, ill):
    pet_data = await TelegramBot.get_user_tracking_id(data.callback_query.from_.id)
    if pet_data is not None:
        tracking_id, user_id, message_id, date, live_period = pet_data[0], pet_data[1], pet_data[2], \
                                                              pet_data[3], pet_data[4]
        await insert_ill_data_in_db(user_id, tracking_id, message_id, ill)
        await update_state(user_id, state=state + 1)
    else:
        print('Set geolocation first!')


async def resolve_pet_danger_state(user_id, state, data, danger):
    pet_data = await TelegramBot.get_user_tracking_id(data.callback_query.from_.id)
    if pet_data is not None:
        tracking_id, user_id, message_id, date, live_period = pet_data[0], pet_data[1], pet_data[2], \
                                                              pet_data[3], pet_data[4]
        await insert_danger_data_in_db(user_id, tracking_id, message_id, danger)
        await update_state(user_id, state=state + 1)
    else:
        print('Set geolocation first!')


async def resolve_pet_height_state(user_id, state, data, height):
    pet_data = await TelegramBot.get_user_tracking_id(data.callback_query.from_.id)
    if pet_data is not None:
        tracking_id, user_id, message_id, date, live_period = pet_data[0], pet_data[1], pet_data[2], \
                                                              pet_data[3], pet_data[4]
        await insert_height_data_in_db(user_id, tracking_id, message_id, height)
        await update_state(user_id, state=state + 1)
    else:
        print('Set geolocation first!')



async def resolve_session_state(user_id):
    pass


async def insert_pet_type_data_in_db(user_id, tracking_id, message_id, pet_type):
    system_timestamp = datetime.now().isoformat()
    query = f"INSERT INTO pet_tracking (user_id, tracking_id, message_id, system_timestamp, pet_type) " \
            f"VALUES  ('{user_id}', '{tracking_id}', '{message_id}', '{system_timestamp}', '{pet_type}');"
    async with aiosqlite.connect('../db/animal_monitor.db') as db:
        res = await db.execute(query)
        await db.commit()
    return True


async def insert_color_data_in_db(user_id, tracking_id, message_id, color):
    query_1 = f"SELECT id FROM pet_tracking WHERE user_id='{user_id}' AND " \
              f"tracking_id = '{tracking_id}' ORDER BY pet_tracking.id DESC LIMIT 1;"
    async with aiosqlite.connect('../db/animal_monitor.db') as db:
        res = await db.execute(query_1)
        data = await res.fetchall()
        id_ = data[0][0]

    query = f"UPDATE pet_tracking SET color = '{color}' " \
            f"WHERE  user_id='{user_id}' AND id = {id_} AND " \
            f"tracking_id = '{tracking_id}';"
    async with aiosqlite.connect('../db/animal_monitor.db') as db:
        res = await db.execute(query)
        await db.commit()


async def insert_sex_data_in_db(user_id, tracking_id, message_id, sex):
    query_1 = f"SELECT id FROM pet_tracking WHERE user_id='{user_id}' AND " \
              f"tracking_id = '{tracking_id}' ORDER BY pet_tracking.id DESC LIMIT 1;"
    async with aiosqlite.connect('../db/animal_monitor.db') as db:
        res = await db.execute(query_1)
        data = await res.fetchall()
        id_ = data[0][0]

    query = f"UPDATE pet_tracking SET sex = '{sex}' " \
            f"WHERE  user_id='{user_id}' AND id = {id_} AND " \
            f"tracking_id = '{tracking_id}';"
    async with aiosqlite.connect('../db/animal_monitor.db') as db:
        res = await db.execute(query)
        await db.commit()


async def insert_age_data_in_db(user_id, tracking_id, message_id, age):
    query_1 = f"SELECT id FROM pet_tracking WHERE user_id='{user_id}' AND " \
              f"tracking_id = '{tracking_id}' ORDER BY pet_tracking.id DESC LIMIT 1;"
    async with aiosqlite.connect('../db/animal_monitor.db') as db:
        res = await db.execute(query_1)
        data = await res.fetchall()
        id_ = data[0][0]

    query = f"UPDATE pet_tracking SET age = '{age}' " \
            f"WHERE  user_id='{user_id}' AND id = {id_} AND " \
            f"tracking_id = '{tracking_id}';"
    async with aiosqlite.connect('../db/animal_monitor.db') as db:
        res = await db.execute(query)
        await db.commit()


async def insert_wild_data_in_db(user_id, tracking_id, message_id, wild):
    query_1 = f"SELECT id FROM pet_tracking WHERE user_id='{user_id}' AND " \
              f"tracking_id = '{tracking_id}' ORDER BY pet_tracking.id DESC LIMIT 1;"
    async with aiosqlite.connect('../db/animal_monitor.db') as db:
        res = await db.execute(query_1)
        data = await res.fetchall()
        id_ = data[0][0]

    query = f"UPDATE pet_tracking SET is_wild = '{wild}' " \
            f"WHERE  user_id='{user_id}' AND id = {id_} AND " \
            f"tracking_id = '{tracking_id}';"
    async with aiosqlite.connect('../db/animal_monitor.db') as db:
        res = await db.execute(query)
        await db.commit()


async def insert_ill_data_in_db(user_id, tracking_id, message_id, ill):
    query_1 = f"SELECT id FROM pet_tracking WHERE user_id='{user_id}' AND " \
              f"tracking_id = '{tracking_id}' ORDER BY pet_tracking.id DESC LIMIT 1;"
    async with aiosqlite.connect('../db/animal_monitor.db') as db:
        res = await db.execute(query_1)
        data = await res.fetchall()
        id_ = data[0][0]

    query = f"UPDATE pet_tracking SET is_ill = '{ill}' " \
            f"WHERE  user_id='{user_id}' AND id = {id_} AND " \
            f"tracking_id = '{tracking_id}';"
    async with aiosqlite.connect('../db/animal_monitor.db') as db:
        res = await db.execute(query)
        await db.commit()


async def insert_danger_data_in_db(user_id, tracking_id, message_id, danger):
    query_1 = f"SELECT id FROM pet_tracking WHERE user_id='{user_id}' AND " \
              f"tracking_id = '{tracking_id}' ORDER BY pet_tracking.id DESC LIMIT 1;"
    async with aiosqlite.connect('../db/animal_monitor.db') as db:
        res = await db.execute(query_1)
        data = await res.fetchall()
        id_ = data[0][0]

    query = f"UPDATE pet_tracking SET in_danger = '{danger}' " \
            f"WHERE  user_id='{user_id}' AND id = {id_} AND " \
            f"tracking_id = '{tracking_id}';"
    async with aiosqlite.connect('../db/animal_monitor.db') as db:
        res = await db.execute(query)
        await db.commit()


async def insert_height_data_in_db(user_id, tracking_id, message_id, height):
    query_1 = f"SELECT id FROM pet_tracking WHERE user_id='{user_id}' AND " \
              f"tracking_id = '{tracking_id}' ORDER BY pet_tracking.id DESC LIMIT 1;"
    async with aiosqlite.connect('../db/animal_monitor.db') as db:
        res = await db.execute(query_1)
        data = await res.fetchall()
        id_ = data[0][0]

    query = f"UPDATE pet_tracking SET height = '{height}' " \
            f"WHERE  user_id='{user_id}' AND id = {id_} AND " \
            f"tracking_id = '{tracking_id}';"
    async with aiosqlite.connect('../db/animal_monitor.db') as db:
        res = await db.execute(query)
        await db.commit()