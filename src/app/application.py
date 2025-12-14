from typing import List

import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import ExceptionTypeFilter

from config import Config, load_config, setup_logging, get_logger
from .routing import routers
from handlers.errors import global_error_handler, service_error_handler
from exceptions import ServiceUnavailableError
from web.client import N8nClient

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
        self._dispatcher.shutdown.register(self._on_shutdown)
 
        self._set_routers()
        self._set_error_handling()

        logger.debug("Application initialized successfully")


    #run bot event loop
    def start(self, webhook: bool | None = None):
        logger.info("Starting bot")
        #TODO: congigure webhook
        # if webhook:
        #     pass

        asyncio.run(self._run_polling())


    def _set_routers(self):
        logger.debug("Set routers")
        self._dispatcher.include_routers(*routers)

    def _set_error_handling(self):
        logger.debug("Set error handler")

        self._dispatcher.errors.register(
            service_error_handler,
            ExceptionTypeFilter(ServiceUnavailableError)
            )
        
        self._dispatcher.errors.register(
            global_error_handler
        )

    async def _run_polling(self):
        logger.debug("Run polling")
        await self._bot.delete_webhook(drop_pending_updates=True)
        await self._dispatcher.start_polling(self._bot)

    async def _on_shutdown(self):
        await N8nClient.close()
        logger.debug("N8n client closed")

application = Application()
