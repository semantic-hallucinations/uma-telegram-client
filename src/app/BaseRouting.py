from aiogram import Router

private_chat_router = Router("private_chat")
group_chat_router = Router("group_chat")

routers = [private_chat_router, 
           group_chat_router]
