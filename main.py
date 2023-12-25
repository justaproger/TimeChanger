import asyncio
from telethon import TelegramClient, functions
from datetime import datetime

api_id = '1839181'
api_hash = 'd4cd79a3fb11d5fe2d827d0b93219778'
session = 'your_session'

async def change_name_every_minute():
    async with TelegramClient(session, api_id, api_hash) as client:
        while True:
            now = datetime.now()
            time_string = now.strftime("%H:%M")
            await client(functions.account.UpdateProfileRequest(last_name="Abdukarimov" + "["+time_string+"]"))
            await asyncio.sleep(60)

loop = asyncio.get_event_loop()
loop.run_until_complete(change_name_every_minute())
