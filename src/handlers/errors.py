from aiogram.types import ErrorEvent

from config import get_logger


logger = get_logger("bot.handlers")

async def service_error_handler(event: ErrorEvent):
    logger.error(f"External API Error: {event.exception}", exec_info=True )
    
    if event.update.message:
        await event.update.message.answer(
            "😔 Сервис временно недоступен или перегружен. Пожалуйста, попробуйте через пару минут."
        )

async def global_error_handler(event: ErrorEvent):
    logger.error(f"Critical error caused by {event.exception}", exc_info=True)
    
    if event.update.message:
        await event.update.message.answer("Извините, произошла внутренняя ошибка.")


