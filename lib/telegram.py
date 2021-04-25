import asyncio
import aiofiles
import aiohttp
import aiosqlite
from aiofiles import os as aioos
import os
from lib.secret import TELEGRAM_TOKEN
from lib.models import TelegramUpdateResponse, TelegramPhotoPathResponse
from lib.sql_queries import INSERT_UPDATES, UPDATE_ANSWERED, CHECK_IS_ANSWERED
from messages.message_texts import START_MESSAGE_TEXT
from datetime import datetime, timedelta
from warnings import warn
import concurrent.futures
from lib.state_resolvers import *


class TelegramBot:
    def __init__(self, token):
        self.root = f'https://api.telegram.org/bot{token}/' + '{method}'
        self.update_polls_command = self.root.format(method='getUpdates')
        self.send_message_method = 'sendMessage?chat_id={chat_id}&text={message_text}&parse_mode=HTML'
        self.send_message_command = self.root.format(method=self.send_message_method)
        self.get_file_step_1 = self.root.format(method='getFile?file_id={file_id}')
        self.get_file_step_2 = f'https://api.telegram.org/file/bot{token}/' + '{file_path}'
        self.query = []
        self.updates = []

    @staticmethod
    async def async_request(session_kwargs, request_kwargs):
        async with aiohttp.ClientSession(**session_kwargs) as session:
            async with session.request(**request_kwargs) as response:
                return await response.json()

    async def update_polls(self):
        while True:
            # await asyncio.sleep(3)
            response = await TelegramBot.async_request(session_kwargs={},
                                                       request_kwargs={'method': 'POST',
                                                                       'url': self.update_polls_command})
            parsed_response = TelegramUpdateResponse.parse_obj(response)
            if not parsed_response.ok:
                raise Exception('Status is not OK')
            for data in parsed_response.result:
                if await self.is_update_resolved(update_id=data.update_id):
                    continue
                await TelegramBot.track_update(update_id=data.update_id)

                correct_message = data.message if data.message is not None else data.edited_message
                telegram_id = correct_message.from_.id
                update_id = data.update_id
                chat_id = correct_message.chat.id

                # im checking this first cause average users will send location first
                if data.message is not None:
                    if correct_message.location is not None and correct_message.location.live_period is not None:
                        # start_tracking
                        await self.start_tracking_user(data=data)
                    elif correct_message.location is not None and correct_message.location.live_period is None:
                        await self.send_message(chat_id=chat_id, text='Вы должны отправить отслеживание ' \
                                                                      'геопозиции, а не одиночную геопозицию')
                else:
                    if correct_message.location is not None \
                            and correct_message.location.live_period is not None \
                            and correct_message.location.heading is not None:
                        await TelegramBot.continue_tracking_user(data=data)

                if correct_message.text != '/start':
                    await self.send_message(chat_id=chat_id, text='')
                else:
                    await self.send_message(chat_id=chat_id, text=START_MESSAGE_TEXT)

                checked_user = await self.check_user_in_db(telegram_id=telegram_id, chat_id=chat_id)

                if not checked_user[0]:
                    await TelegramBot.resolve_update(update_id=data.update_id)
                    continue

                if data.message is not None and data.message.photo is not None:
                    current_message = data.message
                    if not await self.resolve_pet_photo(data, current_message):
                        continue
                elif data.edited_message is not None and data.edited_message.photo is not None:
                    current_message = data.edited_message
                    if not await self.resolve_pet_photo(data, current_message):
                        continue
                else:
                    print('no photo in file')


                # file_id: str
                # file_unique_id: str
                # file_size: int
                # width: int
                # height: int

                await self.resolve_update(update_id=data.update_id)
                print(data)

    async def resolve_pet_photo(self, data, current_message):
        if await get_state(current_message.from_.id) == 0:
            await self.send_message(current_message.chat.id, text='Закончите описание животного')
            await self.resolve_update(update_id=data.update_id)
            return False
        pet = await self.get_pet_params(current_message, current_message.chat.id)
        if pet is not None:
            await update_state(current_message.from_.id, 1)
            return True

    async def check_user_in_db(self, telegram_id, chat_id):
        async with aiosqlite.connect('../db/animal_monitor.db') as db:
            res = await db.execute(f'SELECT id, is_active FROM user WHERE telegram_id = {telegram_id};')
            result = await res.fetchall()
            await db.commit()
            if len(result) == 0:
                await self.send_message(chat_id=chat_id, text=START_MESSAGE_TEXT)
                return False, 0, 0
            elif len(result) == 1:
                # Bool, id (user), is_active (user)
                return True, result[0][0], result[0][1]
            else:
                raise Exception('Unknown behaviour')

    @staticmethod
    async def make_active(telegram_id):
        async with aiosqlite.connect('../db/animal_monitor.db') as db:
            res = await db.execute(f'INSERT INTO user VALUES( id, is_active FROM user '
                                   f'WHERE telegram_id = {telegram_id};')
            await db.commit()

    @staticmethod
    async def start_tracking_user(data):
        update_id = data.update_id
        user_id = data.message.from_.id
        username = data.message.from_.username
        first_name = data.message.from_.first_name
        message_id = data.message.message_id
        # system timestamp
        system_timestamp = datetime.now().isoformat()
        # telegram message timestamp
        iso_timestamp = data.message.date.isoformat()
        live_period = data.message.location.live_period
        latitude = data.message.location.latitude
        longitude = data.message.location.longitude
        heading = data.message.location.heading
        horizontal_accuracy = data.message.location.horizontal_accuracy

        user_query = f"INSERT OR IGNORE INTO user(telegram_id, username, first_name, " \
                     f"system_timestamp, date, live_period, is_active) " \
                     f"VALUES('{user_id}', '{username}', '{first_name}', '{system_timestamp}'," \
                     f"'{iso_timestamp}', '{live_period}'," \
                     f" '{1}');"
        async with aiosqlite.connect('../db/animal_monitor.db') as db:
            query_id_ = await db.execute(user_query)
            await db.commit()
            last_row_id = query_id_.lastrowid
        async with aiosqlite.connect('../db/animal_monitor.db') as db:
            tracking_query = f"INSERT INTO user_tracking(user_id, message_id, latitude, longitude, " \
                             f"system_timestamp, date, live_period, heading, horizontal_accuracy) " \
                             f"VALUES('{last_row_id}', '{message_id}', '{latitude}', '{longitude}', " \
                             f"'{system_timestamp}'," \
                             f"'{iso_timestamp}', '{live_period}', '{heading}', '{horizontal_accuracy}');"
            inserted_data = await db.execute(tracking_query)
            await db.commit()
        await insert_state(user_id)

    @staticmethod
    async def continue_tracking_user(data):
        update_id = data.update_id
        user_id = data.edited_message.from_.id
        message_id = data.edited_message.message_id
        # system timestamp
        system_timestamp = datetime.now().isoformat()
        # telegram message timestamp
        iso_timestamp = data.edited_message.date.isoformat()
        live_period = data.edited_message.location.live_period
        latitude = data.edited_message.location.latitude
        longitude = data.edited_message.location.longitude
        heading = data.edited_message.location.heading
        horizontal_accuracy = data.edited_message.location.horizontal_accuracy
        async with aiosqlite.connect('../db/animal_monitor.db') as db:
            query = f'SELECT id FROM user WHERE telegram_id = {user_id};'
            user_id_data = await db.execute(query)
            user_id_row = await user_id_data.fetchall()
            await db.commit()
            if len(user_id_row) == 1:
                user_id = user_id_row[0][0]
                tracking_query = f"INSERT INTO user_tracking(user_id, message_id, latitude, longitude, " \
                                 f"system_timestamp, date, live_period, heading, horizontal_accuracy) " \
                                 f"VALUES('{user_id}', '{message_id}', '{latitude}', '{longitude}', " \
                                 f"'{system_timestamp}', '{iso_timestamp}', '{live_period}', '{heading}', " \
                                 f"'{horizontal_accuracy}');"
                inserted_data = await db.execute(tracking_query)
                await db.commit()
            else:
                warn('User is not in DB')

    async def message_handler(self, parsed_response_message):
        result_object = TelegramResult.parse_obj(result)
        if result_object.message.text == '/start':
            await self.send_message(chat_id=result_object.message.chat.id, text=START_MESSAGE_TEXT)

    async def send_message(self, chat_id, text):
        url = self.send_message_command.format(chat_id=chat_id, message_text=text)
        await self.async_request(session_kwargs={}, request_kwargs={'method': 'POST', 'url': url})

    async def resolve_update(self, update_id):
        query = f"UPDATE proceeded_messages SET is_resolved = '{1}' " \
                f"WHERE update_id = '{update_id}';"
        async with aiosqlite.connect('../db/animal_monitor.db') as db:
            await db.execute(query)
            await db.commit()
        self.update_polls_command = self.root.format(method='getUpdates') + f'?offset={update_id + 1}'

    @staticmethod
    async def track_update(update_id):
        async with aiosqlite.connect('../db/animal_monitor.db') as db:
            query = f"INSERT OR IGNORE INTO proceeded_messages (update_id) VALUES('{update_id}');"
            await db.execute(query)
            await db.commit()

    async def is_update_resolved(self, update_id):
        async with aiosqlite.connect('../db/animal_monitor.db') as db:
            query = f"SELECT is_resolved FROM proceeded_messages WHERE update_id = '{update_id}';"
            query_result = await db.execute(query)
            await db.commit()
            is_resolved = await query_result.fetchall()
            if len(is_resolved) == 0:
                return False
            if len(is_resolved) == 1 and is_resolved[0][0] == 1:
                self.update_polls_command = self.root.format(method='getUpdates') + f'?offset={update_id + 1}'
                return True
            else:
                return False

    @staticmethod
    async def get_user_tracking_id(user_id):
        last_tracking_state = f'SELECT user_tracking.id, user_id, message_id, user_tracking.date, ' \
                              f'user_tracking.live_period FROM user_tracking ' \
                              f'LEFT JOIN user ' \
                              f'ON user_tracking.user_id = user.id ' \
                              f'WHERE user.telegram_id = {user_id} ORDER BY user_tracking.id DESC LIMIT 1;'
        async with aiosqlite.connect('../db/animal_monitor.db') as db:
            result = await db.execute(last_tracking_state)
            data = await result.fetchall()
            await db.commit()
        if len(data) == 1:
            return data[0]
        else:
            print('set geoсode')

    async def get_pet_params(self, current_message, chat_id):
        tracking_id, user_id, message_id, \
            date, live_period = await TelegramBot.get_user_tracking_id(current_message.from_.id)
        correct_data = datetime.fromisoformat(date) + timedelta(live_period)
        if correct_data <= datetime.now(correct_data.tzinfo):
            message = 'Сессия истекла, отправьте новую геопозицию'
            await self.send_message(chat_id, text=message)
            # session is ended
            await update_state(user_id, 9)
            return None
        photo = {'size': -1, 'file_id': ''}
        for photo_file in current_message.photo:
            if photo_file.file_size > photo['size']:
                photo['size'] = photo_file.file_size
                photo['file_id'] = photo_file.file_id
        url = self.get_file_step_1.format(file_id=photo['file_id'])
        inner_path = await TelegramBot.get_photo_url(url, self.get_file_step_2)
        return inner_path

    @staticmethod
    async def async_content_request(session_kwargs, request_kwargs):
        async with aiohttp.ClientSession(**session_kwargs) as session:
            async with session.request(**request_kwargs) as response:
                return await response.read()

    @staticmethod
    async def get_photo_url(url_with_file_id, second_step_path):
        response = await TelegramBot.async_request(session_kwargs={},
                                                   request_kwargs={'method': 'POST',
                                                                   'url': url_with_file_id})
        valid_response = TelegramPhotoPathResponse.parse_obj(response)
        if not valid_response.ok:
            raise Exception('Check response status for image')
        timestamp = datetime.now().date().isoformat()
        data_path = f"../data/{timestamp}/{valid_response.result.file_path.replace('/', '_')}"
        loop = asyncio.get_running_loop()

        with concurrent.futures.ProcessPoolExecutor() as pool:
            try:
                await loop.run_in_executor(pool, os.listdir, f'../data/{timestamp}/')
            except FileNotFoundError:
                await loop.run_in_executor(pool, os.mkdir, f'../data/{timestamp}/')
        last_path = second_step_path.format(file_path=valid_response.result.file_path)
        async with aiofiles.open(data_path, 'wb') as f:
            content = await TelegramBot.async_content_request(session_kwargs={},
                                                              request_kwargs={'method': 'GET',
                                                                              'url': last_path})
            await f.write(content)
        return data_path


if __name__ == '__main__':
    bot = TelegramBot(TELEGRAM_TOKEN)
    asyncio.run(bot.update_polls())
