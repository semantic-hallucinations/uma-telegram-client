import functools
from config import get_logger

def log_handler(logger_name: str = "bot.handlers"):

    logger = get_logger(logger_name)

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):

            user_id = "unknown"
            if args:
                event = args[0]
                
                if hasattr(event, "from_user") and event.from_user:
                    user_id = event.from_user.id

            logger.info(f"Handler {func.__name__} started for user {user_id}")
            
            try:
                result = await func(*args, **kwargs)
                logger.info(f"Handler {func.__name__} finished success")
                return result
            
            except Exception as e:
                logger.error(f"Error in handler {func.__name__}: {e}")
                raise e 
        
        return wrapper
    return decorator