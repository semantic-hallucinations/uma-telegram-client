import asyncio
from typing import Any, Dict, Optional
import httpx

from config import get_logger
from app.context import web_context
from utils.exceptions import ServiceUnavailableError
from utils.formatters import format_json_body
from app.enums import EventInitiator, EventType

logger = get_logger("bot.services")

class BaseWebClient:
    MAX_RETRIES = 3 
    DEFAULT_TIMEOUT = httpx.Timeout(120.0, connect=5.0)

    def __init__(self, base_url: str):
        self.base_url = base_url
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.DEFAULT_TIMEOUT
            )
        return self._client

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()


    async def _request(
        self, 
        method: str, 
        endpoint: str, 
        json: Optional[Dict] = None, 
        params: Optional[Dict] = None,
        max_attempts: int = None  
    ) -> Any:
        client = await self._get_client()
        
        
        attempts_count = max_attempts if max_attempts is not None else self.MAX_RETRIES
        
        for attempt in range(1, attempts_count + 1):

            try:
                logger.info("Sending request to {method} {endpoint}")
                response = await client.request(method, endpoint, json=json, params=params)
                response.raise_for_status()
                logger.info("Request to {method} {endpoint} was sended successfully")
                return response.json()
                
            except httpx.HTTPError as e:
                
                if attempts_count > 1:
                    logger.warning(f"Request to {endpoint} failed (Attempt {attempt}/{attempts_count}): {e}")
                
                if attempt == attempts_count:
                
                    raise ServiceUnavailableError(f"Failed to communicate with {self.base_url}") from e
                
                await asyncio.sleep(2 ** (attempt - 1))


class N8nClient(BaseWebClient):
    def __init__(self):
        super().__init__(base_url=web_context.n8n_url)

    async def get_answer(self, query: str, sessionId: int) -> str:
        method = "POST"
        endpoint = "/webhook/pipeline"
        payload = {
            "query": query,
            "sessionId": sessionId
        }
        logger.info("sending request from n8n-client to {method} {endpoint}")
        data = await self._request(method, endpoint, json=payload)
        logger.info("Request from n8n-client to {method} {endpoint} successed")
        return format_json_body(data)


class EventStorageClient(BaseWebClient):
    def __init__(self):
        super().__init__(base_url=web_context.event_storage_url)

    async def save_event(
        self, 
        telegram_user_id: int, 
        initiator: str, 
        event_type: str, 
        content: str = None, 
        meta_data: Dict = None
    ) -> None:
        payload = {
            "telegramUserId": telegram_user_id,
            "initiator": initiator,
            "type": event_type,
            "content": content,
            "metaData": meta_data
        }

        method = "POST"
        endpoint_addr = "/api/events/telegram"
        logger.info(f"Sending event to {method} {web_context.event_storage_url}{endpoint_addr}")
        try:
            await self._request(method, endpoint_addr, json=payload, max_attempts=1)
            logger.info(f"Request sended successfully to {method} {web_context.event_storage_url}{endpoint_addr}")
        except Exception as e:
            logger.error(f"Failed to save event log: {e}")

    async def get_context(self, telegram_user_id: int, limit: int = 10) -> list[dict]:
        params = {"limit": limit}
        return await self._request("GET", f"/api/events/telegram/context/{telegram_user_id}", params=params)


n8n_client = N8nClient()
event_storage_client = EventStorageClient()