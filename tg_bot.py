import subprocess
import asyncio
import os
from typing import Final

from dotenv import load_dotenv

import logging

from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command


load_dotenv()
TOKEN_TG: Final[str] = os.getenv('TOKEN_TG')
CHANNEL_ID: Final[str] = os.getenv('TG_CHANNEL')

message_to_push = []


logging.basicConfig(level=logging.INFO)
bot = Bot(
    token=TOKEN_TG,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


async def run_tg_bot() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Hi! Send the message you want to push than select action.")


def get_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text="Push to Discord", callback_data="act_ds")],
        [types.InlineKeyboardButton(text="Push to Telegram", callback_data="act_tg")],
        [types.InlineKeyboardButton(text="Push both", callback_data="act_both")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def tg_channel_message(text: str):
    await bot.send_message(CHANNEL_ID, text)


@dp.message(F.text)
async def act_text(message: types.Message):
    message_to_push.append(message.text)
    await message.answer(
        "Upload successful!\n"
        "Select action.",
        reply_markup=get_keyboard()
    )


@dp.callback_query(F.data.startswith("act_"))
async def callbacks_act(callback: types.CallbackQuery):
    if not message_to_push:
        await callback.answer(
            text="Please upload new message.",
            show_alert=True
        )
        return

    action = callback.data.split("_")[1]

    if action == "ds":
        subprocess.call(["python", "ds_bot.py", str(message_to_push[0])])
        message_to_push.clear()

    if action == "tg":
        await tg_channel_message(str(message_to_push[0]))
        message_to_push.clear()

    if action == "both":
        await tg_channel_message(str(message_to_push[0]))
        subprocess.call(["python", "ds_bot.py", str(message_to_push[0])])
        message_to_push.clear()

    await callback.answer(
        text="Done!",
        show_alert=True
    )


if __name__ == '__main__':
    asyncio.run(run_tg_bot())
