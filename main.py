import asyncio
from datetime import datetime
import pytz
from telethon import TelegramClient, functions

api_id = '1839181'
api_hash = 'd4cd79a3fb11d5fe2d827d0b93219778'
session = 'your_session'

async def time_until_new_year():
    tashkent_tz = pytz.timezone('Asia/Tashkent')
    now = datetime.now(tashkent_tz)
    new_year = datetime(year=now.year + 1, month=1, day=1, tzinfo=tashkent_tz)
    delta = new_year - now
    days, seconds = delta.days, delta.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return days, hours, minutes

async def change_last_name_every_minute():
    async with TelegramClient(session, api_id, api_hash) as client:
        while True:
            days, hours, minutes = await time_until_new_year()
            last_name = f"До Нового года осталось \n {days} дней, {hours} часов и {minutes} минут(ы)."
            await client(functions.account.UpdateProfileRequest(first_name=last_name))
            await asyncio.sleep(60)

loop = asyncio.get_event_loop()
loop.run_until_complete(change_last_name_every_minute())
