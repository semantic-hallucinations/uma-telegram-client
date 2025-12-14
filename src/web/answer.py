from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest

from .client import N8nClient

from app.context import bot_context, web_context
from utils.formatters import clean_tags


async def handle_agent_answer(query: str, message: Message):
    # await message.answer("Арбузный привет! \n Твоё сообщение: " + message.text + 
    #                      "\n Мой контекст: " + query)
    # return
    
    answer = await N8nClient.get_answer(query)

    answer_format: str = web_context.n8n_answer_format
    msg_parse_mode = bot_context.supported_parse_modes[answer_format]

    try:
        await message.answer(answer, parse_mode=msg_parse_mode) 
    
    except TelegramBadRequest:

        await message.answer(clean_tags(answer, answer_format)) 

