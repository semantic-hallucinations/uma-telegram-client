from aiogram import Router, F
from aiogram.enums import ChatType

from .filters import IsBotMentioned
from middlewares import RateLimiter


#init routers
private_router = Router(name="private")
group_router = Router(name="group")

#set filters
private_router.message.filter(F.chat.type == ChatType.PRIVATE)
group_router.message.filter(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))
group_router.message.filter(IsBotMentioned())

#set middlewares
global_middleware = RateLimiter()
private_router.message.middleware(global_middleware)
group_router.message.middleware(global_middleware)


routers = [private_router, group_router]
