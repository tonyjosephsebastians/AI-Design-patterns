# FastAPI Sidebar + TTS Retry Example

This document explains how the example in `main.py` works end to end.

## 1) High-Level Purpose

The app demonstrates two things in one FastAPI service:

1. A sidebar menu API (`/sidebar`) for UI navigation data.
2. A Text-to-Speech API (`/tts`) that is resilient to transient failures using retry + exponential backoff + jitter.

It also includes:

1. A health endpoint (`/health`) for monitoring.
2. A demo HTML page (`/demo`) that renders the sidebar and calls `/tts`.

## 2) File Overview

Main file:

- `main.py` defines constants, request models, retry logic, API routes, and the demo UI page.

## 3) Configuration (Environment Variables)

The TTS endpoint uses:

1. `TTS_URL` (required)
2. `TTS_API_KEY` (optional)

Read at startup time:

- `TTS_URL = os.getenv("TTS_URL", "").strip()`
- `TTS_API_KEY = os.getenv("TTS_API_KEY", "").strip()`

If `TTS_URL` is missing, `/tts` returns HTTP 500 with a setup message.

## 4) Constants and Their Meaning

Retry settings:

1. `RETRYABLE_STATUS_CODES = {408, 425, 429, 500, 502, 503, 504}`
2. `DEFAULT_ATTEMPTS = 5`
3. `BASE_DELAY_SECONDS = 0.5`
4. `MAX_DELAY_SECONDS = 8.0`

Meaning:

1. Retry only for transient/network/server overload style failures.
2. Try at most 5 times total.
3. Delay grows exponentially from 0.5s.
4. Delay is capped to avoid unbounded wait.

## 5) Sidebar Data

`SIDEBAR_MENU` is a dictionary with sections:

1. `top`: `Search`, `Write`, `Notifications`
2. `user`: `Home`, `Library`, `Profile`, `Stories`, `Stats`, `Following`
3. `feeds`: curated list (`Generative AI`, `TDS Editors`, etc.)
4. `more`: `More`

Route:

- `GET /sidebar` returns this dictionary directly.

## 6) Request Model for TTS

`TTSRequest` (Pydantic model) validates incoming JSON for `/tts`:

1. `text: str` (required, min length 1, max length 4000)
2. `voice: str` (default `"alloy"`)

Example request body:

```json
{
  "text": "Building resilient systems with exponential backoff.",
  "voice": "alloy"
}
```

## 7) TTS Call Flow

There are two layers:

1. `_call_tts_provider(text, voice)` makes one HTTP call to the provider.
2. `_tts_with_backoff(text, voice)` wraps the first function with retry logic.

### 7.1 `_call_tts_provider` (single attempt)

Steps:

1. Verify `TTS_URL` is set, else HTTP 500.
2. Build JSON payload: `{"text": ..., "voice": ...}`.
3. Build headers:
4. Always include `Content-Type: application/json`.
5. Add `Authorization: Bearer <TTS_API_KEY>` if API key exists.
6. Send async POST using `httpx.AsyncClient(timeout=20.0)`.
7. If network-level error (`httpx.RequestError`), convert to `RetryableTTSError`.
8. If response status is retryable (e.g., 503), raise `RetryableTTSError`.
9. If response status is other 4xx/5xx, raise `HTTPException` immediately (non-retry path).
10. On success, return raw audio bytes.

### 7.2 `_tts_with_backoff` (retry strategy)

Algorithm:

1. Loop attempts `1..DEFAULT_ATTEMPTS`.
2. Try `_call_tts_provider`.
3. If success, return immediately.
4. If `RetryableTTSError`:
5. If this is the final attempt, stop and return HTTP 503.
6. Else compute delay:
7. `exponential_delay = min(MAX_DELAY_SECONDS, BASE_DELAY_SECONDS * 2^(attempt-1))`
8. Apply full jitter: `sleep = random.uniform(0, exponential_delay)`
9. `await asyncio.sleep(sleep)` and retry.
10. If all attempts fail, return HTTP 503 with last error message.

Why jitter is used:

1. Without jitter, many clients retry in lockstep and can spike traffic again.
2. Full jitter spreads retries over a random window.

## 8) API Endpoints

1. `GET /`
2. Returns service metadata (`message`, `docs`, `demo` links).

3. `GET /health`
4. Returns `{"status": "ok"}`.

5. `GET /sidebar`
6. Returns sidebar menu JSON.

7. `POST /tts`
8. Input: `TTSRequest`.
9. Output: audio bytes with `Content-Type: audio/mpeg`.
10. Error behavior:
11. HTTP 500 if `TTS_URL` missing.
12. HTTP 503 if transient failures persist after retries.
13. Provider status passthrough for non-retryable HTTP failures.

14. `GET /demo`
15. Returns HTML UI:
16. Left panel loads menu from `/sidebar`.
17. Main panel sends text to `/tts`.
18. On success it plays audio in `<audio>`.

## 9) Demo Page Behavior

Client-side JavaScript has two functions:

1. `loadSidebar()`
2. Calls `/sidebar`, then renders each section and its items.

3. `speak()`
4. Reads text from textarea.
5. Sends POST `/tts` with JSON body.
6. If response is error, prints response text in status area.
7. If success, creates blob URL and plays audio in browser.

## 10) Runtime Sequence (Practical)

When user clicks **Speak**:

1. Browser sends `POST /tts`.
2. FastAPI validates body with `TTSRequest`.
3. Server enters `_tts_with_backoff`.
4. Server calls provider via `_call_tts_provider`.
5. If transient failure, wait random exponential delay and retry.
6. If success, return audio bytes.
7. Browser receives bytes, creates object URL, starts playback.

## 11) Run Instructions

From `api design` folder:

```powershell
pip install fastapi uvicorn httpx
$env:TTS_URL="https://your-provider-endpoint"
$env:TTS_API_KEY="your-key"   # optional
uvicorn main:app --reload
```

Then open:

- `http://127.0.0.1:8000/demo`
- `http://127.0.0.1:8000/docs`

## 12) Common Issues

1. `500 Set TTS_URL...`
2. Cause: `TTS_URL` not set before app start.

3. `503 TTS temporarily unavailable...`
4. Cause: provider/network kept failing through all retry attempts.

5. `/tts` returns non-audio data
6. Cause: provider endpoint contract mismatch with expected payload/output.
7. Fix by adapting payload/headers/response parsing in `_call_tts_provider`.

## 13) Suggested Next Improvements

1. Add request timeout and retry settings via env vars.
2. Add structured logs with attempt count and delay.
3. Add unit tests for retryable vs non-retryable behavior.
4. Add idempotency key support for duplicate client submissions.

