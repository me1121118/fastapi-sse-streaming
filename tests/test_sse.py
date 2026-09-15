import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from fastapi_sse_streaming import SSEResponse, ServerSentEvent

@pytest.fixture
def app():
    fastapi_app = FastAPI()

    @fastapi_app.get("/stream-text")
    async def stream_text():
        async def generator():
            yield "Hello"
            yield "World"
        return SSEResponse(generator())

    @fastapi_app.get("/stream-events")
    async def stream_events():
        async def generator():
            yield ServerSentEvent(data={"chunk": "first"}, event="delta", id="1")
            yield ServerSentEvent(data="[DONE]", event="done")
        return SSEResponse(generator())

    return fastapi_app

@pytest.mark.asyncio
async def test_sse_text_stream(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/stream-text")
        assert resp.status_code == 200
        assert resp.headers["content-type"].startswith("text/event-stream")
        content = resp.text
        assert "data: Hello\n\n" in content
        assert "data: World\n\n" in content

@pytest.mark.asyncio
async def test_sse_event_stream(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/stream-events")
        assert resp.status_code == 200
        content = resp.text
        assert "event: delta" in content
        assert "id: 1" in content
        assert 'data: {"chunk": "first"}' in content
        assert "event: done" in content
        assert "data: [DONE]" in content
