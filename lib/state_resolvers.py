from lib.telegram import TelegramBot
import aiosqlite

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
            raise Exception(f'Unknown behaviour, check user state for user_id = {user_id}')


async def resolve_pet_type_state(user_id, state):
    await update_state(user_id, state=state + 1)
    pass


async def resolve_pet_color_state(user_id, state):
    await update_state(user_id, state=state + 1)
    pass


async def resolve_pet_sex_state(user_id, state):
    await update_state(user_id, state=state + 1)
    pass


async def resolve_pet_age_state(user_id, state):
    await update_state(user_id, state=state + 1)
    pass


async def resolve_is_wild_state(user_id, state):
    await update_state(user_id, state=state + 1)
    pass


async def resolve_is_ill_state(user_id, state):
    await update_state(user_id, state=state + 1)
    pass


async def resolve_in_danger_state(user_id, state):
    await update_state(user_id, state=state + 1)
    pass


async def resolve_session_state(user_id):
    pass
