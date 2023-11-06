from typing import Any, Dict

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_query(async_client: AsyncClient) -> None:
    params: Dict[str, Any] = {"id": 100, "title": "test", "data": [1, 2, 3, 4, 5]}

    response_post = await async_client.post(
        url="/test_query",
        params=params,
    )

    assert response_post.status_code == 200
    assert response_post.json() == {"data": {"id": 100, "title": "test", "data": [1, 2, 3, 4, 5]}}


@pytest.mark.asyncio
async def test_body(async_client: AsyncClient) -> None:
    params: Dict[str, Any] = {"id": 100, "title": "test", "data": [1, 2, 3, 4, 5]}

    response_post = await async_client.post(
        url="/test_body",
        json=params,
    )

    assert response_post.status_code == 200
    assert response_post.json() == {"data": {"id": 100, "title": "test", "data": [1, 2, 3, 4, 5]}}


@pytest.mark.asyncio
async def test_form(async_client: AsyncClient) -> None:
    params: Dict[str, Any] = {"id": 100, "title": "test"}

    response_post = await async_client.post(
        url="/test_form",
        data=params,
    )

    assert response_post.status_code == 200
    assert response_post.json() == {"data": {"id": 100, "title": "test"}}


@pytest.mark.asyncio
async def test_pyfa_form(async_client: AsyncClient) -> None:
    params: Dict[str, Any] = {"id": 100, "title": "test"}

    response_post = await async_client.post(
        url="/test_pyfa_form",
        data=params,
    )

    assert response_post.status_code == 200
    assert response_post.json() == {"data": {"id": 100, "title": "test"}}


@pytest.mark.asyncio
async def test_query_gt_valid(async_client: AsyncClient) -> None:
    params: Dict[str, Any] = {"id": 100, "title": "test"}

    response_post = await async_client.post(
        url="/test_query_gt",
        params=params,
    )

    assert response_post.status_code == 200
    assert response_post.json() == {"data": {"id": 100, "title": "test"}}


@pytest.mark.asyncio
async def test_query_gt_invalid(async_client: AsyncClient) -> None:
    params: Dict[str, Any] = {"id": -100, "title": "test"}

    response_post = await async_client.post(
        url="/test_query_gt",
        params=params,
    )

    assert response_post.status_code == 422
