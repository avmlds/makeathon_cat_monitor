import asyncio
import aiohttp
import aiosqlite
from lib.secret import TELEGRAM_TOKEN
from lib.models import TelegramUpdateResponse, TelegramMessageResult
from lib.sql_queries import INSERT_UPDATES, UPDATE_ANSWERED, CHECK_IS_ANSWERED
from messages.message_texts import START_MESSAGE_TEXT
from datetime import datetime
from warnings import warn


class TelegramBot:
    def __init__(self, token):
        self.root = f'https://api.telegram.org/bot{token}/' + '{method}'
        self.update_polls_command = self.root.format(method='getUpdates')
        self.send_message_method = 'sendMessage?chat_id={chat_id}&text={message_text}&parse_mode=HTML'
        self.send_message_command = self.root.format(method=self.send_message_method)
        self.get_file_step_1 = self.root.format(method='getFile?file_id={file_id}')
        self.query = []
        self.updates = []

    @staticmethod
    async def async_request(session_kwargs, request_kwargs):
        async with aiohttp.ClientSession(**session_kwargs) as session:
            async with session.request(**request_kwargs) as response:
                return await response.json()

    async def update_polls(self):
        while True:
            await asyncio.sleep(5)
            response = await TelegramBot.async_request(session_kwargs={},
                                                       request_kwargs={'method': 'POST',
                                                                       'url': self.update_polls_command})
            parsed_response = TelegramUpdateResponse.parse_obj(response)
            if not parsed_response.ok:
                raise Exception('Status is not OK')

            for data in parsed_response.result:
                if await TelegramBot.is_update_resolved(data.update_id):
                    continue
                await TelegramBot.track_update(update_id=data.update_id)

                if data.message is not None:
                    update_id = data.update_id
                    telegram_id = data.message.from_.id
                    message_id = data.message.message_id
                    chat_id = data.message.chat.id
                    if data.message.location is not None and data.message.location.live_period is not None:
                        # start_tracking
                        await self.start_tracking_user(data=data)

                    elif data.message.location is not None and data.message.location.live_period is None:
                        await self.send_message(chat_id=chat_id, text='Вы должны отправить отслеживание ' \
                                                                      'геопозиции, а не одиночную геопозицию')

                else:
                    telegram_id = data.edited_message.from_.id
                    update_id = data.update_id
                    chat_id = data.edited_message.chat.id
                    message_id = data.edited_message.message_id

                    if data.edited_message.location is not None \
                            and data.edited_message.location.live_period is not None \
                            and data.edited_message.location.heading is not None:
                        await TelegramBot.continue_tracking_user(data=data)

                checked_user = await self.check_user_in_db(telegram_id=telegram_id, chat_id=chat_id)
                if not checked_user[0]:
                    await TelegramBot.resolve_update(update_id=data.update_id)
                    continue
                await TelegramBot.resolve_update(update_id=data.update_id)
                print(data)

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

    async def make_active(self, telegram_id, chat_id):
        async with aiosqlite.connect('../db/animal_monitor.db') as db:
            res = await db.execute(f'INSERT INTO user VALUES( id, is_active FROM user '
                                   f'WHERE telegram_id = {telegram_id};')

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
                     f" '{True}');"
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

    @staticmethod
    async def resolve_update(update_id):
        async with aiosqlite.connect('../db/animal_monitor.db') as db:
            query = f"UPDATE proceeded_messages SET is_resolved = '{True}' " \
                    f"WHERE update_id = '{update_id}';"
            await db.execute(query)
            await db.commit()

    @staticmethod
    async def track_update(update_id):
        async with aiosqlite.connect('../db/animal_monitor.db') as db:
            query = f"INSERT OR IGNORE INTO proceeded_messages (update_id) VALUES('{update_id}');"
            await db.execute(query)
            await db.commit()

    @staticmethod
    async def is_update_resolved(update_id):
        async with aiosqlite.connect('../db/animal_monitor.db') as db:
            query = f"SELECT is_resolved FROM proceeded_messages WHERE update_id = '{update_id}';"
            query_result = await db.execute(query)
            await db.commit()
            is_resolved = await query_result.fetchall()
            if len(is_resolved) == 0:
                return False
            if len(is_resolved) == 1 and is_resolved[0][0] == 'True':
                return True
            else:
                return False


if __name__ == '__main__':
    bot = TelegramBot(TELEGRAM_TOKEN)
    asyncio.run(bot.update_polls())
