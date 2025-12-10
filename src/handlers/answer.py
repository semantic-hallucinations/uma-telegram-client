from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest

async def handle_agent_answer(query: str, message: Message):
    answer = ... #TODO: call to n8n api from api-cli
    try:
        await message.answer(answer) #TODO: add parsemode if necessary
    
    except TelegramBadRequest:
        await message.answer(answer) #TODO: add fallback formatting if necessary