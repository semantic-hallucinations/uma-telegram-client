from typing import List
from logging import Logger

import asyncio
from aiogram import Bot, Dispatcher, Router

from config import Config, load_config, setup_logging, get_logger
from .context import BotContext, WebContext
from .routing import routers
from handlers.errors import global_error_handler

import handlers.private
import handlers.group


logger = get_logger("bot")
#Application container class
class Application:
    _config: Config
    _bot: Bot
    _dispatcher: Dispatcher
    _routers: List[Router]


    def __init__(self):
        setup_logging()
        self._config = load_config() 

        logger.debug("Config loaded")

        self._bot = Bot(token=self._config.tg_Bot.token)
        self._dispatcher = Dispatcher()
 
        self._set_routers(routers)
        self._set_error_handler(global_error_handler)

        logger.debug("Application initialized successfully")


    @property
    def bot_context(self) -> BotContext:
        logger.debug("Create bot context")
        #set bot username into context
        username = self._config.tg_Bot.username

        return BotContext(
            _username=username)
    
    @property
    def web_context(self) -> WebContext:
        logger.debug("create web context")
        n8n_addr_url = self._config.web.n8n_url

        return WebContext(
            n8n_url=n8n_addr_url
        )


    #run bot event loop
    def start(self, webhook=False | None):
        logger.info("Starting bot")
        #TODO: congigure webhook
        # if webhook:
        #     pass

        asyncio.run(self._start_polling())


    def _set_routers(self, routers: list[Router]):
        logger.debug("Set routers")
        self._dispatcher.include_routers(routers)

    def _set_error_handler(self, handler):
        logger.debug("Set error handler")
        self._dispatcher.errors.register(handler)

    async def _run_polling(self):
        logger.debug("Run polling")
        await self._bot.delete_webhook(drop_pending_updates=True)
        await self._dispatcher.start_polling(self._bot)


application = Application()
bot_context: BotContext = application.bot_context
web_context: WebContext = application.web_context