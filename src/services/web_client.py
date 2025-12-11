import asyncio
import json

import httpx
from environs import Env

from log import get_logger

from .message_formatter import format_rag_agent_response
from app import WebContext


logger = get_logger("bot.services")

#TODO: edit client depending on answer 
class N8nClient:
    N8N_URL = WebContext.n8n_url
    MAX_RETRIES = 3

    @classmethod
    async def get_response(cls, query: str) -> str:
        for attempt in range(cls.MAX_RETRIES):
            try:

                async with httpx.AsyncClient(timeout=120.0) as client:
                    response = await client.post(
                        cls.N8N_URL,
                        content=json.dumps(query),
                        headers={"Content-Type": "application/json"},
                    )
                    response.raise_for_status()
                    return format_rag_agent_response(response.json())
                
            except (httpx.RequestError, httpx.HTTPStatusError) as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")

                if attempt == cls.MAX_RETRIES - 1:
                    logger.error("All retry attempts failed")
                    raise RuntimeError("Failed to get response from RAG-service") from e
                await asyncio.sleep(2**attempt * 3)


