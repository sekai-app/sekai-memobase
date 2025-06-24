from httpx import AsyncClient

from ..models.response import BillingData
from ..models.utils import Promise, CODE
from ..connectors import ADMIN_URL


async def get_project_usage(project_id: str) -> Promise[BillingData]:
    if ADMIN_URL is None:
        return Promise.reject(CODE.SERVICE_UNAVAILABLE, "Memobase Admin URL not set")
    async with AsyncClient(base_url=ADMIN_URL) as client:
        response = await client.get(f"billing/projects/{project_id}")
        if response.status_code != 200:
            return Promise.reject(
                CODE.SERVICE_UNAVAILABLE,
                f"Failed to get project usage: {response.text}",
            )
        return Promise.resolve(BillingData(**response.json()["data"]))


async def cost_project_usage(
    project_id: str, input_tokens: int, output_tokens: int
) -> Promise[None]:
    if ADMIN_URL is None:
        return Promise.reject(CODE.SERVICE_UNAVAILABLE, "Memobase Admin URL not set")
    async with AsyncClient(base_url=ADMIN_URL) as client:
        response = await client.post(
            f"billing/projects/{project_id}",
            json={"usage": input_tokens + output_tokens},
        )
        if response.status_code != 200:
            return Promise.reject(
                CODE.SERVICE_UNAVAILABLE,
                f"Failed to cost project usage: {response.text}",
            )
        return Promise.resolve(None)
