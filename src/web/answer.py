import asyncio
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest

from .client import n8n_client, event_storage_client

from app.context import bot_context, web_context
from app.enums import EventInitiator, EventType
from utils.formatters import clean_tags


async def handle_agent_answer(query: str, message: Message):
    # await message.answer("Арбузный привет! \n Твоё сообщение: " + message.text + 
    #                      "\n Мой контекст: " + query)
    # return
    
    #save user message event
    user_id = message.from_user.id

    asyncio.create_task(
        event_storage_client.save_event(
            telegram_user_id=user_id,
            initiator="EventInitiator.USER",       
            event_type="EventType.MESSAGE", 
            content=query
        )
    )
    
    try:
        answer = await n8n_client.get_answer(query)
    except Exception as e:
        await message.answer("Извините, сервис временно недоступен.")
        
        asyncio.create_task(
            event_storage_client.save_event(
                telegram_user_id=user_id,
                initiator="SYSTEM",
                event_type="ERROR",
                content=f"N8n Error: {str(e)}"
            )
        )
        return

    answer_format: str = web_context.n8n_answer_format
    msg_parse_mode = bot_context.supported_parse_modes.get(answer_format)

    final_answer_text = answer
    try:
        await message.answer(answer, parse_mode=msg_parse_mode) 
    
    except TelegramBadRequest:
        final_answer_text = clean_tags(answer, answer_format)
        await message.answer(final_answer_text)
        
    finally:
        asyncio.create_task(
        event_storage_client.save_event(
            telegram_user_id=user_id,
            initiator=EventInitiator.ASSISTANT,   
            event_type=EventType.MESSAGE,      
            content=final_answer_text
        )
    )

    

