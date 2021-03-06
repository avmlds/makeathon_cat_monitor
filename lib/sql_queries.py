INSERT_UPDATES = '''INSERT OR IGNORE INTO telegram_updates(status,
                                update_id,
                                message_id,
                                message_from_id,
                                message_from_is_bot,
                                message_from_first_name,
                                message_from_username,
                                message_from_language_code,
                                message_chat_id,
                                message_chat_first_name,
                                message_chat_username,
                                message_chat_type,
                                date,
                                latitude,
                                longitude,
                                text,
                                entities_offset,
                                entities_length,
                                entities_type)
VALUES (
'%(status)s',
'%(update_id)s',
'%(message_id)s',
'%(message_from_id)s',
'%(message_from_is_bot)s',
'%(message_from_first_name)s',
'%(message_from_username)s',
'%(message_from_language_code)s',
'%(message_chat_id)s',
'%(message_chat_first_name)s',
'%(message_chat_username)s',
'%(message_chat_type)s',
'%(date)s',
'%(latitude)s',
'%(longitude)s',
'%(text)s',
'%(entities_offset)s',
'%(entities_length)s',
'%(entities_type)s'
);'''


CHECK_IS_ANSWERED = "SELECT message_chat_id, message_id, is_answered FROM telegram_updates " \
                    "WHERE message_id = {message_id} AND message_chat_id = {chat_id};"
UPDATE_ANSWERED = "UPDATE telegram_updates SET is_answered = 'True' WHERE message_id = {message_id} " \
                  "AND message_chat_id = {chat_id};"
