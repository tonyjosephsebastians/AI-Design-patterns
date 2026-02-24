import asyncio
import os
import random
from typing import Dict, List

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel, Field

app = FastAPI(title="FastAPI Sidebar + TTS Retry Example")

SIDEBAR_MENU: Dict[str, List[str]] = {
    "top": ["Search", "Write", "Notifications"],
    "user": ["Home", "Library", "Profile", "Stories", "Stats", "Following"],
    "feeds": [
        "Generative AI",
        "ORB, Operations Research Bit",
        "Mihailo Zoin",
        "Data Science Collective",
        "Dmytro Iakubovskyi",
        "Nikhil Adithyan",
        "AI Engineer Daily",
        "Zion",
        "TDS Editors",
        "TDS Archive",
    ],
    "more": ["More"],
}

RETRYABLE_STATUS_CODES = {408, 425, 429, 500, 502, 503, 504}
DEFAULT_ATTEMPTS = 5
BASE_DELAY_SECONDS = 0.5
MAX_DELAY_SECONDS = 8.0
TTS_URL = os.getenv("TTS_URL", "").strip()
TTS_API_KEY = os.getenv("TTS_API_KEY", "").strip()


class RetryableTTSError(Exception):
    pass


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=4000)
    voice: str = "alloy"


async def _call_tts_provider(text: str, voice: str) -> bytes:
    if not TTS_URL:
        raise HTTPException(
            status_code=500,
            detail="Set TTS_URL environment variable to your TTS provider endpoint.",
        )

    payload = {"text": text, "voice": voice}
    headers = {"Content-Type": "application/json"}
    if TTS_API_KEY:
        headers["Authorization"] = f"Bearer {TTS_API_KEY}"

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(TTS_URL, json=payload, headers=headers)
    except httpx.RequestError as exc:
        raise RetryableTTSError(str(exc)) from exc

    if response.status_code in RETRYABLE_STATUS_CODES:
        raise RetryableTTSError(f"Retryable HTTP status: {response.status_code}")

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.text[:300])

    return response.content


async def _tts_with_backoff(text: str, voice: str) -> bytes:
    last_error = "unknown error"

    for attempt in range(1, DEFAULT_ATTEMPTS + 1):
        try:
            return await _call_tts_provider(text=text, voice=voice)
        except RetryableTTSError as exc:
            last_error = str(exc)
            if attempt == DEFAULT_ATTEMPTS:
                break

            exponential_delay = min(
                MAX_DELAY_SECONDS,
                BASE_DELAY_SECONDS * (2 ** (attempt - 1)),
            )
            # Full jitter spreads retries to reduce synchronized spikes.
            sleep_seconds = random.uniform(0, exponential_delay)
            await asyncio.sleep(sleep_seconds)

    raise HTTPException(
        status_code=503,
        detail=f"TTS temporarily unavailable after {DEFAULT_ATTEMPTS} attempts: {last_error}",
    )


@app.get("/")
def read_root():
    return {
        "message": "FastAPI sidebar + TTS retry example",
        "docs": "/docs",
        "demo": "/demo",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/sidebar")
def sidebar():
    return SIDEBAR_MENU


@app.post("/tts")
async def text_to_speech(data: TTSRequest):
    audio_bytes = await _tts_with_backoff(text=data.text, voice=data.voice)
    return Response(content=audio_bytes, media_type="audio/mpeg")


@app.get("/demo", response_class=HTMLResponse)
def demo_page():
    return """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Sidebar + TTS</title>
  <style>
    body {
      margin: 0;
      font-family: "Segoe UI", Tahoma, sans-serif;
      display: grid;
      grid-template-columns: 280px 1fr;
      min-height: 100vh;
      background: #f7f7f8;
    }
    aside {
      border-right: 1px solid #e2e2e2;
      background: #ffffff;
      padding: 16px;
      overflow-y: auto;
    }
    h3 { margin: 12px 0 8px; font-size: 13px; color: #666; text-transform: uppercase; }
    ul { margin: 0 0 12px; padding: 0; list-style: none; }
    li { padding: 6px 0; font-size: 15px; }
    main { padding: 24px; }
    textarea {
      width: min(760px, 100%);
      height: 170px;
      padding: 10px;
      font-size: 15px;
    }
    button {
      margin-top: 12px;
      padding: 9px 14px;
      font-size: 14px;
      cursor: pointer;
    }
    #status { margin-top: 10px; font-size: 14px; color: #555; }
  </style>
</head>
<body>
  <aside id="sidebar"></aside>

  <main>
    <h2>Text to Speech (Retry + Exponential Backoff)</h2>
    <p>Enter text and call <code>/tts</code>. Configure <code>TTS_URL</code> and optional <code>TTS_API_KEY</code>.</p>
    <textarea id="text">Building resilient systems with retry and exponential backoff.</textarea><br />
    <button onclick="speak()">Speak</button>
    <div id="status"></div>
    <audio id="player" controls style="margin-top: 12px; width: min(760px, 100%);"></audio>
  </main>

  <script>
    async function loadSidebar() {
      const res = await fetch("/sidebar");
      const data = await res.json();
      const sidebar = document.getElementById("sidebar");
      let html = "";
      for (const [section, items] of Object.entries(data)) {
        html += `<h3>${section}</h3><ul>${items.map(x => `<li>${x}</li>`).join("")}</ul>`;
      }
      sidebar.innerHTML = html;
    }

    async function speak() {
      const status = document.getElementById("status");
      const text = document.getElementById("text").value;
      status.textContent = "Generating audio...";

      const res = await fetch("/tts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, voice: "alloy" })
      });

      if (!res.ok) {
        status.textContent = "Failed: " + (await res.text());
        return;
      }

      const blob = await res.blob();
      const player = document.getElementById("player");
      player.src = URL.createObjectURL(blob);
      status.textContent = "Audio ready";
      player.play();
    }

    loadSidebar();
  </script>
</body>
</html>
"""
