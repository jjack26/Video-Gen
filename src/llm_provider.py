"""OpenAI Responses API adapter; no requests unless explicitly enabled."""
from __future__ import annotations
import json
import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError

class ProviderDisabled(RuntimeError):
    pass

def draft_text(instructions: str, prompt: str, *, enabled: bool = False, model: str = "gpt-4.1-mini", max_output_tokens: int = 350) -> str:
    if not enabled:
        raise ProviderDisabled("Live API disabled; use the offline demo first")
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ProviderDisabled("OPENAI_API_KEY not configured")
    if not 1 <= max_output_tokens <= 600:
        raise ValueError("max_output_tokens outside safety range")
    if len(instructions) > 8000 or len(prompt) > 12000:
        raise ValueError("prompt exceeds local length limits")
    body = json.dumps({"model": model, "instructions": instructions, "input": prompt, "max_output_tokens": max_output_tokens, "store": False}).encode()
    request = Request("https://api.openai.com/v1/responses", data=body, headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"}, method="POST")
    try:
        with urlopen(request, timeout=40) as response:
            data = json.load(response)
    except HTTPError as exc:
        raise RuntimeError("OpenAI API request failed with HTTP " + str(exc.code)) from None
    parts = [part.get("text", "") for item in data.get("output", []) if item.get("type") == "message" for part in item.get("content", []) if part.get("type") == "output_text"]
    if not parts:
        raise RuntimeError("API response contained no output text")
    return "\n".join(parts)
