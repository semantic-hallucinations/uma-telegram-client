import asyncio
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest

from .client import n8n_client
from app.scheduler import schedule_log

from app.context import bot_context, web_context
from app.enums import EventInitiator, EventType
from utils.formatters import clean_tags

from config import get_logger

logger = get_logger("bot.services")

async def handle_agent_answer(query: str, message: Message):
    # await message.answer("Арбузный привет! \n Твоё сообщение: " + message.text + 
    #                      "\n Мой контекст: " + query)
    # return

    logger.info("handling agent answer")

    user_id = message.from_user.id

    try:
        answer = await n8n_client.get_answer(query) #wait for a rag-pipeline answer
    except Exception as e:
        await message.answer("Извините, сервис временно недоступен.")
        schedule_log(user_id, EventInitiator.SYSTEM, EventType.ERROR, f"N8n Error: {str(e)}")
        return

    answer_format = web_context.n8n_answer_format
    msg_parse_mode = bot_context.supported_parse_modes.get(answer_format) #parse md or html
    
    final_answer_text = answer

    try:
        await message.answer(answer, parse_mode=msg_parse_mode) #answer to user in chat
        
    except TelegramBadRequest:
        final_answer_text = clean_tags(answer, answer_format)
        await message.answer(final_answer_text) #parse error - send without formatting
        
    finally:
        schedule_log(user_id, EventInitiator.ASSISTANT, EventType.MESSAGE, final_answer_text)





    


