from aiogram.filters import BaseFilter
from aiogram.types import Message
from app import bot_context


class IsBotMentioned(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        entities = message.entities or []
        
        for entity in entities:
            if entity.type == "mention" \
                and message.text[entity.offset:entity.offset+entity.length]\
                      == bot_context.tagged_username:
                return True
            
        return False