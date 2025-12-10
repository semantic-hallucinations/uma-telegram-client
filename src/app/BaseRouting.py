from aiogram import Router, F
from aiogram.enums import ChatType

from filters import IsBotMentioned
from middlewares import RateLimiter

private_chat_router = Router("private_chat")
private_chat_router.message.filter(ChatType.PRIVATE)
private_chat_router.message.middleware(RateLimiter)

group_chat_router = Router("group_chat")
group_chat_router.message.filter(ChatType.GROUP, 
                                 ChatType.SUPERGROUP,
                                 IsBotMentioned)
group_chat_router.message.middleware(RateLimiter)

routers = [private_chat_router, 
           group_chat_router]
