import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from database import init_db
from handlers.start import router as start_router
from handlers.plants import router as plants_router
from handlers.actions import router as actions_router
from scheduler import start_scheduler


async def main():
    await init_db()

    bot = Bot('8587251582:AAFEHz7h-ge8pvhCwlqTm1N4eaTry9YdZOo')
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(plants_router)
    dp.include_router(actions_router)

    asyncio.create_task(start_scheduler(bot))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())