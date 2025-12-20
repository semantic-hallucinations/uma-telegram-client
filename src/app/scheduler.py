import asyncio
from config import get_logger
from web.client import event_storage_client

logger = get_logger("bot.scheduler")

class BackgroundTasks:

    def __init__(self):
        self.tasks = set()

    def add(self, coro):

        task = asyncio.create_task(coro)
        self.tasks.add(task)
        
        task.add_done_callback(self.tasks.discard)
        
        task.add_done_callback(self._log_exception)
        
        return task

    def _log_exception(self, task: asyncio.Task):
        try:
            exc = task.exception()
            if exc:
                logger.error(f"Background task failed: {exc}")
        except asyncio.CancelledError:
            pass




scheduler = BackgroundTasks()

def schedule_log(user_id: int, initiator: str, event_type: str, content: str = None, meta: str = None ):
    """
    Обертка для запуска фоновой задачи сохранения лога.
    Работает по принципу Fire-and-Forget.
    """
    scheduler.add(
        event_storage_client.save_event(
            telegram_user_id=user_id,
            initiator=initiator,
            event_type=event_type,
            content=content,
            meta_data=meta
        )
    )


