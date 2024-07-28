from config import *

from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import Message, Bot
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder

router = Router()
conn = connect()

@router.message(Command('top'))
async def top_users(message: types.Message) -> None:
    name = await conn.fetch(f"select login from users")
    best_days = await conn.fetch(f"select best_days_count from users")
    text = ''

    for i in range(0, len(name)):
        if best_days[i][0] == 1:
            text += f'{i + 1} {name[i][0]} {best_days[i][0]} день\n'
        elif best_days[i][0] < 5:
            text += f'{i + 1} {name[i][0]} {best_days[i][0]} дня\n'
        elif best_days[i][0] < 20:
            text += f'{i + 1} {name[i][0]} {best_days[i][0]} дней\n'
        else:
            text += f'{i + 1} {name[i]} {best_days[i]} дня\n'
    await message.reply(text=text)


@router.message(Command('say'))
async def notification(message: Message, bot: Bot) -> None:
    if message.from_user.id in admin_ids:
        user_ids = await conn.fetch('select chat_id from users')

        new_day_button = types.KeyboardButton(text='Новый день')
        retry_button = types.KeyboardButton(text='Заново')

        reply_keybord_builder = ReplyKeyboardBuilder()
        reply_keybord_builder.add(new_day_button)
        reply_keybord_builder.add(retry_button)

        for i in user_ids:
            await bot.send_message(
                text=f"Если вы продержались ещё один день без никотина нажмите новый день, а если нет то заново",
                reply_markup=reply_keybord_builder.as_markup(resize_keyboard=True,
                                                             input_field_placeholder='ещё один день без никотина',
                                                             one_time_keyboard=True),
                                                             chat_id=i[0])


