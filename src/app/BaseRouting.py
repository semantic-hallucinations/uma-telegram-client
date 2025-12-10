from aiogram import Router, F
from aiogram.enums import ChatType

from filters import IsBotMentioned

private_chat_router = Router("private_chat")
private_chat_router.message.filter(ChatType.PRIVATE)
private_chat_router.message.middleware() #TODO: set middleware for rate limiting

group_chat_router = Router("group_chat")
group_chat_router.message.filter(ChatType.GROUP, 
                                 ChatType.SUPERGROUP,
                                 IsBotMentioned)
group_chat_router.message.middleware()#TODO: set middleware for rate limiting

routers = [private_chat_router, 
           group_chat_router]
