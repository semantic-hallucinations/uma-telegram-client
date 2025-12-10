from aiogram import F, Router
from aiogram.enums import ChatType, ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from app import routers
from .answer import handle_agent_answer


rt: Router = routers["group_chat"]


@rt.message(F.reply_to_message, F.text)
async def reply_message(message: Message):
    replied_text = message.reply_to_message.text
    query = __has_context(replied_text + " " + message.text)
    
    if query:
        await handle_agent_answer(query, message)


@rt.message(F.test)
async def text_message(message: Message):
    query = __has_context(message.text)
    
    if query:
        await handle_agent_answer(message.text, message)


def __has_context(message: str) -> str:
    return message.split(maxsplit=1)[1] if len(message.split()) > 1 else ""


@rt.message(~F.text)
async def non_text_message(message: Message):
    await message.answer(
        text="На данный момент бот работает только с текстовыми запросами."
    )

