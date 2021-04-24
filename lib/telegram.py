import asyncio
import aiohttp
import aiosqlite
from lib.secret import TELEGRAM_TOKEN
from lib.models import TelegramUpdateResponse
from lib.sql_queries import INSERT_UPDATES

class TelegramBot:
    def __init__(self, token):
        self.root = 'https://api.telegram.org/bot{}/'.format(token) + '{}'
        self.update_polls_command = self.root.format('getUpdates')
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
            if not response['ok']:
                return {'Messages': 'No new'}

            for message_response in parsed_response.result:
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
                        'date': message_response.message.date.isoformat(),
                        'text': message_response.message.text}

                if message_response.message.entities is not None:
                    data.update({'entities_offset': message_response.message.entities[0].offset,
                                 'entities_length': message_response.message.entities[0].length,
                                 'entities_type': message_response.message.entities[0].type})
                else:
                    data.update({'entities_offset': None, 'entities_length': None, 'entities_type': None})

                async with aiosqlite.connect('../db/animal_monitor.db') as db:
                    await db.execute(INSERT_UPDATES % data)
                    await db.commit()

            if response['ok']:
                for result in response['result']:
                    current_loop = asyncio.get_running_loop()
                    if result['update_id'] not in self.updates:
                        pass
            print(parsed_response)


if __name__ == '__main__':
    bot = TelegramBot(TELEGRAM_TOKEN)
    asyncio.run(bot.update_polls())
