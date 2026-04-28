"""Minimal Ollama client for Gemma 4. Text-in/text-out, no tools, no history."""

from __future__ import annotations

import sys
import time

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "gemma4:e4b-it-q8_0"
DEFAULT_TIMEOUT = 600


def ask_gemma(prompt: str, model: str = DEFAULT_MODEL) -> str:
    """Send a single prompt to Ollama, return the full response. Raises on non-2xx."""
    response = requests.post(
        OLLAMA_URL,
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=DEFAULT_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()["response"]


def _cli() -> None:
    if len(sys.argv) < 2:
        print('usage: python -m src.gemma_client "<prompt>" [model]', file=sys.stderr)
        sys.exit(1)

    prompt = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) >= 3 else DEFAULT_MODEL

    print(f"[{model}] prompt: {len(prompt)} chars", file=sys.stderr)
    t0 = time.perf_counter()
    answer = ask_gemma(prompt, model=model)
    elapsed = time.perf_counter() - t0
    print(f"[{model}] response: {len(answer)} chars in {elapsed:.1f}s", file=sys.stderr)
    print(answer)


if __name__ == "__main__":
    _cli()
