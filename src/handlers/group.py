from aiogram import F, Router
from aiogram.types import Message

from app.routing import group_router
from web.answer import handle_agent_answer
from utils import log_handler
from app.context import bot_context

rt: Router = group_router


@rt.message(F.reply_to_message, F.text)
@log_handler("bot.handlers")
async def reply_message(message: Message):
    msg_text = __strip_bot_username(message.text)
    
    if msg_text:
        replied_text = __strip_bot_username(message.reply_to_message.text) 
        query = "QUOTE: " + replied_text + " QUERY: " + msg_text
        await handle_agent_answer(query, message)


@rt.message(F.text)
@log_handler("bot.handlers")
async def text_message(message: Message):
    query = __strip_bot_username(message.text)
    
    if query:
        await handle_agent_answer(query, message)


def __strip_bot_username(text: str) -> str:
    return text.replace(bot_context.tagged_username, "").strip()

@rt.message(~F.text)
@log_handler("bot.handlers")
async def non_text_message(message: Message):
    await message.answer(
        text="На данный момент бот работает только с текстовыми запросами."
    )

