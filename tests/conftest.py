import asyncio
from typing import Any, AsyncGenerator, Generator

import pytest_asyncio
from httpx import AsyncClient

from tests.fastapi_app import app


@pytest_asyncio.fixture(scope="session", autouse=True)
def event_loop() -> Generator[asyncio.AbstractEventLoop, Any, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop

    loop.close()


@pytest_asyncio.fixture(scope="module")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://testserver") as client_:
        yield client_
