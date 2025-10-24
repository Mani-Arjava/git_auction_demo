from typing import Annotated
import httpx
from httpx import AsyncClient
from fastapi import Depends


async def get_rest_api_client(base_url: str):
    async with httpx.AsyncClient(base_url=base_url) as client:
        yield client


APIClientDependency = Annotated[AsyncClient, Depends(get_rest_api_client)]
