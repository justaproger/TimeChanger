# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import datetime
import asyncio
from telethon.sync import TelegramClient
from telethon.tl import functions, types

# Функция для склонения слов
def plural_form(n, forms):
    if n%10==1 and n%100!=11:
        return forms[0]
    elif 2<=n%10<=4 and (n%100<10 or n%100>=20):
        return forms[1]
    else:
        return forms[2]

async def create_image():
    # Создаем клиент Telegram
    client = TelegramClient('my_session', api_id='1839181', api_hash='d4cd79a3fb11d5fe2d827d0b93219778')
    await client.start()
    

    while True:
        # Создаем изображение с черным фоном
        img = Image.new('RGB', (500, 500), color = (0, 0, 0))

        d = ImageDraw.Draw(img)
        fnt = ImageFont.truetype("font.ttf", 32, encoding='UTF-8')

        # Вычисляем, сколько времени осталось до Нового года
        now = datetime.datetime.now()
        new_year = datetime.datetime(year=now.year+1, month=1, day=1)
        remaining = new_year - now
        
        # Форматируем оставшееся время без секунд
        days = remaining.days
        hours, remainder = divmod(remaining.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        remaining_str = f'{days} {plural_form(days, ["день", "дня", "дней"])} {hours} {plural_form(hours, ["час", "часа", "часов"])} {minutes} {plural_form(minutes, ["минута", "минуты", "минут"])}'

        # Вычисляем размеры текста
        text_width, text_height = fnt.getbbox(remaining_str)[2:4]

        # Вычисляем позицию текста
        text_x = (img.width - text_width) / 2
        text_y = (img.height - text_height) / 2

        # Добавляем текст на изображение
        d.text((text_x, text_y+text_height - 100), f'Осталось до Нового года:\n {remaining_str}', font=fnt, fill=(0, 255, 0))

        # Добавляем текущее время на изображение
        current_time_str = datetime.datetime.now().strftime("%H:%M")
        d.text((img.width/2, text_y + text_height), f'({current_time_str})', font=fnt, fill=(0, 255, 0), anchor="mm")
        # Сохраняем изображение
        img.save('newyear.png')

        # Получаем текущие профильные фотографии
        photos = await client.get_profile_photos('me')

        # Если есть профильные фотографии, удаляем последнюю
        if photos:
            await client(functions.photos.DeletePhotosRequest(id=[photos[0]]))

        # Загружаем новую профильную фотографию
        file = await client.upload_file('newyear.png')
            await client(functions.photos.UploadProfilePhotoRequest(file=file))

        # Ждем одну минуту
        await asyncio.sleep(60)

    await client.stop()

# Запускаем функцию create_image
asyncio.run(create_image())
