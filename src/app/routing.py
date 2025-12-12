from aiogram import Router, F
from aiogram.enums import ChatType

from .filters import IsBotMentioned
from middlewares import RateLimiter


#init routers
private_router = Router("private")
group_router = Router("group")

#set filters
private_router.message.filter(F.chat.type == ChatType.PRIVATE)
group_router.message.filter(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))
group_router.message.filter(IsBotMentioned)

#set middlewares
private_router.message.middleware(RateLimiter)
group_router.message.middleware(RateLimiter)


routers = [private_router, group_router]
