from src.handlers import command
from src.handlers import messages
from src.auth import authorization

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from config import TOKEN

import logging
import sys
import asyncio


async def main() -> None:
    dp = Dispatcher()
    
    dp.include_router(authorization.router)
    dp.include_router(command.router)
    dp.include_router(messages.router)

    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()