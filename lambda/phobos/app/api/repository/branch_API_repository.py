from typing import Annotated
from fastapi import Depends
from httpx import AsyncClient
import os
from dotenv import load_dotenv
from pathlib import Path
from app.api.services.service_client.api_client import get_rest_api_client

# Load environment variables based on environment
if os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
    # Running in Lambda - environment variables are already loaded
    pass
else:
    # Local development - load from .env files
    # Try to load from project root .env first
    env_path = Path(__file__).parent.parent.parent.parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        # Fallback to test.env
        load_dotenv("./environments/test.env")


class BranchServiceClient:
    def __init__(self, api_client: AsyncClient):
        self.api_client = api_client

    # async def get_branches(self, branch_id: str):
    #     resp = await self.api_client.get(f"/v1/branch/{branch_id}")

    #     if resp.status_code != 200:
    #         print("Error fetching branch data")
    #         return None
    #     return resp.json()
    async def get_branches(self, branch_id: str):
        url = f"/v1/branch/{branch_id}"
        resp = await self.api_client.get(url)

        if resp.status_code != 200:
            return None
        return resp.json()  # branch details

    async def get_branches_by_bank_name(self, bank_name: str):
        url = f"/v1/branches?bank_name={bank_name}"
        resp = await self.api_client.get(url)
        if resp.status_code != 200:
            return []
        return resp.json()  # list of branches


async def get_branch_service_client():
    branch_service_url = os.getenv("BRANCH_BASE_URL")
    async for client in get_rest_api_client(branch_service_url):
        yield BranchServiceClient(client)


BranchServiceClientDependency = Annotated[
    BranchServiceClient, Depends(get_branch_service_client)
]
