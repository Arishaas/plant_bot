import asyncio
from datetime import datetime, date
import aiosqlite
from database import get_user_plants, get_plant_default, DB


async def notify(bot, user_id, text):
    try:
        await bot.send_message(user_id, text)
    except:
        pass


async def check_and_notify(bot):
    async with aiosqlite.connect(DB) as db:
        cur = await db.execute("SELECT DISTINCT user_id FROM user_plants")
        users = [row[0] for row in await cur.fetchall()]

    for user in users:
        plants = await get_user_plants(user)

        for name, lw, lf, lt, notes in plants:
            defaults = await get_plant_default(name)
            if defaults:
                w, f, t = defaults
            else:
                w, f, t = 7, 30, 365

            def days_since(d):
                return (date.today() - datetime.fromisoformat(d).date()).days

            if days_since(lw) >= w:
                await notify(bot, user, f"Пора полить: {name}")

            ds_feed = days_since(lf)
            if ds_feed >= f:
                await notify(bot, user, f"Сегодня подкормка: {name}")
            elif f - ds_feed == 7:
                await notify(bot, user, f"Через неделю подкормка: {name}")

            if days_since(lt) >= t:
                await notify(bot, user, f"Пора пересадить: {name}")


async def start_scheduler(bot):
    while True:
        await check_and_notify(bot)
        await asyncio.sleep(60 * 60 * 24)