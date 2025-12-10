from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

from app import routers
from .answer import handle_agent_answer

rt: Router = routers["private_chat"]

@rt.message(CommandStart())
async def command_start(message: Message):
    await message.answer(
        text=(
            "Я - бот-ассистент Белорусского государственного"
            " университета информатики и радиоэлектроники.\n"
            "Готов ответить на все вопросы об университете!"
        )
    )


@rt.message(Command(commands="help"))
async def command_help(message: Message):
    await message.answer(
        text=(
            "Вы можете задать мне любой интересующий вас вопрос"
            " по поводу поступления или учебы в БГУИР."
            " Напишите мне сообщение."
        )
    )

@rt.message(F.reply_to_message, F.text)
async def reply_message(message: Message):
    replied_text = message.reply_to_message.text
    query = replied_text + " " + message.text

    await handle_agent_answer(query, message)


@rt.message(F.test)
async def text_message(message: Message):
    await handle_agent_answer(message.text, message)

@rt.message(~F.text)
async def non_text_message(message: Message):
    await message.answer(
        text="На данный момент бот работает только с текстовыми запросами."
    )

