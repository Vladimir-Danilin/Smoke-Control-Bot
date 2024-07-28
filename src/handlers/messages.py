from config import *

from aiogram import types, Router, F
from aiogram.types import Message
import pandas as pd

router = Router()
conn = connect()

@router.message(F.text.lower() == "профиль")
async def profile_stat(message: types.Message) -> None:
    name = await conn.fetch(f"select login from users where tg_login = '{message.from_user.full_name}'")
    days = await conn.fetch(f"select days from users where tg_login = '{message.from_user.full_name}'")
    best_days_count = await conn.fetch(
        f"select best_days_count from users where tg_login = '{message.from_user.full_name}'")

    await message.answer(
        f"Ваш профиль {name[0][0]}\nвыжито дней {days[0][0]}\nмаксимально выжито дней {best_days_count[0][0]}")


@router.message(F.text.lower() == 'новый день')
async def new_day(message: Message) -> None:
    current_days = await conn.fetch(f"select days from users where chat_id = '{message.from_user.id}'")
    await conn.fetch(f"UPDATE users set days = {current_days[0][0] + 1} where chat_id = '{message.from_user.id}'")
    await conn.fetch(
        f"UPDATE users set best_days_count = {current_days[0][0]+1} where chat_id = '{message.from_user.id}' and best_days_count < days")

    quotations = pd.read_csv('./../../data/quotations.csv')
    quotation = quotations.sample()
    await message.answer(f"цитата дня {quotation['author'].values[0]} говорил, {quotation['comment'].values[0]}")


@router.message(F.text.lower() == 'заново')
async def retry(message: Message) -> None:
    current_days = await conn.fetch(f"select days from users where chat_id = '{message.from_user.id}'")
    await conn.fetch(f"UPDATE users set best_days_count = {current_days[0][0]} where chat_id = '{message.from_user.id}' and best_days_count < days")
    await conn.fetch(
        f"UPDATE users set days = 1 where chat_id = '{message.from_user.id}'")

    quotations = pd.read_csv('./../../data/quotations.csv')
    quotation = quotations.sample()
    await message.answer(f"цитата дня {quotation['author'].values[0]} говорил, {quotation['comment'].values[0]}")