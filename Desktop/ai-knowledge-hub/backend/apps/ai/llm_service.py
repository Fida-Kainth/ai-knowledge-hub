"""
Socket.IO server (Async) for realtime token streaming and a helper
`query_llm` function for non-streaming HTTP requests.

- sio: AsyncServer instance used by project_name.asgi to mount sockets.
- chat_message handler streams tokens (demo) or can be extended to
  connect to a provider's streaming API.
- query_llm(prompt, options) returns a text response (sync function).
"""
import asyncio
import os
import json
import logging

import socketio
from django.conf import settings

logger = logging.getLogger(__name__)

# Async Socket.IO server instance (ASGI)
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


async def _fake_token_stream(prompt: str):
    """
    Simple async generator that yields tokens for demo purposes.
    Replace with real streaming from provider.
    """
    text = f"This is a demo streamed response for: {prompt}"
    for ch in text.split():
        await asyncio.sleep(0.04)
        yield ch + " "


@sio.event
async def connect(sid, environ):
    await sio.emit("server_ready", {"message": "Connected to AI Socket"}, to=sid)
    logger.debug("Client connected: %s", sid)


@sio.event
async def disconnect(sid):
    logger.debug("Client disconnected: %s", sid)


@sio.event
async def chat_message(sid, data):
    """
    Expected client payload:
      {"prompt": "Write me an intro about X", "session_id": "abc"}
    Emits:
      - 'chat_token' events with {'token': '...'}
      - 'chat_done' when complete
      - 'chat_error' on error
    """
    prompt = (data or {}).get("prompt", "")
    if not prompt:
        await sio.emit("chat_error", {"error": "prompt required"}, to=sid)
        return

    try:
        # If you want to hook provider streaming, add it here.
        async for token in _fake_token_stream(prompt):
            await sio.emit("chat_token", {"token": token}, to=sid)
        await sio.emit("chat_done", {"ok": True}, to=sid)
    except Exception as exc:
        logger.exception("Error streaming tokens")
        await sio.emit("chat_error", {"error": str(exc)}, to=sid)


def query_llm(prompt: str, options: dict | None = None) -> str:
    """
    Synchronous (blocking) LLM query helper.
    - If OPENAI_API_KEY present, call OpenAI chat completions (try best-effort).
    - Otherwise return a safe echo fallback.

    options can include model, temperature, etc.
    """
    options = options or {}
    api_key = getattr(settings, "OPENAI_API_KEY", "") or os.getenv("OPENAI_API_KEY", "")
    model = options.get("model") or getattr(settings, "OPENAI_MODEL", None)

    if api_key:
        try:
            # Try modern "openai" python package usage (best-effort)
            import openai
            openai.api_key = api_key
            # Use ChatCompletion if available
            messages = [{"role": "user", "content": prompt}]
            params = {"model": model or "gpt-4o-mini", "messages": messages}
            # allow temperature override
            if "temperature" in options:
                params["temperature"] = options["temperature"]
            resp = openai.ChatCompletion.create(**params)
            # Support both v1 schema and older
            if hasattr(resp, "choices"):
                # resp.choices[0].message.content
                choice = resp.choices[0]
                # some SDKs return message dict, some return .message
                content = ""
                if isinstance(choice, dict):
                    content = choice.get("message", {}).get("content") or choice.get("text", "")
                else:
                    # object path
                    content = getattr(getattr(choice, "message", None), "content", None) or getattr(choice, "text", "")
                if content:
                    return content
            # Last fallback
            return str(resp)
        except Exception:
            # fall through to other providers if available
            logger.exception("OpenAI call failed, falling back to echo.")
    # No key or provider failed: safe fallback
    return f"Echo: {prompt}"
