from typing import List

import asyncio
from aiogram import Bot, Dispatcher, Router

from config import Config, load_config
from app.AppContext import BotContext
from log import init_logging

#Application container class
class Application:
    _config: Config
    _bot: Bot
    _dispatcher: Dispatcher
    _routers: List[Router]

    def __init__(self):
        #init bot
        self._bot = Bot(
            token=self.config.tg_Bot.token
        )
        self._dispatcher = Dispatcher()

        #setup enviroment
        self.config = load_config()
        init_logging()


    @property
    def bot_context(self) -> BotContext:
        #set bot username into context
        username = self._config.tg_Bot.username

        #set router map into context
        routers_map = {}
        for router in self._routers:
            routers_map[router.name] = router

        return BotContext(
            _username=username,
            _router_map=routers_map)


    #run bot event loop
    def start(self, webhook=False | None):
        #TODO: congigure webhook
        # if webhook:
        #     pass

        asyncio.run(self._start_polling())

    def set_routers(self, routers: list[Router]):
        self._dispatcher.include_routers(routers)

    def set_error_handler(self, handler):
        self._dispatcher.errors.register(handler)

    async def _run_polling(self):
        await self._bot.delete_webhook(drop_pending_updates=True)
        await self._dispatcher.start_polling(self._bot)


   