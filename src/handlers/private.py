from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

from app.routing import private_router
from utils import log_handler
from web.answer import handle_agent_answer

from app.scheduler import schedule_log
from app.enums import EventInitiator, EventType

rt: Router = private_router


@rt.message(CommandStart())
@log_handler("bot.handlers")
async def command_start(message: Message):
    schedule_log(message.from_user.id, EventInitiator.USER, EventType.COMMAND)

    await message.answer(
        text=(
            "Я - бот-ассистент Белорусского государственного"
            " университета информатики и радиоэлектроники.\n"
            "Готов ответить на все вопросы об университете!"
        )
    )


@rt.message(Command(commands="help"))
@log_handler("bot.handlers")
async def command_help(message: Message):
    schedule_log(message.from_user.id, EventInitiator.USER, EventType.COMMAND)

    await message.answer(
        text=(
            "Вы можете задать мне любой интересующий вас вопрос"
            " по поводу поступления или учебы в БГУИР."
            " Напишите мне сообщение."
        )
    )


@rt.message(F.reply_to_message, F.text)
@log_handler("bot.handlers")
async def reply_message(message: Message):
    replied_text = message.reply_to_message.text
    query = " QUOTE: " + replied_text + " QUERY: " + message.text

    schedule_log(message.from_user.id, EventInitiator.USER, EventType.MESSAGE, query)

    await handle_agent_answer(query, message)


@rt.message(F.text)
@log_handler("bot.handlers")
async def text_message(message: Message):
    schedule_log(message.from_user.id, EventInitiator.USER, EventType.MESSAGE, message.text)

    await handle_agent_answer(message.text, message)


@rt.message(~F.text)
@log_handler("bot.handlers")
async def non_text_message(message: Message):
    await message.answer(
        text="На данный момент бот работает только с текстовыми запросами."
    )

