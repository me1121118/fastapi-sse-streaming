"""
fastapi-sse-streaming: Clean, reliable Server-Sent Events (SSE) streaming for FastAPI.
Perfect for ChatGPT-like typewriter AI responses and real-time event feeds.
"""

import asyncio
import json
from typing import Any, AsyncGenerator, AsyncIterable, Dict, Optional, Union
from fastapi.responses import StreamingResponse

class ServerSentEvent:
    """Represents a single Server-Sent Event formatted according to the SSE specification."""
    def __init__(
        self,
        data: Union[str, Dict[str, Any], Any],
        event: Optional[str] = None,
        id: Optional[str] = None,
        retry: Optional[int] = None
    ):
        self.data = data
        self.event = event
        self.id = id
        self.retry = retry

    def encode(self) -> bytes:
        lines = []
        if self.id is not None:
            lines.append(f"id: {self.id}")
        if self.event is not None:
            lines.append(f"event: {self.event}")
        if self.retry is not None:
            lines.append(f"retry: {self.retry}")

        if isinstance(self.data, (dict, list)):
            data_str = json.dumps(self.data)
        else:
            data_str = str(self.data)

        for line in data_str.splitlines():
            lines.append(f"data: {line}")

        return ("\n".join(lines) + "\n\n").encode("utf-8")

class SSEResponse(StreamingResponse):
    """FastAPI StreamingResponse preconfigured for Server-Sent Events."""
    def __init__(
        self,
        generator: AsyncIterable[Union[str, Dict[str, Any], ServerSentEvent]],
        ping_interval: Optional[float] = None,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None
    ):
        sse_headers = {
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no", # Disable proxy buffering for Nginx/Cloudflare
        }
        if headers:
            sse_headers.update(headers)

        async def stream_wrapper():
            async for item in generator:
                if isinstance(item, ServerSentEvent):
                    yield item.encode()
                elif isinstance(item, (dict, list)):
                    yield ServerSentEvent(data=item).encode()
                else:
                    yield ServerSentEvent(data=str(item)).encode()

        super().__init__(
            content=stream_wrapper(),
            status_code=status_code,
            headers=sse_headers,
            media_type="text/event-stream"
        )
