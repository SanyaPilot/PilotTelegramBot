from modules.telethon.init import client
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from loguru import logger


async def join_chat(chat_id):
    try:
        try:
            await client(JoinChannelRequest(chat_id))
        except Exception:
            await client(ImportChatInviteRequest(chat_id))
        logger.info(f'Helper successfully joined chat {chat_id}')
        return True
    except Exception as err:
        logger.error(f'Helper failed to join to chat with error:\n{err}')
        return False
