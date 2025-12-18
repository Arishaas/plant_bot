import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from database import init_db
from handlers.start import router as start_router
from handlers.plants import router as plants_router
from handlers.actions import router as actions_router
from handlers.fallback import router as fallback_router
from scheduler import start_scheduler


async def main():
    await init_db()

    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(plants_router)
    dp.include_router(actions_router)
    dp.include_router(fallback_router)

    asyncio.create_task(start_scheduler(bot))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
