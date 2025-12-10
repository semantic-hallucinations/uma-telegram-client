from aiogram.filters import BaseFilter
from aiogram.types import Message
from app import BotContext


class IsBotMentioned(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        entities = message.entities or []
        for entity in entities:
            if entity.type == "mention" and message.text[entity.offset:entity.offset+entity.length] == BotContext.tagged_username:
                return True
        
        return False