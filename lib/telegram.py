import asyncio
import aiohttp
import aiosqlite
from lib.secret import TELEGRAM_TOKEN
from lib.models import TelegramUpdateResponse, TelegramMessageResult
from lib.sql_queries import INSERT_UPDATES, UPDATE_ANSWERED, CHECK_IS_ANSWERED
from messages.message_texts import START_MESSAGE_TEXT
from datetime import datetime


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
            await asyncio.sleep(3)
            response = await TelegramBot.async_request(session_kwargs={},
                                                       request_kwargs={'method': 'POST',
                                                                       'url': self.update_polls_command})
            parsed_response = TelegramUpdateResponse.parse_obj(response)
            if not parsed_response.ok:
                raise Exception('Status is not OK')
            for data in parsed_response.result:
                if data.message is not None:
                    telegram_id = data.message.from_.id
                    chat_id = data.message.from_.id

                    if data.message.location is not None and data.message.location.live_period is not None:
                        # start_tracking
                        await self.start_tracking_user(data=data)

                else:
                    telegram_id = data.edited_message.from_.id
                    chat_id = data.edited_message.from_.id
                    if data.edited_message.location is not None \
                            and data.edited_message.location.live_period is not None \
                            and data.edited_message.location.heading is not None:
                        await self.continue_tracking_user(data=data)

                checked_user = await self.check_user_in_db(telegram_id=telegram_id, chat_id=chat_id)
                if not checked_user[0]:
                    continue

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

            print(parsed_response)

    async def check_user_in_db(self, telegram_id, chat_id):
        async with aiosqlite.connect('../db/animal_monitor.db') as db:
            res = await db.execute(f'SELECT id, is_active FROM user WHERE telegram_id = {telegram_id}')
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
            res = await db.execute(
                f'INSERT INTO user VALUES( id, is_active FROM user WHERE telegram_id = {telegram_id}')

    async def start_tracking_user(self, data):
        user_id = data.message.from_.id
        username = data.message.from_.username
        first_name = data.message.from_.first_name
        message_id = data.message.message_id
        # telegram message timestamp
        iso_timestamp = data.message.date.isoformat()
        live_period = data.message.location.live_period
        latitude = data.message.location.latitude
        longitude = data.message.location.longitude
        heading = data.message.location.heading
        horizontal_accuracy = data.message.location.horizontal_accuracy

        user_query = f"INSERT OR IGNORE INTO user(telegram_id, username, first_name, date, live_period, is_active) " \
                     f"VALUES('{user_id}', '{username}', '{first_name}', '{iso_timestamp}', '{live_period}'," \
                     f" '{True}');"
        async with aiosqlite.connect('../db/animal_monitor.db') as db:
            query_id_ = await db.execute(user_query)
            await db.commit()
            last_row_id = query_id_.lastrowid
        async with aiosqlite.connect('../db/animal_monitor.db') as db:
            tracking_query = f"INSERT INTO user_tracking(user_id, message_id, latitude, longitude, " \
                             f"date, live_period, heading, horizontal_accuracy) " \
                             f"VALUES('{last_row_id}', '{message_id}', '{latitude}', '{longitude}', " \
                             f"'{iso_timestamp}', '{live_period}', '{heading}', '{horizontal_accuracy}');"
            inserted_data = await db.execute(tracking_query)
            await db.commit()

            u = 38 / 1

    async def continue_tracking_user(self, data):
        user_id = data.edited_message.from_.id
        username = data.edited_message.from_.username
        first_name = data.edited_message.from_.first_name
        message_id = data.edited_message.message_id
        # telegram message timestamp
        iso_timestamp = data.edited_message.date.isoformat()
        live_period = data.edited_message.location.live_period
        latitude = data.edited_message.location.latitude
        longitude = data.edited_message.location.longitude
        heading = data.edited_message.location.heading
        horizontal_accuracy = data.edited_message.location.horizontal_accuracy
        async with aiosqlite.connect('../db/animal_monitor.db') as db:
            query = f'SELECT id FROM user WHERE telegram_id = {user_id}'
            user_id_data = await db.execute(query)
            user_id_row = await user_id_data.fetchall()
            await db.commit()
            if len(user_id_row) == 1:
                user_id = user_id_row[0][0]
                async with aiosqlite.connect('../db/animal_monitor.db') as db:
                    tracking_query = f"INSERT INTO user_tracking(user_id, message_id, latitude, longitude, " \
                                     f"date, live_period, heading, horizontal_accuracy) " \
                                     f"VALUES('{user_id}', '{message_id}', '{latitude}', '{longitude}', " \
                                     f"'{iso_timestamp}', '{live_period}', '{heading}', '{horizontal_accuracy}');"
                    inserted_data = await db.execute(tracking_query)
                    await db.commit()
            else:
                raise Exception('User is not in DB')

    async def message_handler(self, parsed_response_message):
        result_object = TelegramResult.parse_obj(result)
        if result_object.message.text == '/start':
            await self.send_message(chat_id=result_object.message.chat.id,
                                    text=START_MESSAGE_TEXT)

    async def send_message(self, chat_id, text):
        """
        This func create POST-request and sends it to a Telegram server
        As a result, user with necessary chat_id will receive message with
        'text'.
        :param chat_id: integer
        :param text: string
        :return: POST-request to a Telegram server
        """
        url = self.send_message_command.format(chat_id=chat_id, message_text=text)
        await self.async_request(session_kwargs={}, request_kwargs={'method': 'POST', 'url': url})


if __name__ == '__main__':
    bot = TelegramBot(TELEGRAM_TOKEN)
    asyncio.run(bot.update_polls())
