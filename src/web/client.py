import asyncio
import json

import httpx

from config import get_logger

from utils.formatters import format_json_body
from app.context import web_context
from exceptions import ServiceUnavailableError


logger = get_logger("bot.services")

class N8nClient:
    _client: httpx.AsyncClient | None = None
    MAX_RETRIES = 3
    TIMEOUT = httpx.Timeout(120.0, connect=5.0) 

    @classmethod
    def _get_client(cls) -> httpx.AsyncClient:
        if cls._client is None or cls._client.is_closed:
            cls._client = httpx.AsyncClient(
                base_url=web_context.n8n_url, 
                timeout=cls.TIMEOUT
            )
        return cls._client

    @classmethod
    async def close(cls):
        if cls._client and not cls._client.is_closed:
            await cls._client.aclose()

    @classmethod
    async def get_answer(cls, query: str) -> str:
        client = cls._get_client()
        
        payload = {"query": query} 

        for attempt in range(1, cls.MAX_RETRIES + 1):
            try:
                #TODO: define endpoint address 
                response = await client.post("/webhook/pipeline", json=payload)
                response.raise_for_status()
                return format_json_body(response.json()) 
                
            except httpx.HTTPError as e:
                logger.warning(f"Attempt {attempt} failed: {e}")
                
                if attempt == cls.MAX_RETRIES:
                    logger.error("All N8n retry attempts failed")
                    raise ServiceUnavailableError("Failed to get response from N8n-service") from e
                
                await asyncio.sleep(2 ** (attempt - 1))

