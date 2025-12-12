from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest

from .client import N8nClient


async def handle_agent_answer(query: str, message: Message):
    # await message.answer("Арбузный привет! \n Твоё сообщение: " + message.text + 
    #                      "\n Мой контекст: " + query)
    # return

    answer = await N8nClient.get_answer(query) 
    try:
        await message.answer(answer) #TODO: add parsemode if necessary
    
    except TelegramBadRequest:
        await message.answer(answer) #TODO: add fallback formatting if necessary

