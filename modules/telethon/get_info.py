from modules.telethon.init import client


async def get_user_from_username(username: str):
    user = await client.get_entity(username)
    return user
