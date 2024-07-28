from config import *

from aiogram import types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.markdown import hbold

router = Router()
conn = connect()


class Authorization(StatesGroup):
    login = State()
    end = State()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    check_sing_up_login = await conn.fetch('select tg_login from users')
    check_sing_up_chat_id = await conn.fetch('select chat_id from users')
    if message.from_user.full_name not in [i[0] for i in check_sing_up_login] \
        and message.from_user.id not in [i[0] for i in check_sing_up_chat_id]:
        await message.answer(
            'Чтобы начать использовать бота введите логин или отправь !, если хочешь оставить логин из телеграмма')
        await state.set_state(Authorization.login)
    else:
        await message.answer('Вы уже зарегистрированны')


@router.message(Authorization.login)
async def set_username(message: Message, state: FSMContext) -> None:
    await state.set_state(Authorization.end)
    check_reg = await conn.fetch(f"select chat_id from users where chat_id = '{message.from_user.id}'")
    if message.from_user.id != check_reg:
        if message.text == '!':
            async with conn.transaction():
                await conn.execute(
                    f"INSERT INTO users (login, tg_login, permission, chat_id) VALUES('{message.from_user.full_name}',
                    '{message.from_user.full_name}', 'user', '{message.from_user.id}')")

            await message.answer(
                f'Привет {hbold(message.from_user.full_name)}, твой первый день без никотина начинается')
        else:
            async with conn.transaction():
                await conn.execute(
                    f"INSERT INTO users (login, tg_login, permission, chat_id) VALUES('{message.text}', '{message.from_user.full_name}', 'user', '{message.from_user.id}')")

            await message.answer(
                f'Привет {hbold(message.text)}, твой первый день без никотина начинается')
    kb = types.KeyboardButton(text='Профиль')
    reply_keybord_builder = ReplyKeyboardBuilder()
    reply_keybord_builder.add(kb)
    km = reply_keybord_builder.as_markup(resize_keyboard=True,
                                         input_field_placeholder="по кнопке внизу вы можете увидеть свою статистику")
    await message.answer('!!!', reply_markup=km)