# 🌊 fastapi-sse-streaming

[![FastAPI](https://img.shields.io/badge/FastAPI-Supported-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Protocol: SSE](https://img.shields.io/badge/Protocol-Server--Sent%20Events-0ea5e9.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)]()

> Clean, reliable Server-Sent Events (SSE) streaming response for FastAPI. Perfect for building ChatGPT-style typewriter interfaces.

Includes automatic spec formatting (`data: ...\n\n`), custom event IDs, and anti-buffering headers (`X-Accel-Buffering: no` for Nginx and Cloudflare).

---

### ☕ Support My Studies / Buy Me a Coffee

Hey there! 👋 I build and open-source lightweight, focused developer tools.

If this small package helped you build streaming AI features, please consider supporting my college/tuition fund:
- ☕ **Buy Me a Coffee:** [buymeacoffee.com/yourname](https://www.buymeacoffee.com)
- 💖 **Ko-fi:** [buymeacoffee.com/kcidi4148](https://buymeacoffee.com/kcidi4148)
- ⭐ **Star this repository** to help other developers discover it!

---

## 📦 Installation

```bash
pip install git+https://github.com/me1121118/fastapi-sse-streaming.git
```

---

## 🚀 Quick Example

```python
import asyncio
from fastapi import FastAPI
from fastapi_sse_streaming import SSEResponse, ServerSentEvent

app = FastAPI()

@app.get("/chat/stream")
async def chat_stream():
    async def token_generator():
        words = ["This", "is", "a", "streaming", "response", "from", "FastAPI!"]
        for word in words:
            await asyncio.sleep(0.1)
            # Yield simple text or rich ServerSentEvent
            yield ServerSentEvent(data={"token": word}, event="token")
        
        yield ServerSentEvent(data="[DONE]", event="finish")

    return SSEResponse(token_generator())
```

---

## 🧪 Testing

```bash
pytest -v tests
```

---

## 📄 License

MIT License. Free for personal and commercial use.
